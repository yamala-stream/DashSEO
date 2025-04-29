import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from app import app
from components.navbar import create_navbar
from components.sidebar import create_sidebar

# Main app layout
app.layout = html.Div([
    # Store for app state
    dcc.Store(id='app-state', storage_type='session'),
    
    # Main layout with navbar and content area
    create_navbar(),
    
    # Page content with sidebar
    dbc.Container([
        dbc.Row([
            # Sidebar
            dbc.Col(create_sidebar(), width=2, className="sidebar-col"),
            
            # Main content area
            dbc.Col([
                dash.page_container
            ], width=10, className="content-col")
        ])
    ], fluid=True, className="mt-4")
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)