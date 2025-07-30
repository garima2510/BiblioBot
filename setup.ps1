# BiblioBot Setup Script

Write-Host "Setting up BiblioBot..." -ForegroundColor Green

# Create virtual environment
Write-Host "Creating virtual environment..." -ForegroundColor Yellow
python -m venv venv

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
.\venv\Scripts\activate

# Install dependencies
Write-Host "Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

# Copy environment template
if (-not (Test-Path ".env")) {
    Write-Host "Creating .env file from template..." -ForegroundColor Yellow
    Copy-Item ".env.template" ".env"
    Write-Host "Please edit .env file with your API keys!" -ForegroundColor Red
} else {
    Write-Host ".env file already exists" -ForegroundColor Green
}

Write-Host "Setup complete! Run 'streamlit run app.py' to start the application." -ForegroundColor Green
Write-Host "Don't forget to configure your API keys in the .env file!" -ForegroundColor Yellow
