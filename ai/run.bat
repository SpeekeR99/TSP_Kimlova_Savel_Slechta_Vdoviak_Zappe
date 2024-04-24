:: Create generated_pdfs directory if it doesn't exist
if not exist generated_pdfs mkdir generated_pdfs

:: Create a virtual environment
python -m venv venv

:: Activate the virtual environment
call venv/Scripts/activate

:: Install the required packages
pip install -r requirements.txt

:: Run the app (API)
python src/api_gateway.py