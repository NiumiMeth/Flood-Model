from flask import Flask, render_template, request
import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression


app = Flask(__name__)


def load_dataset_options():
    """Load unique values from dataset for dropdowns and defaults"""
    data_path = os.path.join("Ipynb files", "data.csv")
    df = pd.read_csv(data_path)
    
    return {
        'cities': sorted(df['city_name'].dropna().unique().tolist()),
        'admin_wards': sorted(df['admin_ward'].dropna().unique().tolist())[:50],  # Limit to first 50
        'land_use': sorted(df['land_use'].dropna().unique().tolist()),
        'storm_drain_types': sorted(df['storm_drain_type'].dropna().unique().tolist()),
        'soil_groups': sorted(df['soil_group'].dropna().unique().tolist()),
        'dem_sources': sorted(df['dem_source'].dropna().unique().tolist()),
        'rainfall_sources': sorted(df['rainfall_source'].dropna().unique().tolist()),
        'return_periods': sorted(df['return_period_years'].dropna().unique().tolist()),
        'catchment_ids': sorted(df['catchment_id'].dropna().unique().tolist())[:50],  # Limit to first 50
        # Defaults based on median/mode values
        'defaults': {
            'elevation_m': float(df['elevation_m'].median()) if not df['elevation_m'].isna().all() else 15.0,
            'drainage_density_km_per_km2': float(df['drainage_density_km_per_km2'].median()) if not df['drainage_density_km_per_km2'].isna().all() else 7.0,
            'storm_drain_proximity_m': float(df['storm_drain_proximity_m'].median()) if not df['storm_drain_proximity_m'].isna().all() else 100.0,
            'historical_rainfall_intensity_mm_hr': float(df['historical_rainfall_intensity_mm_hr'].median()) if not df['historical_rainfall_intensity_mm_hr'].isna().all() else 50.0,
            'return_period_years': int(df['return_period_years'].mode()[0]) if len(df['return_period_years'].mode()) > 0 else 10,
            'dem_source': df['dem_source'].mode()[0] if len(df['dem_source'].mode()) > 0 else 'SRTM_3arc',
            'rainfall_source': df['rainfall_source'].mode()[0] if len(df['rainfall_source'].mode()) > 0 else 'ERA5',
            'soil_group': df['soil_group'].mode()[0] if len(df['soil_group'].mode()) > 0 else 'B',
        }
    }


def build_and_train_model():
    """
    Rebuilds and trains the same pipeline you created in the notebook,
    using the dataset in the Ipynb files folder.
    This runs once when the Flask app starts.
    """
    # Adjust path so the app can find your CSV from the project root
    data_path = os.path.join("Ipynb files", "data.csv")

    df = pd.read_csv(data_path)

    # Recreate target
    df["is_risky"] = df["risk_labels"].apply(lambda x: 0 if x == "monitor" else 1)

    # Features / target
    X = df.drop(columns=["is_risky"])
    y = df["is_risky"]

    # Stratified split (same as notebook, mostly for consistency)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # Feature type definitions (copied from notebook)
    numerical_features = [
        "latitude",
        "longitude",
        "elevation_m",
        "drainage_density_km_per_km2",
        "storm_drain_proximity_m",
        "historical_rainfall_intensity_mm_hr",
        "return_period_years",
    ]

    categorical_features = [
        "city_name",
        "admin_ward",
        "catchment_id",
        "dem_source",
        "land_use",
        "soil_group",
        "storm_drain_type",
        "rainfall_source",
    ]

    # Preprocessing pipelines
    numerical_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )

    categorical_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="constant", fill_value="missing")),
            ("onehot", OneHotEncoder(handle_unknown="ignore")),
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numerical_transformer, numerical_features),
            ("cat", categorical_transformer, categorical_features),
        ],
        remainder="drop",
    )

    # Final model pipeline (Logistic Regression as in the notebook before GridSearch)
    model_pipeline = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("classifier", LogisticRegression(random_state=42, max_iter=200)),
        ]
    )

    # Fit on the training data
    model_pipeline.fit(X_train[numerical_features + categorical_features], y_train)

    return model_pipeline, numerical_features, categorical_features


# Load dataset options and train model once at startup
DATASET_OPTIONS = load_dataset_options()
model, NUMERICAL_FEATURES, CATEGORICAL_FEATURES = build_and_train_model()


@app.route("/", methods=["GET", "POST"])
def index():
    prediction = None
    probability = None
    error_message = None
    form_values = {}

    if request.method == "POST":
        try:
            # Collect numerical inputs safely
            numeric_data = {}
            for feature in NUMERICAL_FEATURES:
                value_str = request.form.get(feature, "").strip()
                form_values[feature] = value_str
                if value_str == "":
                    # Use default if empty
                    if feature in DATASET_OPTIONS['defaults']:
                        numeric_data[feature] = DATASET_OPTIONS['defaults'][feature]
                    else:
                        numeric_data[feature] = None
                else:
                    numeric_data[feature] = float(value_str)

            # Collect categorical inputs
            categorical_data = {}
            for feature in CATEGORICAL_FEATURES:
                value_str = request.form.get(feature, "").strip()
                form_values[feature] = value_str
                if value_str == "":
                    # Use default if available
                    if feature in DATASET_OPTIONS['defaults']:
                        categorical_data[feature] = DATASET_OPTIONS['defaults'][feature]
                    else:
                        categorical_data[feature] = None
                else:
                    categorical_data[feature] = value_str

            # Build single-row DataFrame for prediction
            input_data = {**numeric_data, **categorical_data}
            input_df = pd.DataFrame([input_data])

            # Run prediction
            y_pred = model.predict(input_df)[0]

            # If the model supports predict_proba, show the risk probability
            if hasattr(model, "predict_proba"):
                proba = model.predict_proba(input_df)[0][1]  # Probability of class 1 (risky)
                probability = round(float(proba) * 100, 2)

            prediction = "Risky (1)" if y_pred == 1 else "Monitor (0)"

        except ValueError:
            error_message = "Please check your numerical inputs. They must be valid numbers."
        except Exception as e:
            # In a real app, you might log this instead of showing the raw error
            error_message = f"An unexpected error occurred: {e}"

    return render_template(
        "index.html",
        numerical_features=NUMERICAL_FEATURES,
        categorical_features=CATEGORICAL_FEATURES,
        prediction=prediction,
        probability=probability,
        error_message=error_message,
        form_values=form_values,
        dataset_options=DATASET_OPTIONS,
        defaults=DATASET_OPTIONS['defaults'],
    )


if __name__ == "__main__":
    # Run the app in debug mode for development
    app.run(debug=True)
