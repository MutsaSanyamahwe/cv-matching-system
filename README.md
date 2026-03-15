# AI-Powered CV & Job Description Matching System

## Overview
This project is an AI-powered system designed to analyze CVs and job descriptions and provide a fit score indicating how well a candidate matches a job. It combines text processing, NLP, and machine learning techniques to extract skills, compare semantic content, and identify gaps in qualifications.
The system is built to demonstrate a real-world application of AI in recruitment automation while being scalable and deployable.

**Important** This system is not 100% accurate. AI can identify explicit skills and patterns, but implicit experience, context, and nuanced soft skills may not always be detected. It is mean to only be a supportive tool and accuracy depends on the quality of the CV and job description.
**Model may underperform for highly specialized or niche domains unless dictionaries are updated.**

### Try the deployed version: [CV Matcher](https://cv-ai-matching-system.onrender.com/)

## Flow of the system
![Workflow Diagram](/frontend/cv-matcher-frontend/public/images/flowdiagram.png)

## Features

- Skill Extraction: Uses POS tagging, NER, and domain-specific dictionaries.
- Semantic Matching: Uses TF-IDF vectorizer for text similarity scoring.
- Match & Gap Analysis: Clearly shows matched vs missing skills.
- PDF Input: Supports CVs in PDF format.
- Deployable: Runs via FastAPI backend and Docker container.

## Tech Stack

- Python 3.11
- FastAPI – API backend
- spaCy – NLP (POS tagging, NER)
- scikit-learn – TF-IDF vectorization & cosine similarity
- NLTK – Text preprocessing
- Docker – Containerized deployment
- Pickle – Stores pre-trained TF-IDF model
- React (Vite)

## Methodology

1. Text Extraction & Cleaning: Converts PDFs to text, removes punctuation, stopwords, and noise words.
2. Skill Extraction:
- Identifies nouns, proper nouns, and named entities
- Matches domain-specific and soft skills

3. Similarity Calculation: TF-IDF vectorization + cosine similarity.

4. Scoring:

- 70% weight: Skill match

- 30% weight: Semantic similarity

- Output: Fit score, matched skills, missing skills.

## Limitations

- AI cannot perfectly interpret implicit skills or experience not explicitly stated.
- Accuracy depends on the quality of CVs and job descriptions.
- Soft skills detection is limited to keywords; nuanced evaluation is human-dependent.
- Model may underperform for highly specialized or niche domains unless dictionaries are updated.

## Future Improvements
- Integrate transformer-based embeddings (e.g., Sentence-BERT) for better semantic matching.
- Expand domain skill dictionaries for niche industries.

## How to run locally
### Clone the repo
```bash
git clone https://github.com/MutsaSanyamahwe/cv-matching-system
cd cv-matcher/backend
pip install -r requirements.txt
```
**Run locally** 
```bash
uvicorn src.main:app --host 0.0.0.0 --port 10000
```
**Run via docker**
```bash
docker build -t cv-matcher-backend .
docker run -p 8000:10000 cv-matcher-backend
```
## Contributing

Feel free to submit issues or pull requests. Make sure to update documentation and add tests where necessary.

## License

This project is licensed under MIT License.

> **⚠ Note:** This system is not 100% accurate. It identifies explicit skills and patterns but may miss implicit skills, context, or niche domain expertise. Use as a supportive tool, not a final decision-maker.

![Python](https://img.shields.io/badge/python-3.11-blue)
![License](https://img.shields.io/badge/license-MIT-green)


