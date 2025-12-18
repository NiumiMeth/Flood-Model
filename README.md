# Flood Risk Prediction Web App

A machine learning-powered web application that predicts flood risk based on geographical, environmental, and meteorological features. The application uses a trained logistic regression model to classify locations as either "Monitor" (low risk) or "Risky" (high flood risk).

## 🖼️ Interface Screenshots

<div align="center">
  <img src="Images/flood 1.png" alt="Flood Prediction Interface 1" width="45%" style="margin: 10px;">
  <img src="Images/flood 4.png" alt="Flood Prediction Interface 2" width="45%" style="margin: 10px;">
  <br>
  <img src="Images/flood 2.png" alt="Flood Prediction Interface 3" width="45%" style="margin: 10px;">
  <img src="Images/flood 3.png" alt="Flood Prediction Interface 4" width="45%" style="margin: 10px;">
</div>

## 📊 Data Analysis & Model Development

### Exploratory Data Analysis (`flood_EDA.ipynb`)

The EDA notebook provides comprehensive analysis of the flood risk dataset:

**Dataset Overview:**
- **Total Records**: 2,963 entries
- **Features**: 17 columns (6 numerical, 10 categorical, 1 target)
- **Target Variable**: `risk_labels` (binary classification: "monitor" vs "risky")

**Key Features Analyzed:**
- **Geographical**: `latitude`, `longitude`, `elevation_m`
- **Infrastructure**: `drainage_density_km_per_km2`, `storm_drain_proximity_m`, `storm_drain_type`
- **Environmental**: `land_use`, `soil_group`, `catchment_id`
- **Meteorological**: `historical_rainfall_intensity_mm_hr`, `return_period_years`, `rainfall_source`
- **Administrative**: `city_name`, `admin_ward`, `dem_source`

**Analysis Performed:**
- Data type identification and missing value analysis
- Numerical feature distribution visualization (histograms and box plots)
- Categorical feature exploration
- Outlier detection and data quality assessment

### Model Development (`Model.ipynb`)

#### 1. **Target Variable Creation**
- Converted multi-class `risk_labels` to binary classification:
  - `0` = "monitor" (low risk)
  - `1` = "risky" (high risk - any label other than "monitor")
- Class distribution: ~67% "monitor", ~33% "risky"

#### 2. **Data Preprocessing Pipeline**

**Feature Type Definition:**
- **Numerical Features** (7): `latitude`, `longitude`, `elevation_m`, `drainage_density_km_per_km2`, `storm_drain_proximity_m`, `historical_rainfall_intensity_mm_hr`, `return_period_years`
- **Categorical Features** (8): `city_name`, `admin_ward`, `catchment_id`, `dem_source`, `land_use`, `soil_group`, `storm_drain_type`, `rainfall_source`
- **Excluded Features**: `segment_id` (identifier), `risk_labels` (target)

**Preprocessing Steps:**

**Numerical Features Pipeline:**
```python
numerical_transformer = Pipeline([
    ('imputer', SimpleImputer(strategy='median')),  # Handle missing values
    ('scaler', StandardScaler())                     # Standardize features
])
```

**Categorical Features Pipeline:**
```python
categorical_transformer = Pipeline([
    ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),  # Fill missing with 'missing'
    ('onehot', OneHotEncoder(handle_unknown='ignore'))                      # One-hot encoding
])
```

**Combined Preprocessing:**
- Used `ColumnTransformer` to apply appropriate transformations to each feature type
- Automatically handles unknown categories in production data
- Drops unused columns (remainder='drop')

#### 3. **Machine Learning Pipeline**

**Full Pipeline Structure:**
```python
model_pipeline = Pipeline([
    ('preprocessor', ColumnTransformer([...])),
    ('classifier', LogisticRegression(random_state=42))
])
```

**Model Selection:**
- **Algorithm**: Logistic Regression (linear classifier)
- **Rationale**: Interpretable, fast, works well with mixed feature types after preprocessing

#### 4. **Hyperparameter Tuning**

**Grid Search Configuration:**
- **Regularization (C)**: [0.1, 1, 10]
- **Solver**: ['lbfgs', 'liblinear']
- **Max Iterations**: [100, 200]
- **Cross-Validation**: 5-fold CV
- **Scoring Metric**: Accuracy

**Best Parameters Found:**
- `C`: 0.1 (stronger regularization)
- `solver`: 'lbfgs'
- `max_iter`: 100
- **Best CV Score**: 0.8215 (82.15% accuracy)

#### 5. **Model Performance**

**Test Set Results:**
- **Accuracy**: 79.26%
- **Precision (Monitor)**: 0.86
- **Recall (Monitor)**: 0.83
- **F1-Score (Monitor)**: 0.84
- **Precision (Risky)**: 0.67
- **Recall (Risky)**: 0.72
- **F1-Score (Risky)**: 0.70

**Data Split:**
- **Training Set**: 80% (2,370 samples)
- **Test Set**: 20% (593 samples)
- **Stratified Split**: Maintains class distribution in both sets

#### 6. **Pipeline Implementation in Web App**

The Flask web application (`app.py`) replicates the exact preprocessing pipeline and model training process from the notebook:
- Same feature definitions (numerical vs categorical)
- Identical preprocessing steps (imputation, scaling, encoding)
- Same model architecture (Logistic Regression)
- Model retrains on startup using the full dataset

---

## 🚀 Quick Start

### Setup
1. **Create virtual environment**:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # source venv/bin/activate  # macOS/Linux
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python app.py
   ```

4. **Access the app**: Open `http://127.0.0.1:5000/` in your browser

### Project Structure
```
Flood Model/
├── notebooks/
│   ├── flood_EDA.ipynb          # Exploratory data analysis
│   └── Model.ipynb               # Model development & training
├── data/
│   └── data.csv                  # Training dataset
├── Images/
│   ├── flood 1.png              # Interface screenshots
│   ├── flood 2.png
│   ├── flood 3.png
│   └── flood 4.png
├── templates/
│   └── index.html                # Web interface
├── static/
│   └── style.css                 # Styling
├── app.py                        # Flask application
├── requirements.txt              # Dependencies
└── README.md                     # This file
```

---

## 🌐 Deployment

The app is ready for deployment to various platforms. See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

**Recommended Platforms:**
- **Render** - Free tier available (auto-sleep after inactivity)
- **Fly.io** - Free tier with persistent storage
- **PythonAnywhere** - Free tier with subdomain

**Deployment Files:**
- `Procfile` - Production server configuration (gunicorn)
- `runtime.txt` - Python version specification
- Production-ready `app.py` with environment variable support

---

## 🎨 Features

- **Modern UI**: Professional glassmorphism design with smooth animations
- **Real ML Model**: Trained logistic regression with 79%+ accuracy
- **Interactive Form**: User-friendly interface with dropdowns and tooltips
- **Risk Probability**: Visual probability gauge showing prediction confidence
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile

---

## 🛠️ Technology Stack

- **Backend**: Flask (Python)
- **ML Framework**: scikit-learn
- **Data Processing**: pandas, numpy
- **Frontend**: HTML5, CSS3, JavaScript
- **Icons**: Font Awesome
- **Production Server**: Gunicorn

---

## 📝 Git Usage

Initialize and commit your project:
```bash
git init
git add .
git commit -m "Initial commit: flood model web app"
```

---

## 📄 License

This project is for educational/academic purposes.
