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

## Git Usage

Once this structure is in place, you can initialize a Git repository and make your first commit:

```bash
git init
git add .
git commit -m "Initial commit: flood model web app"
```


