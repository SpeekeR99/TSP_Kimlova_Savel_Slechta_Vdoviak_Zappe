:: Create a virtual environment
python -m venv venv

:: Activate the virtual environment
call venv/Scripts/activate

:: Install the required packages
pip install -r requirements.txt

:: Run the app (API)
python src/api/api_gateway.py