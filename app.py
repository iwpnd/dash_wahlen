import os
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd

app = dash.Dash()

wahlen_df = pd.read_csv('wahlen.csv')
wahlen_df['beteiligung'] = wahlen_df.waehler / wahlen_df.waehler_be

wahlen_pv = pd.pivot_table(
    wahlen_df, 
    index=['bezirkname'], 
    aggfunc=sum, 
    fill_value=0
    )
wahlen_pv.index = ['Charlottenburg-Wilmersdorf', 'Friedrichshain-Kreuzberg', 'Lichtenberg',
                   'Marzahn-Hellersdorf', 'Mitte', 'Neukoelln', 'Pankow',
                   'Reinickendorf', 'Spandau', 'Steglitz-Zehlendorf',
                   'Tempelhof-Schoeneberg', 'Treptow-Koepenick']

trace1 = go.Bar(x=wahlen_pv.index, y=wahlen_df['cdu_p'], name='CDU')
trace2 = go.Bar(x=wahlen_pv.index, y=wahlen_df['spd_p'], name='SPD')
trace3 = go.Bar(x=wahlen_pv.index, y=wahlen_df['linke_p'], name='DIE LINKE')
trace4 = go.Bar(x=wahlen_pv.index, y=wahlen_df['gruene_p'], name='GRUENE')
trace5 = go.Bar(x=wahlen_pv.index, y=wahlen_df['afd_p'], name='AfD')
trace6 = go.Bar(x=wahlen_pv.index, y=wahlen_df['piraten_p'], name='Piraten')
trace7 = go.Bar(x=wahlen_pv.index, y=wahlen_df['fdp_p'], name='FDP')


app.layout = html.Div(children=[
    html.H1(children='Wahlergebnis Bundestagswahl 2017'),
    html.Div(),
    dcc.Graph(
        id='sgraph',
        config={
            'displayModeBar': False
        },
        figure={
            'data': [
                trace1,
                trace2, 
                trace3, 
                trace4,
                trace5,
                trace6,
                trace7
                ],
            'layout':
            go.Layout(title='Anteil Zweitstimme pro Bezirk', barmode='stack')
        })
])

if __name__ == '__main__':
    app.run_server(debug=True)