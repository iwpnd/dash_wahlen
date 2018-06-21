import os
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd

app = dash.Dash()

wahlen_df = pd.read_csv('./data/wahlen.csv')
wahlen_df['beteiligung'] = wahlen_df.waehler / wahlen_df.waehler_be

wahlen_pv = pd.pivot_table(
    wahlen_df, 
    index=['bezirkname'], 
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

cdu = go.Bar(x=wahlen_pv.index, y=wahlen_df['cdu_p'], name='CDU')
spd = go.Bar(x=wahlen_pv.index, y=wahlen_df['spd_p'], name='SPD')
linke = go.Bar(x=wahlen_pv.index, y=wahlen_df['linke_p'], name='DIE LINKE')
gruene = go.Bar(x=wahlen_pv.index, y=wahlen_df['gruene_p'], name='GRUENE')
afd = go.Bar(x=wahlen_pv.index, y=wahlen_df['afd_p'], name='AfD')
piraten = go.Bar(x=wahlen_pv.index, y=wahlen_df['piraten_p'], name='Piraten')
fdp = go.Bar(x=wahlen_pv.index, y=wahlen_df['fdp_p'], name='FDP')


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
                    x=wahlen_df[wahlen_df['bezirkname'] == i]['afd_p'],
                    y=wahlen_df[wahlen_df['bezirkname'] == i]['beteiligung'],
                    text=wahlen_df[wahlen_df['bezirkname'] == i]['wahlbezirk'],
                    mode='markers',
                    opacity=0.3,
                    marker={
                        'size': 15,
                        'line': {'width': 0.5, 'color': 'white'}
                        },
                        name = i
                ) for i in wahlen_df.bezirkname.unique()
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
