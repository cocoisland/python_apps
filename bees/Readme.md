
https://beescolony.herokuapp.com

Beescolony application showed Honey Bee colony populations existed throughout US States from 1990-2016. The application also showed six common pesticides being used in various States from 1994-2016. 

At the bottom of the US maps, a slider which slided from year 1994-2016 automatically displaying HoneyBee colonies in various States of the country. The color heatmap showed the concentration of bees populations. When the mouse cursor hovered over a particular States, the chart on the upper right automatically displayed all HoneyBee colonies over years for that particular US State that the mouse cursor hovered over to. The chart on the lower right, also automatically displayed a default pesticide used in that particular US State. Below the lower right pesticide chart, is a drop down menu of six pesticides and when selected, will automatically show pesticide being used in that particular US States. And when compared the trend of pesticide graph with the trend of bees colony graph, a person could get a sense of how much indirect impact a particular pesticide had on bees colonies populations.

To run beescolony locally, download bees_final.csv and app.py.
Install dash library.

pip install dash==0.39.0  # The core dash backend
pip install dash-daq==0.1.0  # DAQ components (newly open-sourced!)
pip install pandas
python app.py
