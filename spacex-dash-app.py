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

options_drop_down = []
options_drop_down.append({'label':'All sites', 'value':'ALL'})
for site in spacex_df['Launch Site'].unique():
    options_drop_down.append({'label':site, 'value':site})


# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                 dcc.Dropdown(id='site-dropdown',
                                                options=options_drop_down,
                                                value='ALL',
                                                placeholder="place holder here",
                                                searchable=True
                                                ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider', min=0, max=10000, step=1000, 
                                        marks={0: '0',100: '100'},
                                        value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        fig = px.pie(data_frame=spacex_df, values='class', 
        names='Launch Site', 
        title='Total success Lauches by Site')

        
        return fig
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        conteo = filtered_df[['class']].value_counts()
        df_conteo = conteo.reset_index()
        df_conteo.columns = ['Success', 'Total']
        
        fig = px.pie(data_frame=df_conteo, values='Total', 
        names='Success', 
        title='Total success Lauches by site' + entered_site)

       
        return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
              Input(component_id="payload-slider", component_property="value")])
def get_pie_chart(entered_site, entered_payload):
    print(type(entered_payload[0]))
    data = spacex_df[(spacex_df['Payload Mass (kg)'] >= entered_payload[0]) & (spacex_df['Payload Mass (kg)'] <= entered_payload[1])]
    if entered_site == 'ALL':
        fig = px.scatter(
                data_frame=data,
                x='Payload Mass (kg)', 
                y='class',
                color='Booster Version Category',
                title='Correlation between Payload and Success for all Sites',
                hover_name='Booster Version Category'
            )
        return fig
    else:
        filtered_df = data[data['Launch Site'] == entered_site]
        fig = px.scatter(
                data_frame=filtered_df,
                x='Payload Mass (kg)', 
                y='class',
                color='Booster Version Category',
                title='Correlation between Payload and Success for site ' + entered_site,
                hover_name='Booster Version Category'
            )
        return fig

# Run the app
if __name__ == '__main__':
    app.run()

