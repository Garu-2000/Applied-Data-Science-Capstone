# Import required libraries
import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

# Read the SpaceX data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),

    # TASK 1: Dropdown list for Launch Site selection
    dcc.Dropdown(
        id='site-dropdown',
        options=[
            {'label': 'All Sites', 'value': 'ALL'},
            {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
            {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
            {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
            {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
        ],
        value='ALL',
        placeholder="Select a Launch Site here",
        searchable=True
    ),
    html.Br(),

    # TASK 2: Pie Chart for total successful launches
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),

    html.P("Payload range (Kg):"),

    # TASK 3: Slider for Payload selection
    dcc.RangeSlider(
        id='payload-slider',
        min=0, max=10000, step=1000,
        value=[min_payload, max_payload],
        marks={i: str(i) for i in range(0, 10001, 2500)},
        tooltip={"placement": "bottom", "always_visible": True}
    ),

    # TASK 4: Scatter Chart for payload success correlation
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

# TASK 2: Callback for Pie Chart
@app.callback(
    Output('success-pie-chart', 'figure'),
    Input('site-dropdown', 'value')
)
def update_pie_chart(selected_site):
    if selected_site == 'ALL':
        success_counts = spacex_df[spacex_df['class'] == 1].groupby('Launch Site').count()['class']
        fig = px.pie(names=success_counts.index, values=success_counts.values,
                     title="Total Successful Launches by Site")
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == selected_site]
        success_vs_failure = filtered_df['class'].value_counts()
        fig = px.pie(names=success_vs_failure.index, values=success_vs_failure.values,
                     title=f"Success vs. Failure for {selected_site}")
    return fig

# TASK 4: Callback for Scatter Chart
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [Input('site-dropdown', 'value'),
     Input('payload-slider', 'value')]
)
def update_scatter_chart(selected_site, payload_range):
    filtered_df = spacex_df[
        (spacex_df['Payload Mass (kg)'] >= payload_range[0]) &
        (spacex_df['Payload Mass (kg)'] <= payload_range[1])
    ]

    if selected_site == 'ALL':
        fig = px.scatter(filtered_df, x="Payload Mass (kg)", y="class",
                         color="Booster Version Category",
                         title="Correlation between Payload and Success for all Sites")
    else:
        filtered_df = filtered_df[filtered_df['Launch Site'] == selected_site]
        fig = px.scatter(filtered_df, x="Payload Mass (kg)", y="class",
                         color="Booster Version Category",
                         title=f"Correlation between Payload and Success for {selected_site}")
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
