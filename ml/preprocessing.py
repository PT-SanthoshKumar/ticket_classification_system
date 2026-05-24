import re
import string

try:
    from nltk.corpus import stopwords
    from nltk.stem import WordNetLemmatizer
    from nltk.tokenize import word_tokenize
except Exception:
    stopwords = None
    WordNetLemmatizer = None
    word_tokenize = None


FALLBACK_STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "but", "by", "can", "for",
    "from", "has", "have", "how", "i", "in", "is", "it", "my", "of", "on",
    "or", "our", "please", "the", "this", "to", "was", "we", "what", "where",
    "with", "your"
}


def _load_stopwords():
    if stopwords is None:
        return FALLBACK_STOPWORDS
    try:
        return set(stopwords.words("english"))
    except LookupError:
        return FALLBACK_STOPWORDS


def _tokenize(text):
    if word_tokenize is not None:
        try:
            return word_tokenize(text)
        except LookupError:
            pass
    return re.findall(r"[a-z]+", text)


def clean_text(text):
    """Normalize, tokenize, remove stopwords, and lemmatize a ticket."""
    text = str(text).lower()
    text = re.sub(r"http\S+|www\.\S+", " ", text)
    text = re.sub(r"\d+", " ", text)
    text = text.translate(str.maketrans("", "", string.punctuation))
    tokens = _tokenize(text)
    stop_words = _load_stopwords()

    lemmatizer = None
    if WordNetLemmatizer is not None:
        try:
            lemmatizer = WordNetLemmatizer()
            lemmatizer.lemmatize("tests")
        except LookupError:
            lemmatizer = None

    cleaned_tokens = []
    for token in tokens:
        if len(token) < 2 or token in stop_words:
            continue
        cleaned_tokens.append(lemmatizer.lemmatize(token) if lemmatizer else token)

    return " ".join(cleaned_tokens)

