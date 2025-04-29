import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, callback, Input, Output

def create_sidebar():
    """Create the sidebar navigation"""
    return html.Div([
        # User section at top
        html.Div([
            html.H5("SEO Prompt Generator", className="sidebar-header"),
            html.P("Navigation", className="text-muted")
        ], className="sidebar-header"),
        
        # Navigation links
        dbc.Nav([
            dbc.NavLink([
                html.I(className="fas fa-home me-2"),
                html.Span("Dashboard")
            ], href="/", active="exact"),
            
            dbc.NavLink([
                html.I(className="fas fa-edit me-2"),
                html.Span("Generate Prompt")
            ], href="/generator", active="exact"),
            
            dbc.NavLink([
                html.I(className="fas fa-file-alt me-2"),
                html.Span("Templates")
            ], href="/templates", active="exact"),
            
            dbc.NavLink([
                html.I(className="fas fa-key me-2"),
                html.Span("Keywords")
            ], href="/keywords", active="exact"),
            
            dbc.NavLink([
                html.I(className="fas fa-chart-bar me-2"),
                html.Span("Analytics")
            ], href="/analytics", active="exact"),
            
            dbc.NavLink([
                html.I(className="fas fa-cog me-2"),
                html.Span("Settings")
            ], href="/settings", active="exact"),
        ], vertical=True, pills=True, className="sidebar-nav"),
        
        # Stats at bottom
        html.Div([
            html.Hr(),
            html.P("Quick Stats", className="text-muted"),
            html.Div([
                html.P("Total Prompts: 125", className="mb-1"),
                html.P("Templates: 12", className="mb-1"),
                html.P("Keywords: 253", className="mb-1")
            ])
        ], className="sidebar-footer")
    ], className="sidebar")

# Callback to highlight active page
@callback(
    Output({"type": "sidebar-link", "index": dash.ALL}, "active"),
    [Input("url", "pathname")]
)
def set_active_link(pathname):
    # Implementation of active link highlighting
    pass