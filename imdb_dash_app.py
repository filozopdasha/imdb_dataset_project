import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output

df = pd.read_csv('title.basics.tsv', sep='\t', usecols=['tconst', 'startYear', 'genres'])
df = df.dropna(subset=['startYear', 'genres'])
df['startYear'] = pd.to_numeric(df['startYear'], errors='coerce')
df = df.dropna(subset=['startYear'])
df = df[df['genres'].str.strip() != '']
df['genres'] = df['genres'].str.split(',')
df = df.explode('genres')

min_year = int(df['startYear'].min())
max_year = int(df['startYear'].max())

app = Dash(__name__)

app.layout = html.Div([
    html.H1("Genre Popularity by Year Range"),

    html.Label("Select Year Range:"),
    dcc.RangeSlider(
        id='year-range-slider',
        min=min_year,
        max=max_year,
        value=[1990, 2000],
        marks={year: str(year) for year in range(min_year, max_year + 1, 10)},
        step=1
    ),

    dcc.Graph(id='genre-bar-chart')
])


@app.callback(
    Output('genre-bar-chart', 'figure'),
    Input('year-range-slider', 'value')
)
def update_chart(year_range):
    start_year, end_year = year_range
    filtered_data = df[(df['startYear'] >= start_year) & (df['startYear'] <= end_year)]

    genre_counts = filtered_data['genres'].value_counts().reset_index()
    genre_counts.columns = ['genres', 'count']

    fig = go.Figure(data=[
        go.Bar(x=genre_counts['genres'], y=genre_counts['count'])
    ])

    fig.update_layout(
        title=f"Genre Popularity from {start_year} to {end_year}",
        xaxis_title="Genres",
        yaxis_title="Number of Movies"
    )
    return fig


if __name__ == '__main__':
    app.run(debug=True)