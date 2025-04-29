import dash
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Register the page
dash.register_page(__name__, path='/analytics', title='Analytics - SEO Prompt Generator')

def layout():
    """
    Main layout for the analytics dashboard
    """
    return html.Div([
        html.H1("Analytics Dashboard", className="page-header"),
        html.P("View performance metrics for your SEO prompt generator", className="lead mb-4"),
        
        dbc.Tabs([
            dbc.Tab([render_prompt_usage_content()], label="Prompt Usage"),
            dbc.Tab([render_template_performance_content()], label="Template Performance"),
            dbc.Tab([render_keyword_trends_content()], label="Keyword Trends")
        ], id="analytics-tabs")
    ])

def render_prompt_usage_content():
    """
    Content for prompt usage tab
    """
    return html.Div([
        html.H2("Prompt Generation Overview", className="mt-4 mb-3"),
        
        # Summary metrics cards row
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H2(id="total-prompts-metric", className="text-center"),
                        html.P("Total Prompts", className="text-center text-muted")
                    ])
                ])
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H2(id="unique-keywords-metric", className="text-center"),
                        html.P("Unique Keywords", className="text-center text-muted")
                    ])
                ])
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H2(id="categories-metric", className="text-center"),
                        html.P("Categories", className="text-center text-muted")
                    ])
                ])
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H2(id="weekly-trend-metric", className="text-center"),
                        html.P("Weekly Trend", className="text-center text-muted")
                    ])
                ])
            ], width=3),
        ], className="mb-4"),
        
        # Prompt generation over time chart
        html.H3("Prompt Generation Over Time", className="mt-4 mb-3"),
        dcc.Graph(id="prompt-time-chart", figure={}, className="mb-4"),
        
        # Category distribution chart
        html.H3("Prompts by Category", className="mt-4 mb-3"),
        dcc.Graph(id="category-distribution-chart", figure={}, className="mb-4"),
        
        # Recent prompts table
        html.H3("Recent Prompts", className="mt-4 mb-3"),
        html.Div(id="recent-prompts-table")
    ])

def render_template_performance_content():
    """
    Content for template performance tab
    """
    return html.Div([
        html.H2("Template Performance Analysis", className="mt-4 mb-3"),
        
        # Template usage chart
        html.H3("Template Usage Comparison", className="mt-4 mb-3"),
        dcc.Graph(id="template-usage-chart", figure={}, className="mb-4"),
        
        # Template usage over time chart
        html.H3("Template Usage Over Time", className="mt-4 mb-3"),
        dcc.Graph(id="template-time-chart", figure={}, className="mb-4"),
        
        # Template performance metrics table
        html.H3("Template Performance Metrics", className="mt-4 mb-3"),
        html.Div(id="template-metrics-table")
    ])

def render_keyword_trends_content():
    """
    Content for keyword trends tab
    """
    return html.Div([
        html.H2("Keyword Trends and Analysis", className="mt-4 mb-3"),
        
        # Top keywords chart
        html.H3("Top Primary Keywords", className="mt-4 mb-3"),
        dcc.Graph(id="top-keywords-chart", figure={}, className="mb-4"),
        
        # Keyword usage by category
        html.H3("Keyword Usage by Category", className="mt-4 mb-3"),
        dcc.Graph(id="keyword-category-chart", figure={}, className="mb-4"),
        
        # Keyword trends over time
        html.H3("Keyword Trends Over Time", className="mt-4 mb-3"),
        dcc.Graph(id="keyword-trends-chart", figure={}, className="mb-4")
    ])

# Callbacks for Prompt Usage tab
@callback(
    [Output("total-prompts-metric", "children"),
     Output("unique-keywords-metric", "children"),
     Output("categories-metric", "children"),
     Output("weekly-trend-metric", "children")],
    [Input("analytics-tabs", "active_tab")]
)
def update_prompt_metrics(active_tab):
    """Update the prompt usage metric cards"""
    # In a real implementation, this would fetch data from the database
    # Here we're using sample data for illustration
    
    from services.analytics_service import get_prompt_metrics
    metrics = get_prompt_metrics()
    
    # Format the weekly trend with sign and percentage
    if metrics["weekly_trend"] > 0:
        trend_display = f"+{metrics['weekly_trend']:.1f}%"
    else:
        trend_display = f"{metrics['weekly_trend']:.1f}%"
    
    return (
        str(metrics["total_prompts"]),
        str(metrics["unique_keywords"]),
        str(metrics["categories"]),
        trend_display
    )

@callback(
    Output("prompt-time-chart", "figure"),
    [Input("analytics-tabs", "active_tab")]
)
def update_prompt_time_chart(active_tab):
    """Update the prompt generation over time chart"""
    # In a real implementation, fetch this data from the database
    
    from services.analytics_service import get_prompt_time_data
    time_data = get_prompt_time_data()
    
    fig = px.line(
        time_data, 
        x="date", 
        y="count",
        title="Prompts Generated by Day",
        labels={"date": "Date", "count": "Number of Prompts"}
    )
    
    # Customize the layout
    fig.update_layout(
        height=400,
        margin=dict(l=20, r=20, t=40, b=20),
        plot_bgcolor="white",
        paper_bgcolor="white",
        hovermode="closest"
    )
    
    return fig

@callback(
    Output("category-distribution-chart", "figure"),
    [Input("analytics-tabs", "active_tab")]
)
def update_category_chart(active_tab):
    """Update the category distribution chart"""
    # In a real implementation, fetch this data from the database
    
    from services.analytics_service import get_category_distribution
    category_data = get_category_distribution()
    
    fig = px.bar(
        category_data,
        x="category",
        y="count",
        title="Prompts by Content Category",
        labels={"category": "Category", "count": "Number of Prompts"}
    )
    
    # Customize the layout
    fig.update_layout(
        height=400,
        margin=dict(l=20, r=20, t=40, b=20),
        plot_bgcolor="white",
        paper_bgcolor="white",
        hovermode="closest"
    )
    
    return fig

@callback(
    Output("recent-prompts-table", "children"),
    [Input("analytics-tabs", "active_tab")]
)
def update_recent_prompts_table(active_tab):
    """Update the recent prompts table"""
    # In a real implementation, fetch this data from the database
    
    from services.analytics_service import get_recent_prompts
    recent_prompts_df = get_recent_prompts()
    
    if recent_prompts_df.empty:
        return html.Div("No prompt data available yet. Generate some prompts first!", className="text-center p-4")
    
    # Create a formatted table
    table_header = [
        html.Thead(html.Tr([
            html.Th("Timestamp"),
            html.Th("Template"),
            html.Th("Primary Keyword"),
            html.Th("Category"),
            html.Th("Audience")
        ]))
    ]
    
    rows = []
    for _, row in recent_prompts_df.iterrows():
        rows.append(html.Tr([
            html.Td(row["timestamp"]),
            html.Td(row["template_id"]),
            html.Td(row["primary_keyword"]),
            html.Td(row["category"]),
            html.Td(row["audience"])
        ]))
    
    table_body = [html.Tbody(rows)]
    
    table = dbc.Table(
        table_header + table_body,
        bordered=True,
        hover=True,
        responsive=True,
        striped=True
    )
    
    return table

# Callbacks for Template Performance tab
@callback(
    Output("template-usage-chart", "figure"),
    [Input("analytics-tabs", "active_tab")]
)
def update_template_usage_chart(active_tab):
    """Update the template usage comparison chart"""
    
    from services.analytics_service import get_template_usage
    template_usage_df = get_template_usage()
    
    if template_usage_df.empty:
        # Return empty figure with message
        fig = go.Figure()
        fig.update_layout(
            title="No template usage data available yet",
            annotations=[dict(
                text="Generate some prompts to see template usage data",
                showarrow=False,
                xref="paper",
                yref="paper",
                x=0.5,
                y=0.5
            )]
        )
        return fig
    
    fig = px.bar(
        template_usage_df,
        x="template_id",
        y="usage_count",
        title="Template Usage Count",
        labels={"template_id": "Template", "usage_count": "Usage Count"}
    )
    
    # Customize the layout
    fig.update_layout(
        height=400,
        margin=dict(l=20, r=20, t=40, b=20),
        plot_bgcolor="white",
        paper_bgcolor="white",
        hovermode="closest"
    )
    
    return fig

@callback(
    Output("template-time-chart", "figure"),
    [Input("analytics-tabs", "active_tab")]
)
def update_template_time_chart(active_tab):
    """Update the template usage over time chart"""
    
    from services.analytics_service import get_template_time_data
    template_time_data = get_template_time_data()
    
    if template_time_data.empty:
        # Return empty figure with message
        fig = go.Figure()
        fig.update_layout(
            title="No template time-series data available yet",
            annotations=[dict(
                text="Generate more prompts to see template usage over time",
                showarrow=False,
                xref="paper",
                yref="paper",
                x=0.5,
                y=0.5
            )]
        )
        return fig
    
    fig = px.line(
        template_time_data,
        x="date",
        y="count",
        color="template_id",
        title="Template Usage Over Time",
        labels={"date": "Date", "count": "Number of Prompts", "template_id": "Template"}
    )
    
    # Customize the layout
    fig.update_layout(
        height=400,
        margin=dict(l=20, r=20, t=40, b=20),
        plot_bgcolor="white",
        paper_bgcolor="white",
        hovermode="closest",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    return fig

@callback(
    Output("template-metrics-table", "children"),
    [Input("analytics-tabs", "active_tab")]
)
def update_template_metrics_table(active_tab):
    """Update the template metrics table"""
    
    from services.analytics_service import get_template_metrics
    template_metrics_df = get_template_metrics()
    
    if template_metrics_df.empty:
        return html.Div("No template metrics available yet. Generate some prompts first!", className="text-center p-4")
    
    # Create a formatted table
    table_header = [
        html.Thead(html.Tr([
            html.Th("Template Name"),
            html.Th("Usage Count"),
            html.Th("Keyword Diversity"),
            html.Th("Last Used")
        ]))
    ]
    
    rows = []
    for _, row in template_metrics_df.iterrows():
        rows.append(html.Tr([
            html.Td(row["Template Name"]),
            html.Td(row["usage_count"]),
            html.Td(row["keyword_diversity"]),
            html.Td(row["Last Used"])
        ]))
    
    table_body = [html.Tbody(rows)]
    
    table = dbc.Table(
        table_header + table_body,
        bordered=True,
        hover=True,
        responsive=True,
        striped=True
    )
    
    return table

# Callbacks for Keyword Trends tab
@callback(
    Output("top-keywords-chart", "figure"),
    [Input("analytics-tabs", "active_tab")]
)
def update_top_keywords_chart(active_tab):
    """Update the top keywords chart"""
    
    from services.analytics_service import get_top_keywords
    top_keywords_df = get_top_keywords()
    
    if top_keywords_df.empty:
        # Return empty figure with message
        fig = go.Figure()
        fig.update_layout(
            title="No keyword data available yet",
            annotations=[dict(
                text="Add keywords and generate prompts to see keyword usage data",
                showarrow=False,
                xref="paper",
                yref="paper",
                x=0.5,
                y=0.5
            )]
        )
        return fig
    
    fig = px.bar(
        top_keywords_df,
        x="keyword",
        y="usage_count",
        title="Top 10 Primary Keywords by Usage",
        labels={"keyword": "Keyword", "usage_count": "Usage Count"}
    )
    
    # Customize the layout
    fig.update_layout(
        height=400,
        margin=dict(l=20, r=20, t=40, b=20),
        plot_bgcolor="white",
        paper_bgcolor="white",
        hovermode="closest"
    )
    
    return fig

@callback(
    Output("keyword-category-chart", "figure"),
    [Input("analytics-tabs", "active_tab")]
)
def update_keyword_category_chart(active_tab):
    """Update the keyword usage by category chart"""
    
    from services.analytics_service import get_keyword_category_data
    keyword_category_data = get_keyword_category_data()
    
    if keyword_category_data.empty:
        # Return empty figure with message
        fig = go.Figure()
        fig.update_layout(
            title="No keyword category data available yet",
            annotations=[dict(
                text="Generate more prompts with different categories to see this data",
                showarrow=False,
                xref="paper",
                yref="paper",
                x=0.5,
                y=0.5
            )]
        )
        return fig
    
    fig = px.bar(
        keyword_category_data,
        x="primary_keyword",
        y="count",
        color="category",
        title="Top Keywords by Category",
        labels={"primary_keyword": "Keyword", "count": "Number of Prompts", "category": "Category"}
    )
    
    # Customize the layout
    fig.update_layout(
        height=400,
        margin=dict(l=20, r=20, t=40, b=20),
        plot_bgcolor="white",
        paper_bgcolor="white",
        hovermode="closest",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    return fig

@callback(
    Output("keyword-trends-chart", "figure"),
    [Input("analytics-tabs", "active_tab")]
)
def update_keyword_trends_chart(active_tab):
    """Update the keyword trends over time chart"""
    
    from services.analytics_service import get_keyword_trends_data
    keyword_trends_data = get_keyword_trends_data()
    
    if keyword_trends_data.empty:
        # Return empty figure with message
        fig = go.Figure()
        fig.update_layout(
            title="No keyword trend data available yet",
            annotations=[dict(
                text="Generate more prompts over time to see keyword usage trends",
                showarrow=False,
                xref="paper",
                yref="paper",
                x=0.5,
                y=0.5
            )]
        )
        return fig
    
    fig = px.line(
        keyword_trends_data,
        x="date",
        y="count",
        color="primary_keyword",
        title="Keyword Usage Over Time",
        labels={"date": "Date", "count": "Number of Prompts", "primary_keyword": "Keyword"}
    )
    
    # Customize the layout
    fig.update_layout(
        height=400,
        margin=dict(l=20, r=20, t=40, b=20),
        plot_bgcolor="white",
        paper_bgcolor="white",
        hovermode="closest",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    return fig