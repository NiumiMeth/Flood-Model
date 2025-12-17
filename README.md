# Flood Risk Prediction Web App

This project is a simple Flask web application that serves a machine learning model to predict flood risk based on catchment and rainfall characteristics.

## Project Structure

- **app.py**: Main Flask application that loads the dataset, trains the model pipeline, and serves the web UI.
- **data/**:
  - **data.csv**: Input dataset used for training and for populating form dropdown options.
- **notebooks/**:
  - **flood_EDA.ipynb**: Exploratory data analysis notebook.
  - **Model.ipynb**: Model development and experimentation notebook.
- **templates/**:
  - **index.html**: HTML template for the main web page.
- **static/**:
  - **style.css**: CSS styling for the web interface.
- **requirements.txt**: Python dependencies for running the project.
- **.gitignore**: Files and folders that should be ignored by Git.

## Setup and Installation

1. **Create and activate a virtual environment (recommended)**  
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # source venv/bin/activate  # macOS / Linux
   ```

2. **Install dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Flask app**  
   ```bash
   python app.py
   ```

4. Open your browser and navigate to `http://127.0.0.1:5000/` to use the app.

## Deployment

This app is ready for deployment to various platforms. See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions.

**Quick Deploy Options:**
- **Railway** (Recommended) - Easy setup, free tier available
- **Render** - Free tier with auto-sleep
- **Fly.io** - Free tier available
- **PythonAnywhere** - Free tier available

The app includes:
- ✅ `Procfile` for production server (gunicorn)
- ✅ `runtime.txt` for Python version
- ✅ Production-ready configuration
- ✅ All dependencies in `requirements.txt`

## Git Usage

Once this structure is in place, you can initialize a Git repository and make your first commit:

```bash
git init
git add .
git commit -m "Initial commit: flood model web app"
```

## Features

- 🎨 **Modern, Professional UI** - Beautiful glassmorphism design with smooth animations
- 🤖 **Real ML Model** - Trained logistic regression model using scikit-learn
- 📊 **Interactive Form** - Easy-to-use form with dropdowns and tooltips
- 📈 **Risk Probability** - Visual probability gauge with detailed results
- 📱 **Responsive Design** - Works on desktop, tablet, and mobile devices
- ⚡ **Fast Predictions** - Real-time flood risk assessment

## Technology Stack

- **Backend**: Flask (Python)
- **ML Framework**: scikit-learn
- **Frontend**: HTML5, CSS3, JavaScript
- **Icons**: Font Awesome
- **Production Server**: Gunicorn


