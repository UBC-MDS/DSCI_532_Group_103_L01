import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
import altair as alt
import vega_datasets
import pandas as pd
import numpy as np

app = dash.Dash(__name__, assets_folder='assets')
app.config['suppress_callback_exceptions'] = True

server = app.server
app.title = 'Dash app for DSCI 532 group - 103'
def chart1():

    def mds_special():
        font = "Arial"
        axisColor = "#000000"
        gridColor = "#DEDDDD"
        return {
            "config": {
                "title": {
                    "fontSize": 18,
                    "font": font,
                    "anchor": "start", # equivalent of left-aligned.
                    "fontColor": "#000000"
                },
                'view': {
                    "height": 300, 
                    "width": 400
                },
                "axisX": {
                    "domain": True,
                    #"domainColor": axisColor,
                    "gridColor": gridColor,
                    "domainWidth": 1,
                    "grid": False,
                    "labelFont": font,
                    "labelFontSize": 12,
                    "labelAngle": 0, 
                    "tickColor": axisColor,
                    "tickSize": 5, # default, including it just to show you can change it
                    "titleFont": font,
                    "titleFontSize": 16,
                    "titlePadding": 10, # guessing, not specified in styleguide
                    "title": "X Axis Title (units)", 
                },
                "axisY": {
                    "domain": False,
                    "grid": True,
                    "gridColor": gridColor,
                    "gridWidth": 1,
                    "labelFont": font,
                    "labelFontSize": 12,
                    "labelAngle": 0, 
                    #"ticks": False, # even if you don't have a "domain" you need to turn these off.
                    "titleFont": font,
                    "titleFontSize": 16,
                    "titlePadding": 10, # guessing, not specified in styleguide
                    "title": "Y Axis Title (units)", 
                    # titles are by default vertical left of axis so we need to hack this 
                    #"titleAngle": 0, # horizontal
                    #"titleY": -10, # move it up
                    #"titleX": 18, # move it to the right so it aligns with the labels 
                },
            }
                }

    # register the custom theme under a chosen name
    alt.themes.register('mds_special', mds_special)

    # enable the newly registered theme
    alt.themes.enable('mds_special')
    from vega_datasets import data

    states = alt.topo_feature(data.us_10m.url, 'states')
    hate_crime = pd.read_csv('..\data\crime_state_id_clean.csv')

    p1 =alt.Chart(states).mark_geoshape().encode(
            alt.Color('avg_hatecrimes_per_100k_fbi:Q',title="Average hate crime per 100K"),
            tooltip = [
                alt.Tooltip('avg_hatecrimes_per_100k_fbi:Q', title = 'Average hate crime per 100K'),
                alt.Tooltip('state:N')
            ]
        ).transform_lookup(
            lookup='id',
            from_=alt.LookupData(hate_crime, 'id', ['avg_hatecrimes_per_100k_fbi','state'])
        ).project('albersUsa').properties(
            title='Average hate crimes per 100K population in each state',
            width=550,
            height=300)
    
    return p1 


def chart2(x_val = 'gini_index'):

    df = pd.read_csv('..\data\hate_crimes.csv').loc[:,[x_val,'avg_hatecrimes_per_100k_fbi','state']]
    df = df.dropna()
    
    df = pd.DataFrame({'x': df.iloc[:,0], 'y': df.iloc[:,1], 'state':df.iloc[:,2] })

    # Define the degree of the polynomial fit
    degree = 1

    # Build a dataframe with the fitted data
    poly_data = pd.DataFrame({'xfit': np.linspace(df['x'].min(), df['x'].max(), 500)})

    poly_data[str(degree)] = np.poly1d(np.polyfit(df['x'], df['y'], degree))(poly_data['xfit'])

    type_dict = {'gini_index': 'Income Disparity',
                'share_unemployed_seasonal': 'Unemployment rate seasonal',
                'share_white_poverty': 'White people poverty rate',
                'share_non_citizen': 'Percentage of Non-citizens',
                'share_population_in_metro_areas': 'Percentage of people in metro cities'}
                
    # Plot the data points on an interactive axis
    points = alt.Chart(df).mark_circle(color='black', size = 40, opacity = 0.6).encode(
        x=alt.X('x:Q', title=type_dict[x_val], scale = alt.Scale(domain = [min(df['x']),max(df['x'])])),
        y=alt.Y('y:Q', title='Average hate crime per 100K people'),
        tooltip = 'state:O'
    )

    # Plot the best fit polynomials
    polynomial_fit = alt.Chart(poly_data).mark_line().encode(
        x='xfit:Q',
        y='1:Q'
    )
    
    return (points + polynomial_fit).properties(title = 'Hate crime rate across demographic factors', width = 450, height = 250)


app.layout = html.Div([ 
    ### Add Tabs to the top of the page
    dcc.Tabs(id='tabs', value='tab1', children=[
        dcc.Tab(label='Hate Crimes on Average', value='tab-1'),
        dcc.Tab(label='Hate Crimes in Elections ', value='tab-2'),
    ]),    

    html.Div(id='tabs-content-example')
])


@app.callback(Output('tabs-content-example', 'children'),
              [Input('tabs', 'value')])
def render_content(tab = 'tab-1'):
    if tab == 'tab-1':
        return html.Div([
            html.H2('Analysis of Hate crime rates across demographic factors', 
            style={'font-family':'ariel,serif','font-size':'32px'}),
            html.Div([ 
                html.Iframe(
                    sandbox='allow-scripts',
                    id='plot1',
                    height='500',
                    width='1000',
                    style={'border-width':'0'},
                    ################ The magic happens here
                    srcDoc = chart1().to_html()
                    ################ The magic happens here
                    )],
                    style={'display': 'inline-block', 'width': '55%', 'border-width':'0'}
            ),
            html.Div([
                html.H4('Choose the demographic factor on x -axis:'),
                dcc.Dropdown(
                    id = 'dd-chart',
                    options = [
                        {'label': 'Income Disparity', 'value': 'gini_index'},
                        {'label': 'Unemployment rate seasonal', 'value': 'share_unemployed_seasonal'},
                        {'label': 'White people poverty rate', 'value': 'share_white_poverty'},
                        {'label': 'Percentage of Non-citizens', 'value': 'share_non_citizen'},
                        {'label': 'Percentage of people in metro cities', 'value': 'share_population_in_metro_areas'}
                    ],
                    value = 'gini_index',
                    style=dict(width = '70%',
                                verticalAlign="middle")
                ),
                html.Iframe(
                    sandbox='allow-scripts',
                    id='chart2',
                    height='500',
                    width='1000',
                    style={'border-width': '0'},
                    ################ The magic happens here
                    srcDoc = chart2().to_html()
                    ################ The magic happens here
                )],
                style= {'display': 'inline-block','width': '45%', 'border-width':'0'}
            )             
        ])
    elif tab == 'tab-2':
        return html.Div([
            html.H3('Tab content 2'),
            dcc.Graph(
                id='graph-2-tabs',
                figure={
                    'data': [{
                        'x': [1, 2, 3],
                        'y': [5, 10, 6],
                        'type': 'bar'
                    }]
                }
            )
        ])

@app.callback(
    dash.dependencies.Output('chart2', 'srcDoc'),
    [dash.dependencies.Input('dd-chart', 'value')])
def update_plot(xaxis_column_name):

    updated_plot = chart2(xaxis_column_name).to_html()
    return updated_plot

if __name__ == '__main__':
    app.run_server(debug=True)