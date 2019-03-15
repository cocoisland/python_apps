"""Main application and routing logic for Sentiment."""
from decouple import config
from flask import Flask, render_template, request
from .models import DB 
from .review_analysis import fetchRating, predict_text


def create_app():
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    DB.init_app(app)

    @app.route('/')
    def root():
	# Welcome, readme, how-to in base.html
        return render_template('base.html', title='YelpFeelers Sentiment Analysis' )

    @app.route('/predict', methods=['POST'])
    def predict():
        str_pred = request.values['review_text']
        prediction = predict_text(str_pred)
        return render_template('predict.html', title='Predicted value',usr_text=str_pred, prediction=prediction )
        #return predicted_rating

    @app.route('/reset')
    def reset():
        DB.drop_all()
        DB.create_all()
        return render_template('base.html', title='DB Reset!')

    return app

