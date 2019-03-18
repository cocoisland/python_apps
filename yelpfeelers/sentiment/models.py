from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()


class ReviewRating(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    stars = DB.Column(DB.Float)
    review_text = DB.Column(DB.Unicode(500))
    embedding = DB.Column(DB.PickleType, nullable=False)

    def __repr__(self):
        return '<ReviewRating {}>'.format(self.review_text)
        #return f'ReviewRating {self.stars}'

class Misc(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    message = DB.Column(DB.String(50))
