"""Main application and routing logic for Sentiment."""
from decouple import config
from flask import Flask, render_template, abort, jsonify, request
from .models import DB , Misc
from .review_analysis import train_basilica, train_multinomialNB, countVectorizer_encoding
from .load_text import load_local_json, text_clean, BASILICA
import time, os, numpy as np
import pickle


load_msg = ""
metric={}
def create_app():
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    DB.init_app(app)

    @app.route('/')
    def root():
        misc=Misc.query.filter(Misc.id == 1).one()
        load_msg = misc.message
        return render_template('base.html', title='YelpFeelers Sentiment Analysis', metric = metric, load_msg=load_msg )

    @app.route('/predict_cv', methods=['POST'])
    def predict_cv():
          if request.values['review_text'] != "" :
            metric['usr_text'] = request.values['review_text']

            t1=time.time()
            x,y,x_pred = countVectorizer_encoding(metric['usr_text'])
            model = train_multinomialNB(x,y)
            prediction_cv = model.predict(x_pred)
            t2=time.time()

            metric['predvc_time']  = t2 - t1
            metric['prediction_cv']= prediction_cv
          else:
            metric['usr_text'] = 'No text entered'
          misc=Misc.query.filter(Misc.id == 1).one()
          load_msg = misc.message
          return render_template('base.html', title='YelpFeelers Sentiment Analysis', metric = metric , load_msg=load_msg)

    @app.route('/predict_bas', methods=['POST'])
    def predict_bas():
          if request.values['review_text'] != "" :
            metric['usr_text'] = request.values['review_text']

            t1=time.time()
            model = train_basilica()
            x_pred= BASILICA.embed_sentence(metric['usr_text'], model='product-reviews')
            prediction_bas = model.predict(np.array(x_pred).reshape(1,-1))
            t2=time.time()
            metric['predbas_time']  = t2 - t1
            metric['prediction_bas']= prediction_bas
          else:
            metric['usr_text'] = 'No text entered'

          misc=Misc.query.filter(Misc.id == 1).one()
          load_msg = misc.message
          return render_template('base.html', title='YelpFeelers Sentiment Analysis', metric = metric ,load_msg=load_msg)
          #return predicted_rating

    @app.route('/reset')
    def reset():
        pickle_file="./sentiment/model.pickle"
        os.path.isfile(pickle_file) and os.remove(pickle_file)
        DB.drop_all()
        DB.create_all()
        t1=time.time()
        num_rows = load_local_json()
        t2=time.time()
        load_time  = (t2 - t1)/60
        message="Number of observations= %i in %d mins." % (num_rows,load_time)
        db_misc = Misc(message=message)
        DB.session.add(db_misc)
        DB.session.commit()

        return render_template('base.html', title='Reset and Load data !' , metric=metric, load_msg=message)



    @app.route('/api', methods=['POST'])
    def make_endpoint():
      my_random_forest = pickle.load(open("filename","rb"))
      data = request.get_json(force=True)
      predict_request = [data['name'],data['n1']]
      predict_request = np.array(predict_request)
      y = my_random_forest.predict(predict_request)
      pred = [y_hat[0]]
      return jsonify(pred)


    return app

#if __name__ == '__main__':
#  app.run(port = 9000, debug = True)
