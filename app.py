import dash
import dash_bootstrap_components as dbc
from config import APP_TITLE, APP_DESCRIPTION, DEFAULT_THEME

# Initialize the app with theme
app = dash.Dash(
    __name__,
    external_stylesheets=[getattr(dbc.themes, DEFAULT_THEME)],
    use_pages=True,
    suppress_callback_exceptions=True,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"},
        {"name": "description", "content": APP_DESCRIPTION}  # Add description directly here
    ],
)

# Set app title
app.title = APP_TITLE

# For gunicorn deployment
server = app.server