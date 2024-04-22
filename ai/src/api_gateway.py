import os
import zipfile
from flask import Flask, request, jsonify, send_file

from generator_handler import generate_sheets
from preprocessor import preprocess_image

app = Flask(__name__)


@app.route('/get_print_data', methods=['POST'])
def get_data():
    file_data = request.get_json()
    generate_sheets(file_data)

    try:
        pdf_files =["generated_pdfs/bubble_sheets.pdf", "generated_pdfs/question_papers.pdf"]
        zip_file = os.path.join(os.getcwd(), "generated_pdfs/pdfs.zip")

        # Create a zip file containing the PDF files
        with zipfile.ZipFile(zip_file, 'w') as zipf:
            for pdf_file in pdf_files:
                zipf.write(pdf_file, arcname=os.path.basename(pdf_file))

        return send_file(zip_file, as_attachment=True)

    except Exception as e:
        return jsonify({'error': f'An error occurred: {e}'})


@app.route('/test_evaluation', methods=['POST'])
def evaluate_answers():
    if not request.data:
        return jsonify({'error': 'No file part'})

    file_data = request.data

    with open('temp.pdf', 'wb') as fp:
        fp.write(file_data)

    # Extract text from the PDF
    json_data = preprocess_image("temp.pdf")
    os.remove("temp.pdf")

    return jsonify(json_data)


if __name__ == '__main__':
    app.run(debug=True)
