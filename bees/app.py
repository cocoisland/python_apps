
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go

df = pd.read_csv('bees_final.csv')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Div([
        html.Div([
        dcc.Graph(id='graph-with-slider',
                  hoverData={'points': [{'location': 'CA'}]}),
        dcc.Slider(
            id='year-slider',
            min=df['Year'].min(),
            max=df['Year'].max(),
            value=df['Year'].max(),
            marks={str(year): str(year) for year in df['Year'].unique()}
        )],style={'width': '49%', 'display': 'inline-block'}),

        html.Div([
            dcc.Graph(id='colony-time-series'),
            dcc.Graph(id='pesticide-time-series'),

            dcc.Dropdown(
                id='pesticide',
                options=[{'label': i, 'value': i} for i in df.columns[6:12]],
                value='nAllNeonic'
            ),
        ], style={'width': '49%', 'float': 'right', 'display': 'inline-block'})

    ],style={
        'borderBottom': 'thin lightgrey solid',
        'backgroundColor': 'rgb(250, 250, 250)',
        'padding': '10px 5px'
    }),

])

def create_time_series(dff, param, title):
    return {
        'data': [go.Scatter(
            x=dff['Year'],
            y=dff[param],
            mode='lines+markers'
        )],
        'layout': {
            'height': 225,
            'margin': {'l': 30, 'b': 30, 'r': 10, 't': 10},
            'annotations': [{
                'x': 0, 'y': 0.85, 'xanchor': 'left', 'yanchor': 'bottom',
                'xref': 'paper', 'yref': 'paper', 'showarrow': False,
                'align': 'left', 'bgcolor': 'rgba(255, 255, 255, 0.5)',
                'text': title
            }],
            'xaxis': {'showgrid': False}
        }
    }

@app.callback(
    dash.dependencies.Output('colony-time-series', 'figure'),
    [dash.dependencies.Input('pesticide', 'value'),
    dash.dependencies.Input('graph-with-slider', 'hoverData')
     ])
def update_timeseries(pesticide_name, hoverData):
    hoverStateName = hoverData['points'][0]['location']
    dff = df.loc[df.state == hoverStateName, ['Year',pesticide_name,'Colonies']]

    title = '<b>Bees Colonies in :{}</b>'.format(hoverStateName)
    return create_time_series(dff, 'Colonies', title)

@app.callback(
    dash.dependencies.Output('pesticide-time-series', 'figure'),
    [dash.dependencies.Input('pesticide', 'value'),
    dash.dependencies.Input('graph-with-slider', 'hoverData')
     ])
def update_timeseries(pesticide_name, hoverData):
    hoverStateName = hoverData['points'][0]['location']
    dff = df.loc[df.state == hoverStateName, ['Year',pesticide_name,'Colonies']]

    title = '<b>Pesticide:{} used in:{}</b>'.format(pesticide_name,
                                                            hoverStateName)
    return create_time_series(dff, pesticide_name, title)



@app.callback(
    dash.dependencies.Output('graph-with-slider', 'figure'),
    [dash.dependencies.Input('year-slider', 'value')])
def update_figure(selected_year):
    filtered_df = df[df.Year == selected_year]

    scl = [
            [0.0, 'rgb(255,225,225)'],
            [0.2, 'rgb(245,210,203)'],
            [0.4, 'rgb(231,166,153)'],
            [0.6, 'rgb(213,122,105)'],
            [0.8, 'rgb(191,77,60)'],
            [1.0, 'rgb(165,18,18)']
            ]

    df_grouped = filtered_df.groupby('state').sum().reset_index()

    data = [go.Choropleth(
    colorscale = scl,
    autocolorscale = False,
    locations = df_grouped['state'],
    z = df_grouped['Colonies'],
    locationmode = 'USA-states',
    marker = go.choropleth.Marker(
        line = go.choropleth.marker.Line(
            color = 'rgb(255,255,255)',
            width = 2
        )),
    colorbar = go.choropleth.ColorBar(
        title = "#Colonies")
    )]


    layout = go.Layout(
    title = go.layout.Title(
        text = str(selected_year) + ' Bees Colonies<br>(Hover for breakdown)'
    ),
    hovermode='closest',
    geo = go.layout.Geo(
        scope = 'usa',
        projection = go.layout.geo.Projection(type = 'albers usa'),
        showlakes = True,
        lakecolor = 'rgb(255, 255, 255)'),
    )

    return {'data': data, 'layout': layout}



if __name__ == '__main__':
    app.run_server(port=9100)
    #app.run_server(debug=True)
