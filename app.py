import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
import altair as alt
from altair import datum
import vega_datasets
import pandas as pd
import numpy as np
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, assets_folder='assets',external_stylesheets=[dbc.themes.CERULEAN])
app.config['suppress_callback_exceptions'] = True

server = app.server
app.title = 'Dash app for DSCI 532 group - 103'
def chart1():
    """
    Make a US map plot to show the average hate crime per 100K population in each state. Each state is colored by gradient according to the value of average hate crime per 100K populaiton
    ----------------
    Returns:
    A Choropleth U.S. map with states shaded according to the value of average hate crime per 100K populaiton
    

    """
    def mds_special():
        font = "Arial"
        axisColor = "#000000"
        gridColor = "#DEDDDD"
        return {
            "config": {
                "title": {
                    "fontSize": 14,
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
                    "labelFontSize": 10,
                    "labelAngle": 0, 
                    "tickColor": axisColor,
                    "tickSize": 5, # default, including it just to show you can change it
                    "titleFont": font,
                    "titleFontSize": 12,
                    "titlePadding": 10, # guessing, not specified in styleguide
                    "title": "X Axis Title (units)", 
                },
                "axisY": {
                    "domain": False,
                    "grid": True,
                    "gridColor": gridColor,
                    "gridWidth": 1,
                    "labelFont": font,
                    "labelFontSize": 10,
                    "labelAngle": 0, 
                    #"ticks": False, # even if you don't have a "domain" you need to turn these off.
                    "titleFont": font,
                    "titleFontSize": 12,
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
    hate_crime = pd.read_csv('data/crime_state_id_clean.csv')

    p1 =alt.Chart(states).mark_geoshape().encode(
            alt.Color('avg_hatecrimes_per_100k_fbi:Q',title='Average hate crime per 100K', scale = alt.Scale(scheme='orangered')),
            tooltip = [
                alt.Tooltip('avg_hatecrimes_per_100k_fbi:Q', title = 'Average hate crime per 100K'),
                alt.Tooltip('state:N')
            ]
        ).transform_lookup(
            lookup='id',
            from_=alt.LookupData(hate_crime, 'id', ['avg_hatecrimes_per_100k_fbi','state'])
        ).project('albersUsa').properties(
            title='Average hate crimes per 100K population in US states',
            width=550,
            height=300)
    
    return p1 


def chart2(x_val = 'gini_index'):
    """
    This function creates a chart for avg hate crime rate across a specified factor given as input.   
    -------------------

    Arguments:
    x_val - The factor for which we want to compare the avg hate crime rate
    -------------------

    Returns:
    A altair chart with the scatter plot for avg. hate crime rate and specified factor.

    """
    df = pd.read_csv('data/hate_crimes.csv').loc[:,[x_val,'avg_hatecrimes_per_100k_fbi','state']]
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
        tooltip = [alt.Tooltip('state:O', title = "State")]
    )

    # Plot the best fit polynomials
    polynomial_fit = alt.Chart(poly_data).mark_line().encode(
        x='xfit:Q',
        y='1:Q'
    )
    
    return (points + polynomial_fit).properties(title = 'Hate crime rate across socio-economic factors', width = 400, height = 300)
def graph3_4():
    """
    Read and wrangles data from hate_crime.csv file and creates three plots 
    (a heatmap - for percentage of Trump voters across states and change in hate crime after 2016 elections, 
    and two bar charts - for states divided on basis of pre-election hate crime rates) with interactivity among them.
    
    Returns
    -------
    plots
        Three altait plots with interactivity among them
    """
    
    crime_data = pd.read_csv('data/hate_crimes.csv')

    # Wrangling data
    
    crime_data_n = crime_data

    crime_data_n['avg_hatecrimes_fbi_10days'] = ((crime_data_n['avg_hatecrimes_per_100k_fbi']/365)*10)

    crime_data_n['prop'] = (crime_data_n['hate_crimes_per_100k_splc'] - crime_data_n['avg_hatecrimes_fbi_10days'])/crime_data_n['avg_hatecrimes_fbi_10days']

    mean_crime = crime_data_n['avg_hatecrimes_fbi_10days'].mean()

    conditions = [
        (crime_data_n['avg_hatecrimes_fbi_10days'] <= mean_crime ),
        (crime_data_n['avg_hatecrimes_fbi_10days'] > mean_crime)]
    choices = ['low baseline crime rate', 'high baseline crime rate']
    crime_data_n['crime_rate_bracket'] = np.select(conditions, choices)
    
    crime_data_n['diff_hatecrime'] = (crime_data_n['hate_crimes_per_100k_splc'] - crime_data_n['avg_hatecrimes_fbi_10days'])
    crime_data_sorted_trump = crime_data_n.sort_values(by='share_voters_voted_trump')

    state_selector = alt.selection_multi(fields=['state'])

    # Create the plots

    l = alt.Chart(crime_data_n, title = "Rate of change of hate crimes across states with low baseline").mark_bar().encode(
            alt.X('state:N', title = '', axis=alt.Axis(labelAngle = -45)),
            alt.Y('prop:Q', title = 'Rate of change'),
            color=alt.condition(state_selector, alt.ColorValue("steelblue"), alt.ColorValue("grey"))
        ).transform_filter((datum.crime_rate_bracket == 'low baseline crime rate')).properties(width = 475,height = 200)

    h = alt.Chart(crime_data_n, title = "Rate of change of hate crimes across states with high baseline").mark_bar().encode(
            alt.X('state:N', axis=alt.Axis(labelAngle = -45),  title = ''),
            alt.Y('prop:Q', title = 'Rate of change', scale=alt.Scale(domain=[0, 30])),
            color=alt.condition(state_selector, alt.ColorValue("steelblue"), alt.ColorValue("grey"))
        ).transform_filter((datum.crime_rate_bracket == 'high baseline crime rate')).properties(width = 450,height = 200)

    heatmap = alt.Chart(crime_data_sorted_trump, title = 'Change in hate crime rate with voting trend during 2016 U.S. elections').mark_rect().encode(
        alt.X('state', sort=None, title=" ", axis=alt.Axis(labelAngle = -45)),
        alt.Y('share_voters_voted_trump', title="People who voted for Trump (%)"),
        alt.Color('diff_hatecrime', title="Change in hate crime rate (%)", scale = alt.Scale(scheme='orangered')),
        tooltip = [alt.Tooltip('state', title = 'State'),
                   alt.Tooltip('hate_crimes_per_100k_splc', title = "Hate crime rate 10 days after election"),
                   alt.Tooltip('avg_hatecrimes_fbi_10days', title = "Average rate of hate crime (for 10 days")]
    ).properties(width = 950,height = 200).add_selection(state_selector)

    return alt.vconcat(
        heatmap,
        l | h)

    
tabs_styles = {
    'height': '50px',
    'width':'1300px',
    'marginLeft': 20
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'padding-left': '5px',
    'padding-bottom': '100px',  
}

footer = dbc.Container([dbc.Row(dbc.Col(dcc.Markdown('''*Note - States have been divided on the basis of average pre-election hate \
    crime rates into low and high categories. Click on the bars to top graph to explore which baseline category \
    the state lies in.*''', style = {'font-size': '12px'}))),
                        ])

app.layout = html.Div([ 
    ### Add Tabs to the top of the page
    
    html.Div([dbc.Jumbotron([
                dbc.Container([
                      html.H2("The U.S. Hate Crime Analysis"),
                      dcc.Markdown('''
                    Using this App, you can explore the relationship between different socio-economic factors (income, unemployment, education, etc) and hate crime rates. It can also be used to investigte the change of hate crime rates before and after the U.S. president election in 2016.
    '''),],#fluid=True,
                              )],
                                     fluid=True,
                
                                     ),
                                   ]),

    html.Div([
    ### Add Tabs to the top of the page
    dcc.Tabs(id='tabs', value='tab-1', children=[
        dcc.Tab(label='Scoio-Economic factors', value='tab-1'),
        dcc.Tab(label='General Elections', value='tab-2'),
    ],style=tabs_styles),

    html.Div(id='tabs-content-example')
    ])
])


@app.callback(Output('tabs-content-example', 'children'),
              [Input('tabs', 'value')])
def render_content(tab = 'tab-1'):
    """
    This functions updates the values of the tab in our dashboard based on the click on a particular tab
    ---------------------

    Arguments :
    tab - The value of the tab input from the callback function.
    ---------------------

    Returns :
    A html div containing the all the updated plots

    """
    if tab == 'tab-1':
        return html.Div([
            html.H2('Analysis of U.S hate crime rates from 2010-2015 ',
                    style={'font-family':'arial','font-size':'20px', 'padding-left':'400px', 'padding-top':'50px'}),
            
            html.P('The hate crimes are not evenly distributed across all the states in the U.S. \
            Some states have much higher rates than others. This brings up a question that whether \
            there are some factors asscoiated with the occurence of hate crimes. The analysis in this \
                section will help to approach this question.',
                   style={'font-family':'arial','font-size':'16px', 'padding-left':'100px','padding-bottom':'40px',\
                        'color':'black'}),

            html.Div([ 
                html.Iframe(
                    sandbox='allow-scripts',
                    id='plot1',
                    height='400',
                    width='800',
                    style={'border-width':'0'},
                    ################ The magic happens here
                    srcDoc = chart1().to_html()
                    ################ The magic happens here
                    )],
                    style={'display': 'inline-block', 'width': '58%', 'border-width':'0'}
            ),
                html.Div([
                    html.Iframe(
                    sandbox='allow-scripts',
                    id='chart2',
                    height='400',
                    width='550',
                    style={'border-width': '0'},
                    ################ The magic happens here
                    srcDoc = chart2().to_html()
                    ################ The magic happens here
                ),
                html.Div('Select factor for x-axis', 
                        style={'font-family':'arial','font-size':'12px','color':'black'}),
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
                )],
                style= {'display': 'inline-block','width': '42%','height': '30px', 'border-width':'0'}
            )            
        ], style = tab_selected_style)
    elif tab == 'tab-2':
        return html.Div([
                    html.H2('Impact of 2016 U.S. elections on hate crimes',
                    style={'font-family':'arial','font-size':'20px', 'padding-left':'400px', 'padding-top':'50px'}),
                    html.P('Big fluctuations in the hate crime rates have been observed after the U.S. president election in 2016. \
                        It is tempting to think that the election may have substantial impact on these rates. However, before any \
                        conclusion can be made, it needs to be evaluated whether these changes were impacted by a state\'s voting trend',
                    style={'font-family':'arial','font-size':'16px', 'padding-left':'100px','padding-bottom':'40px',  \
                        'color':'black'}),            
                    html.Iframe(
                        sandbox='allow-scripts',
                        id='plot',
                        height='700',
                        width='1300',
                        style={'border-width': '0'},
                        ################ The magic happens here
                        srcDoc=graph3_4().to_html()
                        ################ The magic happens here
                    ),
                    footer    
        ],style = {'borderTop': '1px solid #d6d6d6','padding-left':'5px'})


@app.callback(
    dash.dependencies.Output('chart2', 'srcDoc'),
    [dash.dependencies.Input('dd-chart', 'value')])
def update_plot(xaxis_column_name):
    """
    This functions updates the scatter plot in tab 1 with user input from drop-down menu received from callback
    ----------------

    Arguments : 
    xaxis_column_name - name of the factor in the with which the plot of avg. hate crime vs factor needs to be created
    ----------------

    Returns :
    A function call to the plot creation function with user input of x-axis.

    """
    updated_plot = chart2(xaxis_column_name).to_html()
    return updated_plot

if __name__ == '__main__':
    app.run_server(debug=True)
