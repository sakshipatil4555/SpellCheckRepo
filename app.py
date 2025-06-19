from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
import fitz  # PyMuPDF
from spellchecker import SpellChecker
import os

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def extract_text_from_pdf(file_path):
    doc = fitz.open(file_path)
    all_text = ""
    for page in doc:
        all_text += page.get_text()
    return all_text


def spell_check_text(text):
    spell = SpellChecker()
    words = text.split()
    misspelled = spell.unknown(words)
    results = {}
    for word in misspelled:
        results[word] = list(spell.candidates(word))
    return results


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "pdf_file" not in request.files:
            return "No file uploaded"

        file = request.files["pdf_file"]
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(file_path)

        text = extract_text_from_pdf(file_path)
        misspellings = spell_check_text(text)

        return render_template("result.html", misspellings=misspellings, extracted=text)

    return render_template("index.html")
