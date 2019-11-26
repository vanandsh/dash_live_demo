import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import altair as alt
#import utility as util
#from ./src import utility as util

app = dash.Dash(__name__, assets_folder='assets')
server = app.server

app.title = 'Dash app with pure Altair HTML'


import altair as alt
import vega_datasets

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
def make_plot(x_axis = 'Displacement', y_axis = 'Horsepower'):

    # Create a plot of the Displacement and the Horsepower of the cars dataset
    
    alt.themes.enable('mds_special')

    x_axis_with_type = x_axis + ':Q'
    y_axis_with_type = y_axis + ':Q'
    chart = alt.Chart(vega_datasets.data.cars.url).mark_point(size=90).encode(
                alt.X(x_axis_with_type, title = x_axis),
                alt.Y(y_axis_with_type, title = y_axis),
                tooltip = [x_axis_with_type, y_axis_with_type]
            ).properties(title=x_axis + ' vs. ' + y_axis,
                        width=500, height=350).interactive()

    return chart


app.layout = html.Div([

    ### ADD CONTENT HERE like: html.H1('text'),
    # html.H1('This is my first dashboard'),
    # html.H2('This is a subtitle'),

    # html.H3('Here is an image'),
    # html.Img(src='https://upload.wikimedia.org/wikipedia/commons/thumb/b/b7/Unico_Anello.png/1920px-Unico_Anello.png', 
            # width='10%'),
    html.H3('Dynamic Plot:'),
    html.Iframe(
        sandbox='allow-scripts',
        id='plot',
        height='500',
        width='750',
        style={'border-width': '0'},
        ################ The magic happens here
        #srcDoc=open('./Lecture1_charts/horsepower_vs_displacement.html').read()
        srcDoc=make_plot().to_html()
        ################ The magic happens here
        ),
    # dcc.Markdown('''

    #     ## Markdown Section 
        
    #     '''
    # ),
    # html.H3("Dropdown!"),

    # html.H3("Slider Bar!"),
    # dcc.Slider(
    #     min=0,
    #     max=9,
    #     marks={i: 'Label {}'.format(i) for i in range(10)},
    #     value=5,
    # ),
    # html.Br(),
    # html.Br(),
    # html.Br(),
    # html.Br(),
    ### Add Tabs to the top of the page
    # dcc.Tabs(id='tabs', value='tab1', children=[
    #     dcc.Tab(label='Lecture 1', value='tab-1'),
    #     dcc.Tab(label='Lecture 2', value='tab-2'),
    #     dcc.Tab(label='Lecture 3', value='tab-3'), 
    #     dcc.Tab(label='Lecture 4', value='tab-4'), 
    # ]),
    dcc.Markdown('''
        ### X-axis
        '''
    ),
    dcc.Dropdown(
    id='dd-chart_x',
    options=[
        {'label': 'Fuel Efficiency', 'value': 'Miles_per_Gallon'},
        {'label': 'Cylinders', 'value': 'Cylinders'},
        {'label': 'Engine Displacement', 'value': 'Displacement'},
        # Missing option here
    ],
    value='Displacement',
    style=dict(width='45%',
            verticalAlign="middle")
            ),
    dcc.Markdown('''
        ### Y-axis
        '''
    ),
    dcc.Dropdown(
    id='dd-chart_y',
    options=[
        {'label': 'Fuel Efficiency', 'value': 'Miles_per_Gallon'},
        {'label': 'Cylinders', 'value': 'Cylinders'},
        {'label': 'Engine Displacement', 'value': 'Displacement'},
        # Missing option here
    ],
    value='Cylinders',
    style=dict(width='45%',
            verticalAlign="middle")
            ),
    
])

@app.callback(
    dash.dependencies.Output('plot', 'srcDoc'),
    [dash.dependencies.Input('dd-chart_x', 'value'),
    dash.dependencies.Input('dd-chart_y', 'value')])
def update_plot(xaxis_column_name, yaxis_column_name):
    '''
    Takes in an xaxis_column_name and calls make_plot to update our Altair figure
    '''
    updated_plot = make_plot(xaxis_column_name,yaxis_column_name).to_html()
    return updated_plot


if __name__ == '__main__':
    app.run_server(debug=True)
