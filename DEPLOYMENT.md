# Deployment Guide for Flood Risk Prediction App

This guide will help you deploy your Flask flood prediction web app to various platforms.

## Prerequisites

1. **Git Repository**: Make sure your code is in a Git repository
2. **Data File**: Ensure `data/data.csv` is committed to your repository (it's needed for the model)
3. **Dependencies**: All dependencies are listed in `requirements.txt`

## Deployment Options

### Option 1: Railway (Recommended - Easy & Free Tier Available)

1. **Sign up** at [railway.app](https://railway.app)
2. **Create a new project** → "Deploy from GitHub repo"
3. **Connect your GitHub repository**
4. **Railway will automatically detect**:
   - Python project
   - `Procfile` for the web process
   - `requirements.txt` for dependencies
5. **Set environment variables** (optional):
   - `FLASK_DEBUG=False` (for production)
   - `PORT` (automatically set by Railway)
6. **Deploy** - Railway will build and deploy automatically
7. **Get your URL** - Railway provides a public URL

**Railway Free Tier**: 500 hours/month, $5 credit

---

### Option 2: Render (Free Tier Available)

1. **Sign up** at [render.com](https://render.com)
2. **Create a new Web Service**
3. **Connect your GitHub repository**
4. **Configure**:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Environment**: Python 3
5. **Set environment variables**:
   - `PYTHON_VERSION=3.12.0`
6. **Deploy** - Render will build and deploy
7. **Get your URL** - Render provides a `.onrender.com` URL

**Render Free Tier**: Spins down after 15 min of inactivity (takes ~30s to wake up)

---

### Option 3: Heroku (Paid - $5/month minimum)

1. **Install Heroku CLI**: [devcenter.heroku.com/articles/heroku-cli](https://devcenter.heroku.com/articles/heroku-cli)
2. **Login**: `heroku login`
3. **Create app**: `heroku create your-app-name`
4. **Deploy**: 
   ```bash
   git push heroku main
   ```
5. **Open**: `heroku open`

**Note**: Heroku removed their free tier, so this requires a paid plan.

---

### Option 4: PythonAnywhere (Free Tier Available)

1. **Sign up** at [pythonanywhere.com](https://www.pythonanywhere.com)
2. **Upload your files** via Files tab
3. **Create a Web App**:
   - Choose "Manual configuration"
   - Python 3.12
4. **Edit WSGI file**:
   ```python
   import sys
   path = '/home/yourusername/flood-model'
   if path not in sys.path:
       sys.path.append(path)
   
   from app import app as application
   ```
5. **Reload** the web app

**PythonAnywhere Free Tier**: Limited to 1 web app, must be accessed via their subdomain

---

### Option 5: Fly.io (Free Tier Available)

1. **Install Fly CLI**: [fly.io/docs/getting-started/installing-flyctl](https://fly.io/docs/getting-started/installing-flyctl)
2. **Login**: `fly auth login`
3. **Initialize**: `fly launch` (in your project directory)
4. **Deploy**: `fly deploy`

**Fly.io Free Tier**: 3 shared-cpu VMs, 3GB persistent storage

---

## Pre-Deployment Checklist

- [x] `requirements.txt` includes all dependencies
- [x] `Procfile` is created for gunicorn
- [x] `runtime.txt` specifies Python version
- [x] `data/data.csv` is committed to repository
- [x] Debug mode is disabled in production (handled by environment variable)
- [x] `.gitignore` is properly configured

## Environment Variables

You can set these in your deployment platform's dashboard:

- `FLASK_DEBUG=False` - Disables debug mode (important for production)
- `PORT` - Usually set automatically by the platform
- `PYTHON_VERSION=3.12.0` - Some platforms need this

## Testing Locally Before Deployment

1. **Install gunicorn**: `pip install gunicorn`
2. **Test production server**:
   ```bash
   gunicorn app:app
   ```
3. **Visit**: `http://localhost:8000`

## Troubleshooting

### Issue: App crashes on startup
- **Check**: Make sure `data/data.csv` exists in your repository
- **Check**: All dependencies in `requirements.txt` are correct

### Issue: Model training takes too long
- **Solution**: The model trains on startup. For faster startup, consider:
  - Using a smaller dataset for testing
  - Pre-training and saving the model (advanced)

### Issue: Static files not loading
- **Check**: Flask automatically serves files from `static/` folder
- **Check**: CSS/JS file paths in HTML are correct

### Issue: Port binding error
- **Solution**: The app now uses `PORT` environment variable automatically

## Post-Deployment

1. **Test your deployed app** - Make sure all features work
2. **Monitor logs** - Check for any errors
3. **Update README** - Add your deployment URL
4. **Share your app** - Your flood prediction model is now live! 🌊

## Need Help?

- Check platform-specific documentation
- Review Flask deployment guides
- Check application logs in your platform's dashboard

