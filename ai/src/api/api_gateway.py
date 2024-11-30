import os
import sys
import zipfile
from flask import Flask, request, jsonify, send_file
from pymongo import MongoClient

#  Add the parent directory to the path
sys.path.append(os.path.join(os.getcwd(), ".."))

from ai.src.generator.generator_handler import generate_sheets
from ai.src.evaluator.preprocessor import map_pages_to_students, preprocess_image, create_temp_pdfs
from ai.src.evaluator.evaluator import transform_eval_output


#  Initialize the Flask app
app = Flask(__name__)

mongo_service_port, mongo_service_host = None, None
if os.environ.get('ENV') == 'production':
    mongo_service_port = os.environ.get('MONGO_DB_PORT')
    mongo_service_host = os.environ.get('MONGO_DB_HOST')
    if mongo_service_port is None or mongo_service_host is None:
        raise ValueError("MongoDB service host and port must be defined in the environment variables.")
else:
    mongo_service_port = 27017
    mongo_service_host = 'localhost'
uri = f"mongodb://{mongo_service_host}:{mongo_service_port}"

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
            print(f'An error occurred: {e}')
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
        date = data["date"]

        # ISO string date to DD.MM.YYYY
        date = date.split("T")[0].split("-")
        date = f"{date[2]}. {date[1]}. {date[0]}"

        generate_sheets(collection, questions, students, date)

        pdf_files = ["generated_pdfs/bubble_sheets.pdf", "generated_pdfs/question_papers.pdf"]
        zip_file = os.path.join(os.getcwd(), "generated_pdfs/pdfs.zip")

        # Create a zip file containing the PDF files
        with zipfile.ZipFile(zip_file, 'w') as zipf:
            for pdf_file in pdf_files:
                zipf.write(pdf_file, arcname=os.path.basename(pdf_file))

        return send_file(zip_file, as_attachment=True)

    return catch_errors(inner_func)()


@app.route("/generate-gf-data", methods=["POST"])
def generate_gc_data():
    """
    Get the data from the request and generate the bubble sheets and question papers
    :return: ZIP file containing the generated PDFs
    """
    def inner_func():
        data = request.get_json()

        questions = data["questions"]
        students = data["students"]
        date = data["date"]

        # ISO string date to DD.MM.YYYY
        date = date.split("T")[0].split("-")
        date = f"{date[2]}. {date[1]}. {date[0]}"

        # Preprocess the questions so they match the expected format from Moodle -- we can call our Moodle functions
        for question in questions:
            # GC questions do not have a name
            question["name"] = [""]
            # GC calls it points, Moodle calls it defaultGrade
            question["defaultGrade"] = question["points"]
            # GC does not have a penalty
            question["penalty"] = 0

            # GC does not have answer fractions, let's make them uniformly
            answers = question["answers"]
            correct_answers = 0
            wrong_answers = 0
            for answer in answers:
                if answer["isCorrect"]:
                    correct_answers += 1
                else:
                    wrong_answers += 1

            for answer in answers:
                # GC calls it value, Moodle calls it text
                answer["text"] = answer["value"]
                # Made up uniform fractions for correct and wrong answers
                answer["fraction"] = 1 / correct_answers if answer["isCorrect"] else -1 / wrong_answers
                answer["fraction"] *= 100  # Moodle gives the fractions as percentages

        # Generate the bubble sheets and question papers as if Moodle export
        generate_sheets(collection, questions, students, date)

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
        student_page_ids, test_id = map_pages_to_students(collection, "temp.pdf")
        # If the none of the QR codes worked (could not read the test ID), return an error
        if student_page_ids is None:
            return jsonify({"error": "Error reading the QR codes. Please try again."})
        pdf_names = create_temp_pdfs(student_page_ids, "temp.pdf")
        os.remove("temp.pdf")

        result = []
        logs = []
        for i, pdf in enumerate(pdf_names):
            # Preprocess the image and get the evaluation output
            json_data = preprocess_image(collection, pdf, test_id)

            # Transform the output to a Moodle happy output
            db_data = collection.find_one({"test_id": test_id})
            student_result, student_log = transform_eval_output(json_data, db_data)

            # Skip if the student was not found in the database (most likely due to bad ID detection)
            if student_result is None:
                err_msg = f"ERROR: Evaluation failed on page {i + 1}! Student with {json_data['student_id']} ID not found in the database! (ID detection failed)"
                err_dict = {"error": err_msg, "result": []}
                result.append(err_dict)
                logs.append(err_msg)
                os.remove(pdf)
                continue

            result.append(student_result)
            logs.append(student_log)

            os.remove(pdf)

        log = "\n".join(logs)

        return jsonify({"result": result, "log": log})

    return catch_errors(inner_func)()


if __name__ == '__main__':
    # Create the directory for the generated PDFs if it does not exist
    if not os.path.exists("generated_pdfs"):
        os.makedirs("generated_pdfs")

    if os.environ.get('ENV') == 'production':
        app.run(host='0.0.0.0', port=8081)
    else:
        app.run(debug=True)
