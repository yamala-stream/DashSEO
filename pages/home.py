import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

# Register the page
dash.register_page(__name__, path='/', title='Dashboard - SEO Prompt Generator')

# Layout for the home/dashboard page
def layout():
    return html.Div([
        # Page header
        html.H1("Dashboard", className="page-header"),
        html.P("Overview of your SEO prompt generation activity", className="lead"),
        
        # Stats row
        dbc.Row([
            dbc.Col(
                dbc.Card([
                    dbc.CardBody([
                        html.H2("125", className="card-title text-center"),
                        html.P("Total Prompts", className="card-text text-center text-muted")
                    ])
                ]),
                width=3
            ),
            dbc.Col(
                dbc.Card([
                    dbc.CardBody([
                        html.H2("12", className="card-title text-center"),
                        html.P("Templates", className="card-text text-center text-muted")
                    ])
                ]),
                width=3
            ),
            dbc.Col(
                dbc.Card([
                    dbc.CardBody([
                        html.H2("253", className="card-title text-center"),
                        html.P("Keywords", className="card-text text-center text-muted")
                    ])
                ]),
                width=3
            ),
            dbc.Col(
                dbc.Card([
                    dbc.CardBody([
                        html.H2("+15%", className="card-title text-center text-success"),
                        html.P("Weekly Growth", className="card-text text-center text-muted")
                    ])
                ]),
                width=3
            ),
        ], className="mb-4"),
        
        # Recent activity and charts
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Recent Activity"),
                    dbc.CardBody([
                        html.P("Placeholder for recent activity list")
                        # Will be replaced with actual activity list
                    ])
                ])
            ], width=6),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Prompt Generation Trend"),
                    dbc.CardBody([
                        dcc.Graph(
                            figure={
                                'data': [{'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar'}],
                                'layout': {'title': 'Placeholder Chart'}
                            },
                            id='dashboard-chart'
                        )
                    ])
                ])
            ], width=6)
        ])
    ])