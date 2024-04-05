from flask import Flask, request, jsonify

from ai.src.api.generator_handler import generate_sheets

app = Flask(__name__)


@app.route('/get_data', methods=['POST'])
def get_data():
    file_data = request.get_json()

    generate_sheets(file_data)

    return jsonify({'message': 'JSON file processed successfully'})


if __name__ == '__main__':
    app.run(debug=True)
