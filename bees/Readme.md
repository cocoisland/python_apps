
https://beescolony.herokuapp.com

Beescolony application showed Honey Bee colony populations existed throughout US States from 1990-2016. The application also showed six common pesticides being used in various States from 1994-2016. 

At the bottom of the US maps, a slider which slided from year 1994-2016 automatically displaying HoneyBee colonies in various States of the country. The color heatmap showed the concentration of bees populations. When the mouse cursor hovered over a particular States, the chart on the upper right automatically displayed all HoneyBee colonies over years for that particular US State that the mouse cursor hovered over to. The chart on the lower right, also automatically displayed a default pesticide used in that particular US State. Below the lower right pesticide chart, is a drop down menu of six pesticides and when selected, will automatically show pesticide being used in that particular US States. And when compared the trend of pesticide graph with the trend of bees colony graph, a person could get a sense of how much indirect impact a particular pesticide had on bees colonies populations.

To run beescolony locally, download bees_final.csv and app.py.
Install dash library.

pip install dash==0.39.0  # The core dash backend
pip install dash-daq==0.1.0  # DAQ components (newly open-sourced!)
pip install pandas
python app.py

Deployment to Heroku.
1. To turn on production, Change app.run_server(debug=True) to app.run_server() Add app = dash.Dash(name, external_stylesheets=external_stylesheets) server = app.server
2. Create virtual env, python -m venv new_env
3.Install dash and gunicorn library pip install dash==0.39.0 # The core dash backend pip install dash-daq==0.1.0 # DAQ components (newly open-sourced!) pip install gunicorn
4.Create Procfile with 'web: gunicorn app:server' Testing : gunicorn app:server, to make sure everything run properly.
5.pip freeze > requirements.txt, to create requirement environment for Heroku to setup.

This beescolony repo is created to be deployed to Heroku. On Heroku

1. Create an app
2. On Heroku Deploy tab, choose GitHub option.
3. Search for beescolony repo.
4. Manual Deploy.
