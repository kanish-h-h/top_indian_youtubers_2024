from dash import Dash, html, dash_table, dcc, Output, Input, callback
import pandas as pd
import numpy as np
import plotly.express as px

df = pd.read_csv('data/analysis.csv')

df_n = df.drop(['ID'], axis=1)
df_bar = df.sort_values(by='total_subscribers', ascending=False).head(10)   # for bar chart
df_treemap = df.sort_values(by='total_views', ascending=False).head(20)      # for Tree Map

# for treemap
fig = px.treemap(df_treemap,
                 path=['NAME'],
                 values='total_views',
                 hover_data=['NAME'],
                 color='total_views',
                 color_continuous_scale='RdBu',
                 color_continuous_midpoint=np.average(df['total_views'], weights=df['total_views']))
fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))


app = Dash()

app.layout = html.Div([
    # main heading
    html.Div(
        children='Top 10 INDIAN YouTubers',
        style={
            'textAlign': 'center',
            'fontWeight': 'bold',
            'fontSize': '32px',
            'marginBottom': '20px'
        }
    ),

    # Table
    html.Div([
        html.H2('Top 10 INDIAN YouTubers'),
        dash_table.DataTable(
            id='table',
            data=df_n.to_dict('records'),
            style_cell={'textAlign': 'left'},
            page_size=10,
            style_as_list_view=True,

            style_header={
                'backgroundColor': 'rgb(30,30,30)',
                'color': 'white'
            },

            style_data={
                'backgroundColor': 'rgb(50,50,50)',
                'color': 'white'
            }
        )
    ]),

    # Bar chart
    html.Div([
        html.H2('Top 10 Channels (by subscribers)'),
        dcc.Graph(id='bar_chart', figure=px.bar(df_bar, x='total_subscribers', y='NAME'))
    ]),

    # TreeMap
    html.Div([
        html.H2('Top 20 Channels (by views)'),
        dcc.Graph(id='treemap_chart', figure=fig)
    ])

])

# Save the app layout as a static HTML file
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

if __name__ == '__main__':
    app.run(debug=True)
