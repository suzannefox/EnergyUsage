import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objects as go

# Load the dataset
df = pd.read_csv('./data-cumulative/cumulative.csv')
df['day'] = pd.to_datetime(df['day'])

# Get min and max dates for range selection
min_date = df['day'].min()
max_date = df['day'].max()

# Initialize the Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Date Range Filter Example"),
    
    html.Div([
        html.Label("Date From"),
        dcc.DatePickerSingle(
            id='date-from',
            min_date_allowed=min_date,
            max_date_allowed=max_date,
            date=min_date
        ),
        html.Label("Date To"),
        dcc.DatePickerSingle(
            id='date-to',
            min_date_allowed=min_date,
            max_date_allowed=max_date,
            date=max_date
        ),
    ], style={'display': 'flex', 'gap': '20px'}),
    
    html.Div(id='error-message', style={'color': 'red'}),
    
    dcc.Graph(id='consumption-graph'),
    
    html.H3("Filtered Data"),
    dash_table.DataTable(id='data-table', page_size=10)
])

@app.callback(
    [Output('consumption-graph', 'figure'),
     Output('data-table', 'data'),
     Output('error-message', 'children')],
    [Input('date-from', 'date'),
     Input('date-to', 'date')]
)
def update_graph(date_from, date_to):
    if pd.to_datetime(date_from) > pd.to_datetime(date_to):
        return go.Figure(), [], "'Date From' must be earlier than 'Date To'"
    
    df_filtered = df[(df['day'] >= pd.to_datetime(date_from)) & (df['day'] <= pd.to_datetime(date_to))]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_filtered['x_label'], 
        y=df_filtered['electricity_consumption'], 
        mode='lines+markers', 
        name='Electricity', 
        line=dict(color='blue')
    ))
    
    fig.add_trace(go.Scatter(
        x=df_filtered['x_label'], 
        y=df_filtered['gas_consumption'], 
        mode='lines+markers', 
        name='Gas', 
        line=dict(color='red')
    ))
    
    fig.update_layout(
        title="Energy Consumption Over Time",
        xaxis_title="Time Interval (Start)",
        yaxis_title="Consumption",
        xaxis=dict(tickangle=45),
        template="plotly_white"
    )
    
    return fig, df_filtered.to_dict('records'), ""

if __name__ == '__main__':
    app.run_server(debug=True)