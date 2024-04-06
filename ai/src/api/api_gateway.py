from flask import Flask, request, jsonify

from ai.src.generator_handler import generate_sheets

app = Flask(__name__)


@app.route('/get_print_data', methods=['POST'])
def get_data():
    file_data = request.get_json()
    generate_sheets(file_data)
    return jsonify({'message': 'JSON file processed successfully'})


@app.route('/test_evaluation', methods=['POST'])
def evaluate_answers():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if file and file.filename.endswith('.pdf'):
        file.save('naskenovane.pdf')

        # Extract text from the PDF

        # Convert text to JSON
        json_data = {'text': 'answers'}

        return jsonify(json_data)
    else:
        return jsonify({'error': 'Invalid file format. Please upload a PDF file'})


if __name__ == '__main__':
    app.run(debug=True)
