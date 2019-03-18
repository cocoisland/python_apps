curl https://cli-assets.heroku.com/install-ubuntu.sh | sh
heroku login
heroku git:remote -a cocoisland-twitoff
git remote --verbose

# need to git push requirements.txt and Procfile to github first in order for
# heroku to pull from github. Otherwise heroku will reject your git push.
pip freeze > requirements.txt
Procfile

git push origin master
git push heroku master
pip install gunicorn

#pip install flask flask-sqlalchemy tweepy basilica python-decouple python-dotenv scikit-learn gunicorn psycopg2


heroku config
heroku addons:create heroku-postgresql:hobby-dev

heroku logs --tail
heroku run

setting->config
yourapp.herokuapps.com
