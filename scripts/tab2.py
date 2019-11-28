import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output
import altair as alt
import pandas as pd
import numpy as np
from altair import datum


crime_data = pd.read_csv('../data/hate_crimes.csv')


app = dash.Dash(__name__, assets_folder='assets')
app.config['suppress_callback_exceptions'] = True

server = app.server
app.title = 'U.S. hatecrimes'


def graph3_4():

    def mds_special():
        font = "Arial"
        axisColor = "#000000"
        gridColor = "#DEDDDD"
        return {
            "config": {
                "title": {
                    "fontSize": 24,
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
                    "labelFontSize": 14,
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
    #alt.themes.enable('none') # to return to default

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

    l = alt.Chart(crime_data_n, title = "States with low baseline crime rate").mark_bar().encode(
            alt.X('state:N', title = '', axis=alt.Axis(labelAngle = -45)),
            alt.Y('prop:Q', title = 'Rate of change of hate crime pre and post election'),
            color=alt.condition(state_selector, alt.ColorValue("steelblue"), alt.ColorValue("grey"))
        ).transform_filter((datum.crime_rate_bracket == 'low baseline crime rate'))

    h = alt.Chart(crime_data_n, title = "States with high baseline crime rate").mark_bar().encode(
            alt.X('state:N', axis=alt.Axis(labelAngle = -45),  title = ''),
            alt.Y('prop:Q', title = 'Rate of change of hate crime pre and post election', scale=alt.Scale(domain=[0, 30])),
            color=alt.condition(state_selector, alt.ColorValue("steelblue"), alt.ColorValue("grey"))
        ).transform_filter((datum.crime_rate_bracket == 'high baseline crime rate')).properties(width = 500)

    heatmap = alt.Chart(crime_data_sorted_trump, width= 450).mark_rect().encode(
        alt.X('state', sort=None, title=" ", axis=alt.Axis(labelAngle = -45)),
        alt.Y('share_voters_voted_trump', title="Share of Trump voters (%)"),
        alt.Color('diff_hatecrime', title="Change in hate crime rate (%)"),
        tooltip = [alt.Tooltip('state', title = 'State'),
                   alt.Tooltip('hate_crimes_per_100k_splc', title = "Hate crime rate 10 days after election"),
                   alt.Tooltip('avg_hatecrimes_fbi_10days', title = "Average rate of hate crime (for 10 days")]
    ).properties(width = 1000).add_selection(state_selector)


    return alt.vconcat(
        heatmap,
        l | h)


jumbotron = dbc.Jumbotron(
    		[
		dbc.Container(
		    [html.H5("2016 U.S. election: Change in hate crime rate with voting trend", className="display-3"),
		    ],
		fluid=True,
			     )
		],
	fluid=True
	)


content = dbc.Container([
    dbc.Row(
	    [dbc.Col(
		html.Iframe(
			sandbox='allow-scripts',
			id='plot',
			height='800',
			width='1400',
			style={'border-width': '0', 'align':'center'},
			################ The magic happens here
			srcDoc=graph3_4().to_html()
			################ The magic happens here
			),width='7' 
		    )
	     ]
	   )
	])

app.layout = html.Div([html.H2("2016 U.S. election: Change in hate crime rate with voting trend"),
			html.Iframe(
			sandbox='allow-scripts',
			id='plot',
			height='1000',
			width='1500',
			style={'border-width': '0'},
			################ The magic happens here
			srcDoc=graph3_4().to_html()
			################ The magic happens here
			)], style={'align':'center'})


if __name__ == '__main__':
    app.run_server(debug=True)
