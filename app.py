from flask import Flask, request, jsonify
import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set OpenAI API Key (Loaded from .env)
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

# Home Route
@app.route('/')
def home():
    return "Clay Backend is Running!"

# Upload Resume Endpoint (Fixed: No Duplicate)
@app.route('/upload_resume', methods=['POST'])
def upload_resume():
    print("📥 Received request on /upload_resume")

    if 'resume' not in request.files:
        print("❌ No resume file provided")
        return jsonify({"error": "No resume file provided"}), 400

    resume_file = request.files['resume']
    resume_text = resume_file.read().decode("utf-8")  # Read resume content

    print("✅ Resume uploaded successfully!")
    print("📄 Resume Content:", resume_text)

    return jsonify({"message": "Resume uploaded successfully", "resume_text": resume_text})

# Submit Job Description Endpoint
@app.route('/submit_job', methods=['POST'])
def submit_job():
    print("📥 Received request on /submit_job")
    
    data = request.get_json()
    job_description = data.get('job_description', '')

    if not job_description:
        print("❌ No job description provided")
        return jsonify({"error": "Job description is required"}), 400

    print("✅ Job description received:", job_description)
    return jsonify({"message": "Job description received", "job_description": job_description})

# Generate Resume Endpoint
@app.route('/generate_resume', methods=['POST'])
def generate_resume():
    print("📥 Received request on /generate_resume")

    data = request.get_json()
    resume_text = data.get('resume_text', '')
    job_description = data.get('job_description', '')

    if not resume_text or not job_description:
        print("❌ Missing resume text or job description")
        return jsonify({"error": "Both resume text and job description are required"}), 400

    # Construct prompt for OpenAI
    prompt = f"Revise the following resume to better match the job description provided:\n\nJob Description:\n{job_description}\n\nResume:\n{resume_text}\n\nOptimized Resume:"

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )

    generated_resume = response["choices"][0]["message"]["content"]

    print("✅ Resume generated successfully!")
    return jsonify({"generated_resume": generated_resume})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)  # Change port to 5001
