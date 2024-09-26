import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

# Verileri CSV dosyasından yükle
url = 'https://covid.ourworldindata.org/data/owid-covid-data.csv'
df = pd.read_csv(url)

# Ülkeler listesi
countries = df['location'].unique()

# Dash uygulamasını oluştur
app = dash.Dash(__name__)

# Uygulama düzeni
app.layout = html.Div([
    html.H1("COVID-19 Ölüm Oranları Zaman Serisi"),
    
    html.Label("Ülke Seçin:"),
    dcc.Dropdown(
        id='country-dropdown',
        options=[{'label': country, 'value': country} for country in countries],
        value='Turkey',  # Varsayılan olarak Türkiye seçili
    ),

    dcc.Graph(id='time-series')
])

# Callback fonksiyonu - Zaman Serisi Grafik
@app.callback(
    Output('time-series', 'figure'),
    [Input('country-dropdown', 'value')]
)
def update_time_series(country):
    country_df = df[df['location'] == country]

    fig = px.line(
        country_df,
        x='date',
        y='total_deaths_per_million',
        title=f"{country} COVID-19 Ölüm Oranı Zaman Serisi",
        labels={'total_deaths_per_million': 'Ölüm Oranı (Milyonda)', 'date': 'Tarih'},
    )
    fig.update_xaxes(title_text="Tarih")
    fig.update_yaxes(title_text="Ölüm Oranı (Milyonda)")
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
    

