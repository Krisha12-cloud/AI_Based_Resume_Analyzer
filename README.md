# AI_Based_Resume_Analyzer
Developed an AI-based resume analyzer using NLP to extract and process candidate information from PDFs. Built a job category prediction model using TF-IDF and ML algorithms, and implemented semantic skill matching to compare resumes with job descriptions and recommend relevant courses.

# Problem Statement

Recruiters and job seekers often face challenges in:

Manually analyzing large volumes of resumes
Identifying relevant skills and job roles.
Understanding gaps between candidate profiles and job requirements

This project addresses these challenges by automating resume parsing, classification, and skill analysis.

# Key Features

📄 Resume Parsing: Extracts text and structured details from PDF resumes

🧩 Information Extraction: Identifies name, email, phone number, and skills

📊 Job Category Prediction: Classifies resumes into job roles using ML models

🔍 Resume–JD Matching: Compares resumes with job descriptions

⚠️ Skill Gap Analysis: Detects missing and matched skills

🎓 Course Recommendations: Suggests courses based on missing skills

# How It Works (System Pipeline)
1. Text Extraction : 
Extracts raw text from PDF resumes using PDF processing tools
2. Preprocessing : 
Cleans and normalizes text (removes noise, formatting issues)
3. Information Extraction : 
Uses NLP and pattern-based methods to extract:
Personal details,
Skills,
Section-wise data
4. Feature Engineering : 
Converts textual data into numerical format using TF-IDF
5. Job Category Prediction : 
Applies machine learning models to classify resumes into job categories
6. Skill Matching : 
Performs
Exact matching (direct comparison) and 
Semantic matching (understanding similar skills)
7. Gap Analysis : 
Identifies missing skills required for a specific job role
8. Course Recommendation :
Maps missing skills to relevant courses from a dataset

# Tech Stack

### Programming

Python

### NLP & Text Processing

spaCy

Regex

### Machine Learning

Scikit-learn (Logistic Regression, XgBoost, Gradient Boosting)

### Feature Engineering

TF-IDF Vectorization

Semantic Matching

Sentence Transformers (all-MiniLM-L6-v2)

### Data Processing

Pandas, NumPy

### PDF Processing

PDFMiner

### Interface (Optional)

Streamlit

# How to Run
### Clone the repository
git clone <repo-link>


### Install dependencies
pip install -r requirements.txt

### Run the application
streamlit run app.py

# Authors:
### Krisha Doshi,Hely Vachhani
