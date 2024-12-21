import re
import nltk
from nltk.corpus import stopwords
import ssl

# Handle stopword download
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

# Download stopwords
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))


# Text processing
def preprocess_text(text):
    text = re.sub(r'http\S+', '', text)  # Remove URLs
    text = re.sub(r'@\S+', '', text)     # Remove mentions
    text = re.sub(r'#\S+', '', text)     # Remove hashtags
    text = re.sub(r'[^A-Za-z\s]', '', text)  # Remove special characters
    text = text.lower().strip()
    words = text.split()
    words = [word for word in words if word not in stop_words]
    return ' '.join(words)

