# NLTK, spaCy, Transformers (sentimentos)

import nltk
import spacy
from nltk.corpus import stopwords
from transformers import pipeline
from datetime import datetime

# Carrega recursos
_nlp = spacy.load("pt_core_news_sm")
_stop = set(stopwords.words("portuguese"))

# pipeline de sentimento (modelo pt-br)
_sentiment = pipeline("sentiment-analysis", 
model="nlptown/bert-base-multilingual-uncased-sentiment")

# Normaliza o texto de entrada usando o modelo de linguagem spaCy.
def normalize(text: str) -> str:
    doc = _nlp(text)
    tokens = [t.lemma_.lower() for t in doc if t.is_alpha and t.lemma_.lower() not in _stop]
    return " ".join(tokens)

# Retorna o objeto 'Doc' do spaCy, gerado a partir do texto de entrada.
def spacy_doc(text: str):
    return _nlp(text)

def analyze_sentiment(text: str) -> str:
    try:
        res = _sentiment(text[:512])[0]  # corta prompts muito longos
        # nlptown retorna labels como "1 star"..."5 stars"
        label = res.get("label", "")
        score = res.get("score", 0.0)
        return f"{label} ({score:.2f})"
    except Exception as e:
        return "unknown/desconhecido"
