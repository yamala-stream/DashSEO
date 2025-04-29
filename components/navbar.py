import dash
import dash_bootstrap_components as dbc
from dash import html

def create_navbar():
    """Create the top navigation bar"""
    return dbc.Navbar(
        dbc.Container([
            # Logo/brand
            dbc.NavbarBrand([
                html.Img(src="/assets/images/logo.png", height="30px", className="me-2"),
                "SEO Prompt Generator"
            ], href="/"),
            
            # Responsive toggle for mobile
            dbc.NavbarToggler(id="navbar-toggler"),
            
            # Navbar items
            dbc.Collapse(
                dbc.Nav([
                    dbc.NavItem(dbc.NavLink("Dashboard", href="/")),
                    dbc.NavItem(dbc.NavLink("Generate", href="/generator")),
                    dbc.NavItem(dbc.NavLink("Templates", href="/templates")),
                    dbc.NavItem(dbc.NavLink("Keywords", href="/keywords")),
                    dbc.NavItem(dbc.NavLink("Analytics", href="/analytics")),
                    dbc.NavItem(dbc.NavLink("Settings", href="/settings")),
                ], navbar=True),
                id="navbar-collapse",
                navbar=True,
            ),
            
            # Right-aligned items (settings, notifications, etc.)
            dbc.Nav([
                dbc.NavItem(dbc.NavLink(html.I(className="fas fa-bell"), href="#")),
                dbc.NavItem(dbc.NavLink(html.I(className="fas fa-cog"), href="/settings")),
            ], navbar=True, className="ms-auto")
        ], fluid=True),
        color="primary",
        dark=True,
        className="mb-4",
    )