import os
import sys
import zipfile
from flask import Flask, request, jsonify, send_file
from pymongo import MongoClient

#  Add the parent directory to the path
sys.path.append(os.path.join(os.getcwd(), ".."))

from ai.src.generator.generator_handler import generate_sheets
from ai.src.evaluator.preprocessor import preprocess_image


#  Initialize the Flask app
app = Flask(__name__)
uri = "mongodb://localhost:27017"
# Connect to MongoDB
client = MongoClient(uri)
db = client['adt']
collection = db['quizes']


def catch_errors(func):
    """
    Catch errors in the function and return a JSON response
    :param func: Function to be wrapped
    :return: Wrapped function
    """
    def wrapper(*args, **kwargs):
        """
        Wrapper function
        :param args: Arguments
        :param kwargs: Keyword arguments
        :return: JSON response
        """
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return jsonify({'error': f'An error occurred: {e}'}), 500
    return wrapper


@app.route('/healthcheck', methods=['GET'])
def healthcheck():
    return jsonify({'status': 'OK'})


@app.route('/get_print_data', methods=['POST'])
def get_data():
    """
    Get the data from the request and generate the bubble sheets and question papers
    :return: ZIP file containing the generated PDFs
    """
    def inner_func():
        data = request.get_json()

        questions = data["questions"]
        students = data["students"]
        generate_sheets(collection, questions, students)

        pdf_files = ["generated_pdfs/bubble_sheets.pdf", "generated_pdfs/question_papers.pdf"]
        zip_file = os.path.join(os.getcwd(), "generated_pdfs/pdfs.zip")

        # Create a zip file containing the PDF files
        with zipfile.ZipFile(zip_file, 'w') as zipf:
            for pdf_file in pdf_files:
                zipf.write(pdf_file, arcname=os.path.basename(pdf_file))

        return send_file(zip_file, as_attachment=True)

    return catch_errors(inner_func)()


@app.route('/test_evaluation', methods=['POST'])
def evaluate_answers():
    """
    Evaluate the answers from the PDF
    :return: JSON response containing the student ID and answers
    """
    if not request.data:
        return jsonify({'error': 'No file part'})

    def inner_func():
        file_data = request.data

        with open('temp.pdf', 'wb') as fp:
            fp.write(file_data)

        # Extract text from the PDF
        json_data = preprocess_image(collection, "temp.pdf")
        os.remove("temp.pdf")

        return jsonify(json_data)

    return catch_errors(inner_func)()


if __name__ == '__main__':
    # Create the directory for the generated PDFs if it does not exist
    if not os.path.exists("generated_pdfs"):
        os.makedirs("generated_pdfs")

    if os.environ.get('ENV') == 'production':
        app.run(host='0.0.0.0', port=8081)
    else:
        app.run(debug=True)