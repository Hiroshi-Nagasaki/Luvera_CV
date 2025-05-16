from flask import Flask, request, send_file
import openai
import pdfplumber
from fpdf import FPDF
import io
import os

app = Flask(__name__)

openai.api_key = os.getenv("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")

@app.route("/")
def home():
    return "Luvera CV Review backend is running."

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files['cv']
    with pdfplumber.open(file) as pdf:
        resume_text = "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())
@app.route("/upload", methods=["POST"])
def upload():
    file = request.files['cv']
    ...
    response = openai.ChatCompletion.create(...)  # this is where it fails if key is bad

    prompt = f"""You're an expert resume reviewer. Analyze this CV and give:
1. Strengths
2. Weaknesses
3. ATS compatibility
4. Suggestions
5. Sample bullet rewrites

CV:
\"\"\"
{resume_text}
\"\"\"
"""

    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You're an expert career coach."},
            {"role": "user", "content": prompt}
        ]
    )
    feedback = response.choices[0].message.content

    pdf_report = FPDF()
    pdf_report.add_page()
    pdf_report.set_font("Arial", size=12)
    for line in feedback.split('\n'):
        pdf_report.multi_cell(0, 10, line)
    output = io.BytesIO()
    pdf_report.output(output)
    output.seek(0)

    return send_file(output, as_attachment=True, download_name="Luvera_CV_Review_Report.pdf")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
