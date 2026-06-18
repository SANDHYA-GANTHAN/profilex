import nltk

from nltk.corpus import stopwords

from nltk.stem import WordNetLemmatizer

from nltk.tokenize import word_tokenize


stop_words = set(stopwords.words("english"))

lemmatizer = WordNetLemmatizer()


def clean_text(text):

    tokens = word_tokenize(text.lower())

    cleaned = []

    for token in tokens:

        if token.isalpha():

            if token not in stop_words:

                cleaned.append(
                    lemmatizer.lemmatize(token)
                )

    return " ".join(cleaned)