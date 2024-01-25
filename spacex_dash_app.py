# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px
import sys

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create dropdown list content
dropdown_list = [{'label': 'All Sites', 'value': 'ALL'}]
for site in spacex_df['Launch Site'].unique():
    dropdown_list.append({'label': site, 'value': site})

# Create an app layout
app.layout = html.Div([
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center',
                   'color': '#503D36',
                   'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
    html.Div([               
        html.Label("Choose Launch Site:"),       
        dcc.Dropdown(
        id='site-dropdown',
        options=dropdown_list,
        value='ALL',
        placeholder="Choose Launch Site",
        searchable=True,
        style={
            'width': '80%',
            'padding': '3px',
            'text-align-last': 'center',
            'margin': 'auto'
            })
            ]),
    html.Br(),

#     # TASK 2: Add a pie chart to show the total successful launches count for all sites
#     # If a specific launch site was selected, show the Success vs. Failed counts for the site
    html.Div(dcc.Graph(id='success-pie-chart'), 
             style={'display': 'flex'}),
    html.Br(),

    html.P("Payload range (Kg):"),
#     # TASK 3: Add a slider to select payload range
    dcc.RangeSlider(id='payload-slider',
                    min=0, max=10000, step=1000,
                    marks={0: '0', 2500: '2500',5000:'5000',10000:'10000'},
                    value=[0, 10000]),

    # TASK 4: Add a scatter chart to show the correlation between payload and launch success
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
    ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)

def get_pie_chart(entered_site):
    #get successful launches
    if entered_site == 'ALL':
        filtered_df = spacex_df[spacex_df['class']==1]
        pdf = filtered_df.groupby('Launch Site')['class'].sum().reset_index()
        fig = px.pie(pdf, 
                values='class', 
                names='Launch Site', 
                title='Total Success Launches By Launch Site')
        
    else:
        filtered_df = spacex_df[spacex_df['Launch Site']==entered_site]
        pdf = filtered_df['class'].value_counts().reset_index()
        fig = px.pie(pdf, 
                values='class', 
                names= 'index', 
                title='Total Success Launches By Site')
    return fig
          

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id='payload-slider', component_property='value')]
)


def get_scatter_chart(entered_site, entered_payload):
    entered_min, entered_max = entered_payload
    if entered_site == 'ALL':
        sdf = spacex_df[(spacex_df['Payload Mass (kg)'] >= entered_min) &
                        (spacex_df['Payload Mass (kg)'] <= entered_max)]
        title = 'Total Success Launches (All Sites)'
    else:
        sdf = spacex_df[(spacex_df['Launch Site'] == entered_site) &
                        (spacex_df['Payload Mass (kg)'] >= entered_min) &
                        (spacex_df['Payload Mass (kg)'] <= entered_max)]
        title = f'Total Success Launches at {entered_site}'

    fig2 = px.scatter(sdf, 
                      x='Payload Mass (kg)', 
                      y='class',
                      color="Booster Version Category",
                      title=title)
    return fig2

# Run the app
if __name__ == '__main__':
    app.run_server()
