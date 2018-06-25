import os
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import geopandas as gpd
from derp import df_to_crs, relative_frequency_parties

app = dash.Dash()

# Amt für Statistik Berlin-Brandenburg 2017
# https://daten.berlin.de/datensaetze/geometrien-der-wahlbezirke-für-die-bundestagswahl-berlin-2017
# Amt für Statistik Berlin-Brandenburg 2017
# https://www.statistik-berlin-brandenburg.de/publikationen/dowmies/DL_BE_EE_WB_BU2017.xlsx
# load data into pandas dataframe
gdf = gpd.read_file('./data/RBS_OD_UWB.shp', encoding='ISO-8859-1')
gdf = gdf.sort_values('UWB').reset_index()
df = pd.read_excel('./data/DL_BE_EE_WB_BU2017.xlsx', sheet_name='BE_W2')

# normalize wahlbezirk to allow merge with gdf
df['Adresse'] = df['Adresse'].str.replace('W', '')

# merge and subset
data = gdf.merge(df, left_on='UWB', right_on='Adresse')
data = data[['UWB', 'UWB3', 'BWB', 'BWB2', 'AWK', 'BEZ', 'BEZNAME', 'BWK', 'OW', 'OstWest', 'Wahlberechtigte insgesamt', 'Wähler', 'Ungültige Stimmen', 'Gültige Stimmen', 'CDU',
             'SPD', 'DIE LINKE', 'GRÜNE', 'AfD', 'PIRATEN', 'FDP',
             'geometry', ]]

# list parties you want relative frequency of
parties = ['CDU', 'SPD', 'DIE LINKE', 'GRÜNE', 'AfD', 'PIRATEN', 'FDP']
data = relative_frequency_parties(data, parties)

data = df_to_crs(data, from_epsg='25833', to_epsg='4326')

data['beteiligung'] = data['Wähler'] / data['Wahlberechtigte insgesamt']

wahlen_pv = pd.pivot_table(
    data, 
    index=['BEZNAME'], 
    aggfunc=sum, 
    fill_value=0
    )

wahlen_pv.index = [
    'Charlottenburg-Wilmersdorf', 
    'Friedrichshain-Kreuzberg', 
    'Lichtenberg',
    'Marzahn-Hellersdorf', 
    'Mitte', 
    'Neukoelln', 
    'Pankow',
    'Reinickendorf', 
    'Spandau', 
    'Steglitz-Zehlendorf',
    'Tempelhof-Schoeneberg', 
    'Treptow-Koepenick'
    ]

cdu = go.Bar(x=wahlen_pv.index, y=data['CDU_p'], name='CDU')
spd = go.Bar(x=wahlen_pv.index, y=data['SPD_p'], name='SPD')
linke = go.Bar(x=wahlen_pv.index, y=data['DIE LINKE_p'], name='DIE LINKE')
gruene = go.Bar(x=wahlen_pv.index, y=data['GRÜNE_p'], name='GRUENE')
afd = go.Bar(x=wahlen_pv.index, y=data['AfD_p'], name='AfD')
piraten = go.Bar(x=wahlen_pv.index, y=data['PIRATEN_p'], name='Piraten')
fdp = go.Bar(x=wahlen_pv.index, y=data['FDP_p'], name='FDP')


app.layout = html.Div(children=[
    html.H1(children='Wahlergebnis Bundestagswahl 2017'),
    
    dcc.Graph(
        id='sgraph',
        config={
            'displayModeBar': False
        },
        figure={
            'data': [
                cdu, 
                gruene, 
                linke,
                spd,
                fdp,
                afd,
                piraten
                ],
            'layout':
            go.Layout(
                title='Anteil Zweitstimme pro Bezirk', 
                barmode='stack'
                )
        }),
      
    dcc.Graph(
        id='b-vs-afdp',
        config={
            'displayModeBar': False
        },
        figure={
            'data': [
                go.Scatter(
                    x=data[data['BEZNAME'] == i]['AfD_p'],
                    y=data[data['BEZNAME'] == i]['beteiligung'],
                    text=data[data['BEZNAME'] == i]['BEZ'],
                    mode='markers',
                    opacity=0.3,
                    marker={
                        'size': 15,
                        'line': {'width': 0.5, 'color': 'white'}
                        },
                        name = i
                ) for i in data.BEZNAME.unique()
                ],
            'layout':
                go.Layout(
                    #title='Wahlbeteilung im Bezirk vs Wahlergebnis AfD',
                    xaxis={'title': 'Wahlergebnis AfD'},
                    yaxis={'title': 'Wahlbeteiligung in %'},
                    margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                    legend={'x': 10, 'y': 0},
                    hovermode='closest'
            )
        }
    )

])


if __name__ == '__main__':
    app.run_server(debug=True)
