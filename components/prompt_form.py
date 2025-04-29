import dash_bootstrap_components as dbc
from dash import html, dcc

def create_prompt_form(template=None):
    """Create a form for prompt generation based on template"""
    # Default form if no template is provided
    if template is None:
        return html.Div([
            dbc.Alert("Please select a template first", color="warning")
        ])
    
    # Simple form based on template
    return dbc.Form([
        # Template info
        html.H4(template.get("name", "Template"), className="mb-3"),
        html.P(template.get("description", ""), className="mb-4"),
        
        # Primary keyword
        dbc.FormGroup([
            dbc.Label("Primary Keyword *"),
            dbc.Input(id="primary-keyword-input", type="text", placeholder="Enter primary keyword"),
            dbc.FormText("Main keyword to target in your content")
        ], className="mb-3"),
        
        # Secondary keywords
        dbc.FormGroup([
            dbc.Label("Secondary Keywords"),
            dbc.Input(id="secondary-keywords-input", type="text", 
                     placeholder="Enter secondary keywords, comma separated"),
            dbc.FormText("Supporting keywords to include in your content")
        ], className="mb-3"),
        
        # Source content
        dbc.FormGroup([
            dbc.Label("Source Content"),
            dbc.Textarea(id="source-content-input", placeholder="Enter source content or URL",
                        style={"height": "120px"}),
            dbc.FormText("Reference content or URL to base your prompt on")
        ], className="mb-3"),
        
        # Submit button
        dbc.Button("Generate Prompt", id="generate-prompt-button", 
                  color="primary", size="lg", className="mt-3 w-100")
    ])