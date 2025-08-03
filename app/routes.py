from flask import Blueprint, render_template, request, redirect, flash
import os
import fitz  # PyMuPDF

main = Blueprint('main', __name__)

def extract_questions_from_pdf(pdf_path):
    questions = []
    try:
        doc = fitz.open(pdf_path)
        for page in doc:
            text = page.get_text()
            questions.append(text)
    except Exception as e:
        print("Error:", e)
    return questions

@main.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        uploaded_file = request.files['pdf']
        if uploaded_file and uploaded_file.filename.endswith('.pdf'):
            filepath = os.path.join('uploads', uploaded_file.filename)
            os.makedirs('uploads', exist_ok=True)
            uploaded_file.save(filepath)
            questions = extract_questions_from_pdf(filepath)
            flash('PDF Processed Successfully!', 'success')
            return render_template('index.html', questions=questions)
        else:
            flash('Invalid file format. Please upload a PDF.', 'danger')
    return render_template('index.html')
