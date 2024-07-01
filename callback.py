import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

# Load the dataset
url = 'https://raw.githubusercontent.com/jbrownlee/Datasets/master/airline-passengers.csv'
data = pd.read_csv(url)
data.columns = ['date', 'passengers']

# Get year and month columns
data['date'] = pd.to_datetime(data['date'])
data['year'] = data['date'].dt.year
data['month'] = data['date'].dt.month

# Initialize the Dash app
app = dash.Dash(__name__)
server = app.server
# Layout of the app
app.layout = html.Div([
    html.H1("Airline Passengers Data"),  #giving a header
    dcc.Dropdown(            #creating the dropdown menu
        id='year-dropdown',
        options=[{'label': str(year), 'value': year} for year in data['year'].unique()],
        value=data['year'].min(),
        style={'width': '200px'}
    ),
    dcc.Graph(id='passengers-graph')
])

# Callback to update graph based on selected year by the user
@app.callback(
    Output('passengers-graph', 'figure'),
    [Input('year-dropdown', 'value')]
)
#the function which will filter the data and create the graph depending on the user's selection
def update_figure(selected_year):
    filtered_data = data[data['year'] == selected_year]
    fig = px.line(filtered_data, x='month', y='passengers', title=f'Monthly Airline Passengers for {selected_year}',
                  labels={'month': 'Month', 'passengers': 'Number of Passengers'})
    fig.update_layout(
        yaxis=dict(range=[data['passengers'].min(), data['passengers'].max()])  # Fixed y-axis range
    )
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
