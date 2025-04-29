import dash_bootstrap_components as dbc
from dash import html

def create_template_card(template):
    """Create a card component for template selection"""
    return dbc.Card([
        dbc.CardHeader(template.get("name", "Template")),
        dbc.CardBody([
            html.P(f"Category: {template.get('category', 'General')}", className="card-text"),
            html.P(f"Type: {template.get('schema', 'Article')}", className="card-text"),
            dbc.Button("Select", id={"type": "select-template", "index": template.get("id", "")}, 
                      color="primary", size="sm", className="mt-2")
        ])
    ], className="h-100 template-card mb-3")