from flask import Flask, render_template, request, send_file
import pandas as pd
from wordcloud import WordCloud
from textblob import TextBlob
import io

app = Flask(__name__)

def filter_sentiment(text_list, sentiment):
    filtered = []
    for text in text_list:
        words = TextBlob(str(text)).words
        for word in words:
            polarity = TextBlob(word).sentiment.polarity
            if sentiment == 'positive' and polarity > 0.1:
                filtered.append(word)
            elif sentiment == 'negative' and polarity < -0.1:
                filtered.append(word)
            elif sentiment == '':
                filtered.append(word)
    return ' '.join(filtered)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        column = request.form['column']
        sentiment = request.form['sentiment']
        max_words = int(request.form['max_words'])

        df = pd.read_csv(file)
        if column not in df.columns:
            return "Column not found in uploaded file."

        text_data = df[column].dropna().astype(str).tolist()
        filtered_text = filter_sentiment(text_data, sentiment)

        wc = WordCloud(width=800, height=400, background_color='white', max_words=max_words).generate(filtered_text)
        img_io = io.BytesIO()
        wc.to_image().save(img_io, 'PNG')
        img_io.seek(0)

        return send_file(img_io, mimetype='image/png')

    return render_template('index.html')