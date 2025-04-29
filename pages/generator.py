import dash
from dash import dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc
import pandas as pd
import re
import json
from datetime import date

from services.template_service import get_template, get_template_list, get_templates_by_category, save_prompt_generation
from utils.template_store import get_all_categories

# Register the page
dash.register_page(__name__, path='/generator', title='Generate Prompts - SEO Prompt Generator')

def layout():
    """Main layout for the generator page"""
    return html.Div([
        html.H1("Generate SEO Prompt", className="page-header"),
        html.P("Select a template and customize your prompt", className="lead mb-4"),
        
        # Template selection section
        html.Div([
            html.H2("Step 1: Select Template", className="mb-3"),
            
            # Template category and selection
            dbc.Row([
                dbc.Col([
                    html.Label("Choose a Category"),
                    dcc.Dropdown(
                        id="category-selector",
                        options=[{"label": cat["name"], "value": cat["id"]} for cat in get_all_categories()],
                        value=get_all_categories()[0]["id"] if get_all_categories() else None,
                        clearable=False,
                        className="mb-3"
                    )
                ], width=6),
                
                dbc.Col([
                    html.Label("Choose a Template"),
                    dcc.Dropdown(
                        id="template-selector",
                        options=[],  # Will be populated by callback
                        value=None,
                        clearable=False,
                        className="mb-3"
                    )
                ], width=6)
            ]),
            
            # Template info display
            html.Div(id="template-info", className="mb-4")
        ], className="mb-5"),
        
        # Prompt form (will be shown after template selection)
        html.Div(id="prompt-form-container"),
        
        # Generated prompt output
        html.Div(id="generated-prompt-container")
    ])

@callback(
    Output("template-selector", "options"),
    [Input("category-selector", "value")]
)
def update_template_options(selected_category):
    """Update template options based on selected category"""
    if not selected_category:
        return []
    
    templates_by_category = get_templates_by_category(selected_category)
    
    if selected_category in templates_by_category:
        templates = templates_by_category[selected_category]["templates"]
        return [{"label": template["name"], "value": template["id"]} for template in templates]
    
    return []

@callback(
    Output("template-info", "children"),
    [Input("template-selector", "value")]
)
def display_template_info(template_id):
    """Display information about the selected template"""
    if not template_id:
        return html.Div("Please select a template to continue", className="text-muted")
    
    template = get_template(template_id)
    
    return dbc.Card([
        dbc.CardBody([
            html.H4(template["name"], className="card-title"),
            dbc.Row([
                dbc.Col([
                    html.P([html.Strong("Intent: "), template.get("intent", template.get("use_case", "-"))]),
                ], width=4),
                dbc.Col([
                    html.P([html.Strong("Tone: "), template.get("tone", "-")]),
                ], width=4),
                dbc.Col([
                    html.P([html.Strong("Schema: "), template.get("schema", "-")]),
                ], width=4)
            ])
        ])
    ])

@callback(
    Output("prompt-form-container", "children"),
    [Input("template-selector", "value")]
)
def render_prompt_form(template_id):
    """Render the prompt generation form based on the selected template"""
    if not template_id:
        return html.Div()
    
    template = get_template(template_id)
    
    # Define major countries for target location dropdown
    major_countries = [
        "United States", "United Kingdom", "Canada", "Australia", "Germany", 
        "France", "Italy", "Spain", "Japan", "China", "India", "Brazil", 
        "Mexico", "South Korea", "Russia", "South Africa", "Nigeria", 
        "United Arab Emirates", "Singapore", "New Zealand", "Other"
    ]
    
    form = html.Div([
        html.H2("Step 2: Customize Your Prompt", className="mb-3"),
        
        dbc.Form([
            # Source inputs
            html.H4("Content Source", className="mt-4 mb-3"),
            dbc.Row([
                dbc.Col([
                    dbc.FormGroup([
                        dbc.Label("Source Link (URL)"),
                        dbc.Input(
                            id="source-link-input",
                            type="url",
                            placeholder="https://example.com/article",
                        )
                    ])
                ], width=12)
            ], className="mb-3"),
            
            dbc.Row([
                dbc.Col([
                    dbc.FormGroup([
                        dbc.Label("Reference Content (Text)"),
                        dbc.Textarea(
                            id="reference-content-input",
                            placeholder="Paste content to reference or summarize...",
                            style={"height": "120px"}
                        )
                    ])
                ], width=12)
            ], className="mb-4"),
            
            # Content details in two columns
            html.H4("Content Details", className="mt-4 mb-3"),
            dbc.Row([
                # Column 1
                dbc.Col([
                    dbc.FormGroup([
                        dbc.Label("Primary Keyword"),
                        dbc.Input(
                            id="primary-keyword-input",
                            type="text",
                            placeholder="Main keyword to target",
                            required=True
                        )
                    ], className="mb-3"),
                    
                    dbc.FormGroup([
                        dbc.Label("Target Audience"),
                        dcc.Dropdown(
                            id="target-audience-input",
                            options=[
                                {"label": "Developers", "value": "Developers"},
                                {"label": "Researchers", "value": "Researchers"},
                                {"label": "Business Executives", "value": "Business Executives"},
                                {"label": "Marketers", "value": "Marketers"},
                                {"label": "Students", "value": "Students"},
                                {"label": "General Public", "value": "General Public"}
                            ],
                            value="General Public"
                        )
                    ], className="mb-3")
                ], width=6),
                
                # Column 2
                dbc.Col([
                    dbc.FormGroup([
                        dbc.Label("Secondary Keywords"),
                        dcc.Dropdown(
                            id="secondary-keywords-input",
                            options=[],  # Would be populated from database
                            multi=True,
                            placeholder="Select supporting keywords"
                        )
                    ], className="mb-3"),
                    
                    dbc.FormGroup([
                        dbc.Label("Target Location"),
                        dcc.Dropdown(
                            id="target-location-input",
                            options=[{"label": country, "value": country} for country in major_countries],
                            value="United States"
                        )
                    ], className="mb-3")
                ], width=6)
            ], className="mb-3"),
            
            # Additional settings row
            dbc.Row([
                dbc.Col([
                    dbc.FormGroup([
                        dbc.Label("Reading Level"),
                        dcc.Dropdown(
                            id="reading-level-input",
                            options=[
                                {"label": "General", "value": "General"},
                                {"label": "Beginner", "value": "Beginner"},
                                {"label": "Intermediate", "value": "Intermediate"},
                                {"label": "Advanced", "value": "Advanced"}
                            ],
                            value="General"
                        )
                    ])
                ], width=4),
                
                dbc.Col([
                    dbc.FormGroup([
                        dbc.Label("Content Update Frequency"),
                        dcc.Dropdown(
                            id="update-frequency-input",
                            options=[
                                {"label": "1 month", "value": "1 month"},
                                {"label": "3 months", "value": "3 months"},
                                {"label": "6 months", "value": "6 months"},
                                {"label": "12 months", "value": "12 months"}
                            ],
                            value="3 months"
                        )
                    ])
                ], width=4),
                
                dbc.Col([
                    dbc.FormGroup([
                        dbc.Label("Word Count"),
                        dbc.Input(
                            id="word-count-input",
                            type="number",
                            min=300,
                            max=5000,
                            step=100,
                            value=1500
                        )
                    ])
                ], width=4)
            ], className="mb-3"),
            
            dbc.Row([
                dbc.Col([
                    dbc.FormGroup([
                        dbc.Label("Content Tone"),
                        dcc.Dropdown(
                            id="content-tone-input",
                            options=[
                                {"label": "Professional", "value": "Professional"},
                                {"label": "Conversational", "value": "Conversational"},
                                {"label": "Technical", "value": "Technical"},
                                {"label": "Educational", "value": "Educational"},
                                {"label": "Persuasive", "value": "Persuasive"},
                                {"label": "Informative", "value": "Informative"}
                            ],
                            value=template.get("tone", "Professional")
                        )
                    ])
                ], width=12)
            ], className="mb-4"),
            
            # Advanced options
            dbc.Card([
                dbc.CardHeader("Advanced Options"),
                dbc.CardBody([
                    dbc.Row([
                        # Column 1 of checkboxes
                        dbc.Col([
                            dbc.Checkbox(
                                id="include-faq-input",
                                label="Include FAQ Section",
                                value=True,
                                className="mb-2"
                            ),
                            dbc.Checkbox(
                                id="include-meta-input",
                                label="Generate Meta Title & Description",
                                value=True,
                                className="mb-2"
                            ),
                            dbc.Checkbox(
                                id="include-schema-input",
                                label="Include Schema Markup Recommendation",
                                value=True,
                                className="mb-2"
                            ),
                            dbc.Checkbox(
                                id="generate-image-prompt-input",
                                label="Generate Image Prompt",
                                value=False,
                                className="mb-2"
                            ),
                            dbc.Checkbox(
                                id="url-slug-input",
                                label="Generate URL Slug",
                                value=True,
                                className="mb-2"
                            )
                        ], width=6),
                        
                        # Column 2 of checkboxes
                        dbc.Col([
                            dbc.Checkbox(
                                id="tags-input",
                                label="Generate Tags",
                                value=True,
                                className="mb-2"
                            ),
                            dbc.Checkbox(
                                id="external-references-input",
                                label="External References",
                                value=False,
                                className="mb-2"
                            ),
                            dbc.Checkbox(
                                id="internal-linking-input",
                                label="Internal Linking Suggestions",
                                value=False,
                                className="mb-2"
                            ),
                            dbc.Checkbox(
                                id="featured-snippet-input",
                                label="Optimize for Featured Snippet",
                                value=False,
                                className="mb-2"
                            )
                        ], width=6)
                    ], className="mb-3"),
                    
                    dbc.FormGroup([
                        dbc.Label("Update Notes"),
                        dbc.Textarea(
                            id="update-notes-input",
                            placeholder="Notes if the content needs regular updates...",
                            style={"height": "100px"}
                        )
                    ])
                ])
            ], className="mb-4"),
            
            # Template-specific fields
            render_template_fields(template),
            
            # Submit button
            dbc.Button(
                "Generate SEO Prompt",
                id="generate-prompt-btn",
                color="primary",
                size="lg",
                className="w-100 mt-4"
            )
        ])
    ])
    
    return form

def render_template_fields(template):
    """Render template-specific fields"""
    if 'fields' not in template or not template['fields']:
        return html.Div()  # No fields to render
    
    fields = template['fields']
    
    return html.Div([
        html.H4("Template-Specific Fields", className="mt-4 mb-3"),
        
        dbc.Row([
            dbc.Col([
                dbc.FormGroup([
                    dbc.Label(field_config.get("label", field_name)),
                    dbc.Input(
                        id={"type": "template-field", "name": field_name},
                        type="text",
                        placeholder=f"Enter {field_name.replace('_', ' ')}"
                    ) if field_config.get("type", "text") == "text" else
                    dbc.Textarea(
                        id={"type": "template-field", "name": field_name},
                        placeholder=f"Enter {field_name.replace('_', ' ')}",
                        style={"height": "100px"}
                    ) if field_config.get("type", "text") == "textarea" else
                    dbc.Input(
                        id={"type": "template-field", "name": field_name},
                        type="number",
                        placeholder=f"Enter {field_name.replace('_', ' ')}"
                    )
                ], className="mb-3")
            ], width=6 if len(fields) > 1 else 12)
            for i, (field_name, field_config) in enumerate(list(fields.items())[:len(fields)//2 + len(fields)%2])
        ] + [
            dbc.Col([
                dbc.FormGroup([
                    dbc.Label(field_config.get("label", field_name)),
                    dbc.Input(
                        id={"type": "template-field", "name": field_name},
                        type="text",
                        placeholder=f"Enter {field_name.replace('_', ' ')}"
                    ) if field_config.get("type", "text") == "text" else
                    dbc.Textarea(
                        id={"type": "template-field", "name": field_name},
                        placeholder=f"Enter {field_name.replace('_', ' ')}",
                        style={"height": "100px"}
                    ) if field_config.get("type", "text") == "textarea" else
                    dbc.Input(
                        id={"type": "template-field", "name": field_name},
                        type="number",
                        placeholder=f"Enter {field_name.replace('_', ' ')}"
                    )
                ], className="mb-3")
            ], width=6)
            for i, (field_name, field_config) in enumerate(list(fields.items())[len(fields)//2 + len(fields)%2:])
        ], className="mb-3")
    ]) if fields else html.Div()

@callback(
    Output("generated-prompt-container", "children"),
    [Input("generate-prompt-btn", "n_clicks")],
    [State("template-selector", "value"),
     State("source-link-input", "value"),
     State("reference-content-input", "value"),
     State("primary-keyword-input", "value"),
     State("secondary-keywords-input", "value"),
     State("target-audience-input", "value"),
     State("target-location-input", "value"),
     State("reading-level-input", "value"),
     State("update-frequency-input", "value"),
     State("word-count-input", "value"),
     State("content-tone-input", "value"),
     State("include-faq-input", "value"),
     State("include-meta-input", "value"),
     State("include-schema-input", "value"),
     State("generate-image-prompt-input", "value"),
     State("url-slug-input", "value"),
     State("tags-input", "value"),
     State("external-references-input", "value"),
     State("internal-linking-input", "value"),
     State("featured-snippet-input", "value"),
     State("update-notes-input", "value"),
     State({"type": "template-field", "name": dash.ALL}, "value"),
     State({"type": "template-field", "name": dash.ALL}, "id")]
)
def generate_prompt(n_clicks, template_id, source_link, reference_content, primary_keyword, 
                   secondary_keywords, target_audience, target_location, reading_level, 
                   update_frequency, word_count, content_tone, include_faq, include_meta, 
                   include_schema, generate_image_prompt, url_slug, tags, 
                   external_references, internal_linking, featured_snippet, update_notes,
                   template_field_values, template_field_ids):
    """Generate SEO prompt based on form inputs"""
    if not n_clicks:
        return html.Div()
    
    if not primary_keyword:
        return dbc.Alert("Primary keyword is required", color="danger")
    
    # Get the template
    template = get_template(template_id)
    
    # Format template field values into a dictionary
    template_fields = {}
    for field_value, field_id in zip(template_field_values, template_field_ids):
        field_name = field_id["name"]
        template_fields[field_name] = field_value
    
    # Source input - use the link if provided, otherwise use the content
    source_input = source_link if source_link else reference_content
    
    # Format secondary keywords
    secondary_kw_text = ", ".join(secondary_keywords) if secondary_keywords else ""
    
    # Get current date
    current_date = date.today().strftime("%Y-%m-%d")
    current_year = date.today().year
    
    # Start with the template content
    prompt_template = template["template"]
    
    # If tone isn't already in the template and it's different, add it
    default_tone = template.get("tone", "Professional")
    if content_tone != default_tone and "Tone:" in prompt_template:
        prompt_template = prompt_template.replace(
            f"Tone: {default_tone}", f"Tone: {content_tone}"
        )
    
    # Build the replacements dictionary
    replacements = {
        "{source_link}": source_input or "",
        "{primary_keyword}": primary_keyword,
        "{secondary_keywords}": secondary_kw_text,
        "{target_audience}": target_audience,
        "{target_location}": target_location,
        "{update_frequency}": update_frequency,
        "{current_date}": current_date,
        "{current_year}": str(current_year),
        "{word_count}": str(word_count),
        "{tone}": content_tone,
        "{reading_level}": reading_level,
    }
    
    # Add template-specific field replacements
    for field_name, field_value in template_fields.items():
        replacements[f"{{{field_name}}}"] = field_value or ""
    
    # Apply all replacements
    prompt = prompt_template
    for key, value in replacements.items():
        if value:  # Only replace if value is not empty
            prompt = prompt.replace(key, value)
    
    # Handle optional sections
    if not include_faq and "FAQ Section" in prompt:
        # Try to remove FAQ section without breaking the prompt
        faq_lines = []
        lines = prompt.split("\n")
        in_faq_section = False
        
        for i, line in enumerate(lines):
            if "FAQ Section" in line or "FAQ:" in line:
                in_faq_section = True
            elif (
                in_faq_section
                and line.strip()
                and (line.startswith("#") or line.startswith("##"))
            ):
                in_faq_section = False
                
            if in_faq_section:
                faq_lines.append(i)
                
        # Remove FAQ lines
        if faq_lines:
            prompt = "\n".join(
                [line for i, line in enumerate(lines) if i not in faq_lines]
            )
    
    # Add meta tags generation if requested
    if include_meta and "Meta title" not in prompt and "Meta description" not in prompt:
        prompt += "\n\n## Generate Meta Tags\n"
        prompt += "- Title Tag (50-60 characters)\n"
        prompt += "- Meta Description (150-160 characters)\n"
        
    # Add schema recommendation if requested
    schema_type = template.get("schema", "Article")
    if include_schema and "Schema markup" not in prompt:
        prompt += f"\n\n## Schema Markup\nRecommend appropriate schema.org markup for this {schema_type} content.\n"
        
    # Add target location if provided
    if target_location and target_location != "Other":
        prompt += f"\n\n## Location Targeting\nThis content targets audiences in {target_location}. Include location-specific information and keywords where relevant.\n"
        
    # Add reading level guidance
    if reading_level and reading_level != "General":
        prompt += f"\n\n## Reading Level\nContent should be written at a {reading_level} reading level appropriate for the target audience.\n"
        
    # Add image prompt generation if requested
    if generate_image_prompt:
        prompt += "\n\n## Image Suggestions\n"
        prompt += "- Suggest 3-5 image ideas that would enhance this content\n"
        prompt += "- Provide SEO-optimized alt text for each image\n"
        prompt += "- Recommend image types (e.g., infographic, hero image, screenshot)\n"
        
    # Add URL slug generation if requested
    if url_slug:
        prompt += "\n\n## URL Slug\nGenerate an SEO-friendly URL slug for this content.\n"
        
    # Add tags generation if requested
    if tags:
        prompt += "\n\n## Content Tags\nSuggest 5-10 tags for categorizing this content.\n"
        
    # Add external references if requested
    if external_references:
        prompt += "\n\n## External References\nSuggest 3-5 authoritative external sources that could be referenced in this content.\n"
        
    # Add internal linking suggestions if requested
    if internal_linking:
        prompt += "\n\n## Internal Linking Opportunities\nSuggest topics or content types on the same site that should link to or from this content.\n"
        
    # Add featured snippet optimization if requested
    if featured_snippet:
        prompt += "\n\n## Featured Snippet Optimization\n"
        prompt += "- Format a section of this content to be eligible for a featured snippet\n"
        prompt += "- Include a clear definition, list, or table that directly answers a common question\n"
        prompt += "- Optimize for 'People Also Ask' opportunities\n"
        
    # Add update notes if provided
    if update_notes:
        prompt += f"\n\n## Content Update Strategy\n{update_notes}\n"
        
    # Add social media suggestion section
    prompt += "\n\n## Social Media Content\n"
    prompt += "Generate social media post ideas for LinkedIn, Instagram, and other recommended platforms based on this content.\n"
    
    # Save the prompt to database
    save_prompt_generation(
        template_id,
        primary_keyword,
        template.get("category", "General"),
        target_audience,
        secondary_kw_text,
        prompt
    )
    
    # Return the generated prompt with tabs for different views
    return render_generated_prompt(prompt, primary_keyword)

def render_generated_prompt(prompt, primary_keyword):
    """Render the generated prompt with tabs for editing, preview, and analysis"""
    return html.Div([
        html.H2("Generated SEO Prompt", className="mt-4 mb-3"),
        
        # Create tabs for different views
        dbc.Tabs([
            # Edit & Copy tab
            dbc.Tab([
                dbc.Textarea(
                    id="prompt-text-output",
                    value=prompt,
                    style={"height": "400px", "font-family": "monospace"},
                    className="mb-3"
                ),
                
                dbc.Row([
                    dbc.Col([
                        dbc.Button(
                            "Copy to Clipboard",
                            id="copy-prompt-btn",
                            color="primary",
                            className="me-2"
                        ),
                    ], width=4),
                    
                    dbc.Col([
                        html.A(
                            dbc.Button(
                                "Download Prompt",
                                color="secondary",
                                className="me-2"
                            ),
                            id="download-prompt-link",
                            download=f"seo_prompt_{primary_keyword.replace(' ', '_').lower()}.txt",
                            href=f"data:text/plain;charset=utf-8,{prompt}"
                        ),
                    ], width=4),
                    
                    dbc.Col([
                        dbc.Button(
                            "Save as Template",
                            id="save-as-template-btn",
                            color="success"
                        ),
                    ], width=4)
                ])
            ], label="Edit & Copy"),
            
            # Preview tab
            dbc.Tab([
                html.Div([
                    dcc.Markdown(
                        prompt,
                        className="prompt-preview"
                    )
                ], className="prompt-preview-container")
            ], label="Preview"),
            
            # Analysis tab
            dbc.Tab([
                # Analysis content here
                html.Div([
                    dbc.Row([
                        dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                    html.H5("Word Count"),
                                    html.H2(id="word-count-display")
                                ])
                            ])
                        ], width=3),
                        
                        dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                    html.H5("Character Count"),
                                    html.H2(id="char-count-display")
                                ])
                            ])
                        ], width=3),
                        
                        dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                    html.H5("Keyword Count"),
                                    html.H2(id="keyword-count-display")
                                ])
                            ])
                        ], width=3),
                        
                        dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                    html.H5("Keyword Density"),
                                    html.H2(id="keyword-density-display")
                                ])
                            ])
                        ], width=3)
                    ], className="mb-4"),
                    
                    html.Div([
                        html.H5("Prompt Structure"),
                        html.Div(id="structure-analysis")
                    ], className="mb-4"),
                    
                    html.Div([
                        html.H5("SEO Elements Check"),
                        html.Div(id="seo-elements-check")
                    ])
                ])
            ], label="Analysis")
        ], id="prompt-tabs")
    ], className="mt-4")

# Additional callbacks for prompt analysis
@callback(
    [Output("word-count-display", "children"),
     Output("char-count-display", "children"),
     Output("keyword-count-display", "children"),
     Output("keyword-density-display", "children"),
     Output("structure-analysis", "children"),
     Output("seo-elements-check", "children")],
    [Input("prompt-text-output", "value"),
     Input("primary-keyword-input", "value"),
     Input("secondary-keywords-input", "value")]
)
def update_prompt_analysis(prompt_text, primary_keyword, secondary_keywords):
    """Update the prompt analysis metrics"""
    if not prompt_text or not primary_keyword:
        return "0", "0", "0", "0%", "No data", "No data"
    
    # Word count
    words = prompt_text.split()
    word_count = len(words)
    
    # Character count
    char_count = len(prompt_text)
    
    # Keyword count and density
    keyword_count = 0
    if primary_keyword:
        keyword_pattern = re.compile(r'\b' + re.escape(primary_keyword) + r'\b', re.IGNORECASE)
        keyword_count = len(keyword_pattern.findall(prompt_text))
        keyword_density = (keyword_count / word_count * 100) if word_count > 0 else 0
    else:
        keyword_density = 0
    
    # Structure analysis
    headings = re.findall(r'\n##? ([^\n]+)', prompt_text)
    
    structure_analysis = []
    if headings:
        structure_analysis.append(html.P("Main sections in your prompt:"))
        section_list = []
        
        for i, heading in enumerate(headings[:10]):  # Limit to first 10 for clarity
            section_list.append(html.Li(f"{heading}"))
            
        if len(headings) > 10:
            section_list.append(html.Li(f"...and {len(headings) - 10} more sections"))
            
        structure_analysis.append(html.Ul(section_list))
    else:
        structure_analysis.append(html.P("No clear section headings found. Consider adding ## headings for better structure."))
    
    # SEO elements check
    seo_elements = {
        "Keywords": primary_keyword in prompt_text,
        "Secondary Keywords": (
            any(kw in prompt_text for kw in secondary_keywords)
            if secondary_keywords
            else False
        ),
        "Meta Title/Description": "meta" in prompt_text.lower() or "title tag" in prompt_text.lower(),
        "FAQ Section": "faq" in prompt_text.lower(),
        "Headings Structure": len(headings) > 1,
        "Word Count Target": str(word_count) in prompt_text,
        "Schema Markup": "schema" in prompt_text.lower(),
        "Social Media": "social media" in prompt_text.lower(),
    }
    
    seo_check_items = []
    for element, present in seo_elements.items():
        icon = "✅" if present else "❌"
        seo_check_items.append(html.Div([html.Span(icon, className="me-2"), element]))
    
    return (
        str(word_count),
        str(char_count),
        str(keyword_count),
        f"{keyword_density:.2f}%",
        html.Div(structure_analysis),
        html.Div(seo_check_items, className="seo-checklist")
    )

# JavaScript for copy to clipboard functionality
app.clientside_callback(
    """
    function(n_clicks, text) {
        if (n_clicks) {
            navigator.clipboard.writeText(text);
            return 'Copied!';
        }
        return 'Copy to Clipboard';
    }
    """,
    Output("copy-prompt-btn", "children"),
    [Input("copy-prompt-btn", "n_clicks")],
    [State("prompt-text-output", "value")]
)

# Callback for saving as template
@callback(
    Output("save-as-template-btn", "children"),
    [Input("save-as-template-btn", "n_clicks")],
    [State("prompt-text-output", "value")]
)
def save_as_template(n_clicks, prompt_text):
    """Handle saving the generated prompt as a template"""
    if not n_clicks:
        return "Save as Template"
    
    # In a real implementation, you'd store this in session or database
    # Then redirect to template creation page
    
    # For now, just provide feedback
    return "Template Saved!"