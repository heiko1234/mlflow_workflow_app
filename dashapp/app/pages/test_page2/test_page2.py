import dash
from dash import html, dcc


dash.register_page(__name__,"/testpage2")

# dash.register_page(
#     __name__,
#     path='/second',
#     title='Home Dashboard',
#     name='Home Dashboard'
# )



import pygal
import base64


# line_chart = pygal.Line()
# line_chart.title = 'Browser usage evolution (in %)'
# line_chart.x_labels = map(str, range(2002, 2013))
# line_chart.add('Firefox', [None, None,    0, 16.6,   25,   31, 36.4, 45.5, 46.3, 42.8, 37.1])
# line_chart.add('Chrome',  [None, None, None, None, None, None,    0,  3.9, 10.8, 23.8, 35.3])
# line_chart.add('IE',      [85.8, 84.6, 84.7, 74.5,   66, 58.6, 54.7, 44.8, 36.2, 26.6, 20.1])
# line_chart.add('Others',  [14.2, 15.4, 15.3,  8.9,    9, 10.4,  8.9,  5.8,  6.7,  6.8,  7.5])

# # fig = line_chart

# fig = line_chart.render()


# layout to render and display a svg image on page


# works
# layout = html.Div(
#     [
#         html.H1("This is a test page 2"),
#         dcc.Graph(
#             figure={
#                 "data": [
#                     {
#                         "x": [1, 2, 3],
#                         "y": [4, 1, 2],
#                         "type": "bar",
#                         "name": "SF",
#                     },
#                     {
#                         "x": [1, 2, 3],
#                         "y": [2, 4, 5],
#                         "type": "bar",
#                         "name": u"Montréal",
#                     },
#                 ],
#                 "layout": {"title": "Dash Data Visualization"},
#             }
#         ),
#         html.Img(src='data:image/svg+xml;base64,{}'.format(base64.b64encode(fig).decode()),style={'width':'100%','height':'100%'})
#     ]
# )





linechart = pygal.Line()
linechart.add('IE', [85.8, 84.6, 84.7, 74.5, 66, 58.6, 54.7, 44.8, 36.2, 26.6, 20.1])

fig = linechart.render()



chart = pygal.Line()
chart.add('', [1, 3, 5, 16, 13, 3, 7])
chart.x_labels = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
chart.render_sparkline(show_x_labels=True, show_y_labels=True)

fig2 = chart.render()



gauge_chart = pygal.Gauge(human_readable=True)
gauge_chart.title = 'DeltaBlue V8 benchmark results'
gauge_chart.range = [0, 10000]
gauge_chart.add('Chrome', 8212)
gauge_chart.add('Firefox', 8099)
gauge_chart.add('Opera', 2933)
gauge_chart.add('IE', 41)
gauge_chart.render()

fig3 = gauge_chart.render()



import plotly.express as px


df = px.data.gapminder().query("country=='Canada'")
fig4 = px.line(df, x="year", y="lifeExp")
# make fig4 show no axis , labels, or legend
fig4.update_layout(
    xaxis=dict(
        showgrid=False,
        showline=False,
        showticklabels=False,
        zeroline=False,
    ),
    yaxis=dict(
        showgrid=False,
        showline=False,
        showticklabels=False,
        zeroline=False,
    ),
    # legend=dict(
    #     orientation="h",
    #     yanchor="bottom",
    #     y=1.02,
    #     xanchor="right",
    #     x=1
    # )
)
# make y label not shown
fig4.update_yaxes(title=None)

# make background transparent
fig4.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
)

# make line thinkness a bit thicker
fig4.update_traces(line=dict(width=4))



# make a layout with a card of the svg image, it should be designed as sparkline with a title and a description



layout = html.Div(
    [
        html.H1("This is a test page 2"),
        html.Div(
            [
                html.Div(
                    [
                        html.H1("Figure1"),
                        html.Img(src='data:image/svg+xml;base64,{}'.format(base64.b64encode(fig).decode()),style={'width':'25%','height':'25%'})
                    ],
                    style={"width": "80%", "display": "flex", "align-items": "center", "justify-content": "center"},
                ),
                html.Div(
                    [
                        html.H1("Fig2"),
                        html.Img(src='data:image/svg+xml;base64,{}'.format(base64.b64encode(fig2).decode()),style={'width':'25%','height':'25%'})
                    ],
                    style={"width": "80%", "display": "flex", "align-items": "center", "justify-content": "center"},
                ),
                html.Div(
                    [
                        html.H1("Fig3"),
                        html.Img(src='data:image/svg+xml;base64,{}'.format(base64.b64encode(fig3).decode()),style={'width':'25%','height':'25%'})
                    ],
                    style={"width": "80%", "display": "flex", "align-items": "center", "justify-content": "center"},
                ),
                html.Div(
                    [
                        html.H1("Fig4"),
                        html.Div([dcc.Graph(figure=fig4)]),
                    ],
                    style={"width": "80%", "display": "flex", "align-items": "center", "justify-content": "center", "border": "1px solid black"},
                ),
            ],
            className="card",
        ),
    ]
)



