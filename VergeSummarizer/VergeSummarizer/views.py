"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, request, jsonify
from VergeSummarizer import app
from VergeSummarizer import Summarizer

@app.route('/')
def home():
    return render_template('index.html',
        title="TheVerge Summarizer")

@app.route('/article')
def readArticle():
    try:
        url = request.args.get('url', 0, type=str)
        return ' '.join(Summarizer.getVergeReport(url, 5))
    except Exception as e:
        return str(e)
