Write-Host ""
Write-Host "============================================"
Write-Host " Blood Donor Intelligence System Setup"
Write-Host "============================================"
Write-Host ""

# ---------------------------------------------
# Check Python
# ---------------------------------------------

Write-Host "Checking Python..."

python --version

if ($LASTEXITCODE -ne 0) {

    Write-Host ""
    Write-Host "ERROR: Python is not installed or not in PATH."
    Write-Host "Please install Python 3.11+ and try again."

    exit 1
}

# ---------------------------------------------
# Create virtual environment
# ---------------------------------------------

if (!(Test-Path "venv")) {

    Write-Host ""
    Write-Host "Creating virtual environment..."

    python -m venv venv

    if ($LASTEXITCODE -ne 0) {

        Write-Host "ERROR: Could not create virtual environment."
        exit 1
    }

}
else {

    Write-Host ""
    Write-Host "Virtual environment already exists."

}

# ---------------------------------------------
# Upgrade pip
# ---------------------------------------------

Write-Host ""
Write-Host "Updating pip..."

.\venv\Scripts\python.exe -m pip install --upgrade pip

# ---------------------------------------------
# Install dependencies
# ---------------------------------------------

Write-Host ""
Write-Host "Installing project dependencies..."

.\venv\Scripts\python.exe -m pip install -r requirements.txt

if ($LASTEXITCODE -ne 0) {

    Write-Host ""
    Write-Host "ERROR: Dependency installation failed."

    exit 1
}

# ---------------------------------------------
# Load historical demand data
# ---------------------------------------------

Write-Host ""
Write-Host "Loading historical demand data..."

.\venv\Scripts\python.exe -m app.ml.load_demand_data

if ($LASTEXITCODE -ne 0) {

    Write-Host ""
    Write-Host "ERROR: Demand data loading failed."

    exit 1
}

# ---------------------------------------------
# Train ML model
# ---------------------------------------------

Write-Host ""
Write-Host "Training machine learning model..."

.\venv\Scripts\python.exe -m app.ml.train

if ($LASTEXITCODE -ne 0) {

    Write-Host ""
    Write-Host "ERROR: ML model training failed."

    exit 1
}

# ---------------------------------------------
# Create demo data
# ---------------------------------------------

Write-Host ""
Write-Host "Creating demonstration data..."

.\venv\Scripts\python.exe -m app.ml.seed_demo_data

if ($LASTEXITCODE -ne 0) {

    Write-Host ""
    Write-Host "ERROR: Demo data creation failed."

    exit 1
}

# ---------------------------------------------
# Setup complete
# ---------------------------------------------

Write-Host ""
Write-Host "============================================"
Write-Host " SETUP COMPLETED SUCCESSFULLY"
Write-Host "============================================"
Write-Host ""

Write-Host "To start the application:"
Write-Host ""
Write-Host "  .\run_project.bat"
Write-Host ""

Write-Host "FastAPI:"
Write-Host "  http://127.0.0.1:8000"
Write-Host ""

Write-Host "Swagger:"
Write-Host "  http://127.0.0.1:8000/docs"
Write-Host ""

Write-Host "Dashboard:"
Write-Host "  http://localhost:8501"
Write-Host ""