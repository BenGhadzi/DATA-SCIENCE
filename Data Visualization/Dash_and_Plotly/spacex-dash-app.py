# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(
                                    id='site-dropdown',
                                    options=[
                                        {'label': 'All sites', 'value': 'ALL'},
                                        {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                        {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                        {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                        {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                    ],
                                    value= 'ALL',
                                    placeholder='Select a Launch Site here',
                                    searchable=True,
                                    ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart',)),
                                
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min= 0,
                                                max=10000, step=1000, marks={0: '0', 100: '100'},
                                                value=[min_payload,max_payload],
                                ),
                                                 

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                                               
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
    )

def update_graph(selected_option):
    if selected_option == 'ALL':
        fig= px.pie(spacex_df,
                    values='class',
                    names='Launch Site',
                    title='LAUNCH SUCCESS FOR SELECTED LAUNCH SITES'
                    )
        return fig
    elif selected_option != 'ALL': 
        new_df = spacex_df[spacex_df['Launch Site'] == selected_option]
        counts_df = new_df['class'].value_counts().reset_index()
        counts_df.columns = ['class', 'count']

        fig1 = px.pie(
            counts_df,
            names='class',
            values='count',
            title=f'Success vs Failure for site {selected_option}'
        )

        return fig1
        

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'), 
    Input(component_id='payload-slider', component_property='value')]
)
def update_output(selected_option, slider_option):

    if selected_option == 'ALL sites':
        fig2=px.scatter(spacex_df, 
            x='Payload Mass (kg)', y='class',
            color ="Booster Version Category",
            title='CORRELATION BETWEEN PAYLOAD AND LAUNCH SUCCESS'),
        return fig2

    elif selected_option != 'ALL':
        filtered_df = spacex_df[spacex_df[['Payload Mass (kg)', 'class']]==selected_option]
        fin_df = filtered_df[['Payload Mass (kg)', 'class','Booster Version Category']]

        fig3=px.scatter(fin_df, 
            x='Payload Mass (kg)', y='class',
            color = "Booster Version Category",
            title=f'CORRELATION BETWEEN PAYLOAD AND LAUNCH SUCCESS FROM {selected_option}'),
        return fig3

# Run the app
if __name__ == '__main__':
    app.run(debug=True, port=8002)
