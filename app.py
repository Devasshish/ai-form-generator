from flask import Flask, request, jsonify, render_template
from google_form_generator import process_pdf_and_create_form

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/generate-form', methods=['POST'])
def generate_form():
    pdf_file = request.files['pdf']
    if not pdf_file:
        return jsonify({'error': 'No file provided'}), 400

    # Save the PDF temporarily
    pdf_path = "temp_uploaded_file.pdf"
    pdf_file.save(pdf_path)

    try:
        form_url = process_pdf_and_create_form(pdf_path)
        return jsonify({'form_url': form_url})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
