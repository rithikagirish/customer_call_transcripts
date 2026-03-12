# ==============================
# CALL CENTER TRANSCRIPT PREPROCESSING
# ==============================

import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')

# ==============================
# LOAD DATASET
# ==============================

df = pd.read_csv("call_recordings.csv")


TRANSCRIPT_COLUMN = "Transcript"

# ==============================
# PREPROCESSING SETUP
# ==============================

stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

fillers = {
    "um", "uh", "hmm", "you know", "like",
    "okay", "ok", "right", "actually", "basically"
}

# ==============================
# PREPROCESSING FUNCTIONS
# ==============================

def remove_timestamps(text):
    return re.sub(r"\[\d{2}:\d{2}:\d{2}\]", " ", str(text))

def remove_speaker_labels(text):
    return re.sub(r"(agent|customer|speaker\s*\d+):", " ", text, flags=re.IGNORECASE)

def extract_customer_only(text):
    lines = text.split("\n")
    customer_lines = []

    for line in lines:
        if "customer:" in line.lower():
            customer_lines.append(line.split(":", 1)[1])

    return " ".join(customer_lines) if customer_lines else text

def remove_pii(text):
    text = re.sub(r"\S+@\S+", " EMAIL ", text)       # emails
    text = re.sub(r"\b\d{10}\b", " PHONE ", text)    # phone numbers
    text = re.sub(r"\b\d+\b", " NUMBER ", text)      # other numbers
    return text

def remove_fillers(text):
    for filler in fillers:
        text = text.replace(filler, " ")
    return text

def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-z\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def tokenize_lemmatize(text):
    words = text.split()
    processed = [
        lemmatizer.lemmatize(word)
        for word in words
        if word not in stop_words
    ]
    return " ".join(processed)

# ==============================
# COMPLETE PIPELINE FUNCTION
# ==============================

def preprocess_transcript(transcript):

    text = extract_customer_only(transcript)
    text = remove_timestamps(text)
    text = remove_speaker_labels(text)
    text = remove_pii(text)
    text = remove_fillers(text)
    text = clean_text(text)
    text = tokenize_lemmatize(text)

    return text

# ==============================
# APPLY TO DATASET
# ==============================

df["cleaned_text"] = df[TRANSCRIPT_COLUMN].apply(preprocess_transcript)

# ==============================
# SAVE CLEANED DATASET
# ==============================

df.to_csv("cleaned_customer_calls.csv", index=False)

print("Preprocessing complete ✅")
print(df[["cleaned_text"]].head())
