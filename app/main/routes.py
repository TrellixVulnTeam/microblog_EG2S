from flask import render_template, request, current_app, request
from app.models import Post, Comment
from flask_bootstrap import Bootstrap
from app.main.forms import InputTextForm
from datetime import datetime
from app.main import bp

import random
import logging



@bp.route("/", methods=['GET', 'POST'])


@bp.route("/home", methods=['GET', 'POST'])
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)

    return render_template('main/home.html', posts=posts, current_time=datetime.utcnow())






@bp.route('/')
def track_example():
    track_event(
        category='Example',
        action='test action')
    return 'Event tracked.'


@bp.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500
















def analyse():
    start = time.time()
    if request.method == 'POST':
        rawtext = request.form['rawtext']
        #NLP Stuff
        blob = TextBlob(rawtext)
        received_text2 = blob
        blob_sentiment,blob_subjectivity = blob.sentiment.polarity ,blob.sentiment.subjectivity
        number_of_tokens = len(list(blob.words))
        # Extracting Main Points
        nouns = list()
        for word, tag in blob.tags:
            if tag == 'NN':
                nouns.append(word.lemmatize())
                len_of_words = len(nouns)
                rand_words = random.sample(nouns,len(nouns))
                final_word = list()
                for item in rand_words:
                    word = Word(item).pluralize()
                    final_word.append(word)
                    summary = final_word
                    end = time.time()
                    final_time = end-start
        return render_template('main/analytics.html',received_text = received_text2,number_of_tokens=number_of_tokens,blob_sentiment=blob_sentiment,blob_subjectivity=blob_subjectivity,summary=summary,final_time=final_time)
