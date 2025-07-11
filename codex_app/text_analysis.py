from textblob import TextBlob
from typing import Dict
import matplotlib.pyplot as plt


def analyze_sentiment(text: str) -> Dict[str, float]:
    """Perform sentiment analysis and return polarity and subjectivity."""
    blob = TextBlob(text)
    return {
        "polarity": blob.sentiment.polarity,
        "subjectivity": blob.sentiment.subjectivity,
    }


def plot_sentiment(polarity: float) -> None:
    """Visualize sentiment polarity (-1 to 1)."""
    plt.figure(figsize=(4, 1))
    plt.barh(["Sentiment"], [polarity], color="skyblue")
    plt.xlim(-1, 1)
    plt.title("Sentiment Polarity")
    plt.show()
