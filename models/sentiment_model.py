import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Initialize Sentiment Analyzer
sia = SentimentIntensityAnalyzer()

def load_emoji_sentiments(filepath):
    # Load emoji sentiment data from CSV
    df = pd.read_csv(filepath)
    emoji_sentiments = {}
    for _, row in df.iterrows():
        emoji_sentiments[row['Emoji']] = {
            'pos': row['Positive'],
            'neg': row['Negative'],
            'neutral': row['Neutral']
        }
    return emoji_sentiments

# Load emoji sentiments from the dataset
emoji_sentiments = load_emoji_sentiments('data/Emoji_Sentiment_Data.csv')

def analyze_text(text):
    # Analyze text sentiment using VADER
    return sia.polarity_scores(text)

def analyze_emoji(text):
    # Analyze emojis sentiment using the dataset
    score = {'pos': 0, 'neg': 0, 'neutral': 0}
    for char in text:
        if char in emoji_sentiments:
            sentiment = emoji_sentiments[char]
            score['pos'] += sentiment['pos']
            score['neg'] += sentiment['neg']
            score['neutral'] += sentiment['neutral']
    return score
