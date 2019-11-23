import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(__name__, assets_folder='assets')
server = app.server

app.title = 'Dash app with pure Altair HTML'

app.layout = html.Div([

    ### ADD CONTENT HERE like: html.H1('text'),
    html.H1('This is my first dashboard'),
    html.H2('This is the second line'),
    html.Iframe(
        sandbox='allow-scripts',
        id='plot',
        height='2000',
        width='1800',
        style={'border-width': '5px'},

        ################ The magic happens here
        srcDoc=open('complex_chart.html').read()
        ################ The magic happens here
        )

])

if __name__ == '__main__':
    app.run_server(debug=True)

