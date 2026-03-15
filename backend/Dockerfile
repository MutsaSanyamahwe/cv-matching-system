
FROM python:3.11

# Setting working directory inside container
WORKDIR /app


COPY requirements.txt .

# Upgrading pip
RUN pip install --no-cache-dir --upgrade pip setuptools wheel



# installing the rest of your requirements
RUN pip install --no-cache-dir -r requirements.txt

# install spacy model
RUN python -m spacy download en_core_web_sm

# Download NLTK data during build
RUN python -m nltk.downloader stopwords wordnet



# Copying backend code
COPY ./src ./src

# Copying the pickle file into /app
COPY tfidf_vectorizer.pkl ./tfidf_vectorizer.pkl

# Expose API port
EXPOSE 8000

# Running the FastAPI app
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "10000"]
