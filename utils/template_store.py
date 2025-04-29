"""
Template store utility for SEO Prompt Generator
Adapted from the original Streamlit templates.py module
"""
import json
import os
from pathlib import Path
import re

# Template directory paths
TEMPLATES_DIR = "data/templates"

# Import the advanced templates
# In production, these would be properly imported from your data module
TEMPLATE_CATEGORIES = {
    "educational_awareness": {"name": "Educational & Awareness", "icon": "📚", "templates": []},
    "how_to_tutorials": {"name": "How-To & Tutorials", "icon": "👨‍🏫", "templates": []},
    "expert_technical": {"name": "Expert & Technical Deep-Dives", "icon": "🧠", "templates": []},
    "use_case_focused": {"name": "Use Case Focused", "icon": "🌟", "templates": []}
}

# Default template
DEFAULT_TEMPLATE = {
    "id": "custom_template",
    "name": "Custom Template",
    "use_case": "Custom use case",
    "schema": "Article",
    "tone": "Professional",
    "template": """
# Custom SEO Prompt Template

## Content Brief: {primary_keyword}

You are creating content about {primary_keyword} for {target_audience}.

### SOURCE AND KEYWORDS
- Source/Reference: {source_link}
- Primary Keyword: {primary_keyword}
- Secondary Keywords: {secondary_keywords}
- Target Audience: {target_audience}
- Update Frequency: {update_frequency}
- Last Updated: {current_date}

### CONTENT STRUCTURE
- Title: Include primary keyword near the beginning
- Format: Engaging, well-structured content
- Style: Professional and informative
- Length: {word_count} words
- Schema: Article

### REQUIRED SECTIONS
1. Introduction - Hook and topic overview
2. Main Content - Detailed information
3. Key Benefits/Features - Highlighting important points
4. Examples/Case Studies - Real-world applications
5. Tips/Best Practices - Practical advice
6. Conclusion - Summary and next steps
7. FAQ Section - Common questions answered

### SEO REQUIREMENTS
- Use primary keyword in title, headings, and throughout content
- Include secondary keywords naturally
- Use engaging meta description
- Add internal and external links
- Include images with descriptive alt text
- Create scannable content with headings and bullet points
"""
}

# Base templates to initialize system with
INITIAL_TEMPLATES = {
    "ai_in_business": {
        "name": "AI in Business",
        "intent": "Commercial",
        "tone": "Professional, strategic",
        "schema": "Article",
        "category": "Business",
        "fields": {
            "business_name": {"label": "🏢 Business Name", "type": "text", "required": True},
            "industry": {"label": "🏭 Industry", "type": "text", "required": True}
        },
        "template": """
🔧 AI in Business — Enhanced Prompt Template

Intent: Commercial
Tone: Professional, strategic
Schema: Article

🧠 Prompt

You are an enterprise AI content strategist. Your goal is to write a data-driven article based on the following inputs:
	• Business: {business_name}
	• Industry: {industry}
	• Source Link: {source_link}
	• Primary Keyword: {primary_keyword}
	• Secondary Keywords: {secondary_keywords}
	• Audience: Enterprise leaders, decision-makers
	• Update Frequency: {update_frequency}
	• Last Updated: {current_date}

🔧 Structure
	• H1: How {business_name} Uses AI to Transform {industry}
	• H2s:
	• AI Integration in Business Processes
	• Impact on ROI
	• Challenges and Solutions
	• FAQ:
	• How is AI improving business operations?
	• What are common AI tools in enterprises?
	• CTA: Discover how AI is reshaping the future of business.

🔁 SEO Best Practices
	• Start with ROI hooks and executive-friendly stats
	• Add real-world case studies or industry benchmarks
	• Insert graphs showing growth/efficiency changes
"""
    },
    "beginner_guides": {
        "name": "Beginner Guides",
        "intent": "Educational",
        "tone": "Simple, supportive",
        "schema": "FAQPage",
        "category": "Educational",
        "fields": {
            "topic": {"label": "📚 Topic", "type": "text", "required": True}
        },
        "template": """
📘 Beginner Guides — Enhanced Prompt Template

Intent: Educational
Tone: Simple, supportive
Schema: FAQPage

🧠 Prompt

You are an educator writing a beginner's AI guide. Simplify technical topics for absolute beginners.
	• Topic: {topic}
	• Source or Notes: {source_link}
	• Audience: Students, hobbyists, first-time learners
	• Primary Keyword: {primary_keyword}
	• Secondary Keywords: {secondary_keywords}

🔧 Structure
	• H1: AI Basics: A Beginner's Guide to {topic}
	• H2s:
	• What is {topic}?
	• Why does it matter?
	• Getting Started
	• FAQ:
	• What is {topic} in AI?
	• How do I start learning it?
	• CTA: Start your AI journey with this beginner-friendly introduction.

🧩 SEO Enhancements
	• Define all terms in plain English
	• Add real-world beginner use cases
	• Include a glossary block
"""
    },
    "default": {
        "name": "Default SEO Template",
        "intent": "General",
        "tone": "Professional",
        "schema": "Article",
        "category": "General",
        "fields": {},
        "template": """
🚀 Ultimate Advanced SEO Prompt for High-Traffic AI Content

**Use Case:** Rewrite or generate top-ranking, high-conversion AI articles for your blog, news site, or tutorial portal.

---

✅ MASTER SEO CONTENT REWRITING PROMPT ({category})

You are an expert SEO content strategist and writer for a leading AI media platform. Your job is to **rewrite or create a fully original article** using the content from **{source_link}**, in a way that:

• 📈 Dominates Google search results for competitive and long-tail AI keywords
• 🎯 Targets the primary keyword **"{primary_keyword}"**
• 🧩 Uses secondary keywords like **{secondary_keywords}**
• 🧠 NLP-rich, engaging, skimmable
• 👥 Audience: **{target_audience}**

🔁 Update every {update_frequency}
🧠 Last updated: {current_date}

## Content Structure Guidelines:
• H1: Include primary keyword near the beginning
• H2/H3: Include secondary keywords naturally
• Introduction: Hook readers, introduce the topic
• Body: 5-7 sections with subheadings
• Conclusion: Summarize key points, include call-to-action
• Word count: 1500-2000 words for comprehensive coverage

## SEO Optimization Instructions:
• Include primary keyword in title, meta description, URL
• Use secondary keywords 2-3 times each
• Add 2-3 relevant internal links
• Add 3-4 authoritative external links
• Include image alt text with keywords
• Aim for 2% keyword density
"""
    }
}

def init_templates_directory():
    """Create templates directory and initialize with default templates if it doesn't exist"""
    if not os.path.exists(TEMPLATES_DIR):
        os.makedirs(TEMPLATES_DIR, exist_ok=True)
    
    # Load templates from alternate locations if available
    custom_templates = load_templates_from_directory("prompt_templates")
    
    # Merge with default templates from INITIAL_TEMPLATES
    all_templates = {**INITIAL_TEMPLATES, **custom_templates}
    
    # Create template index file if it doesn't exist
    index_file = os.path.join(TEMPLATES_DIR, "index.json")
    if not os.path.exists(index_file):
        # Save index with initial templates
        with open(index_file, "w") as f:
            json.dump(all_templates, f, indent=4)
        
    # Also create individual template files for each initial template
    for template_id, template_data in all_templates.items():
        template_path = os.path.join(TEMPLATES_DIR, f"{template_id}.json")
        if not os.path.exists(template_path):
            with open(template_path, "w") as f:
                json.dump(template_data, f, indent=4)
                
    return True

def get_all_categories():
    """Get all available template categories, both built-in and custom"""
    categories = []
    
    # Add built-in categories from TEMPLATE_CATEGORIES
    for category_id, category_data in TEMPLATE_CATEGORIES.items():
        categories.append({
            "id": category_id,
            "name": category_data.get("name", category_id),
            "icon": category_data.get("icon", "📁"),
            "is_builtin": True
        })
    
    # Add categories from INITIAL_TEMPLATES
    for template_id, template_data in INITIAL_TEMPLATES.items():
        category = template_data.get("category", "General")
        category_found = False
        for c in categories:
            if c["id"] == category:
                category_found = True
                break
                
        if not category_found:
            categories.append({
                "id": category,
                "name": category,
                "icon": "📁",
                "is_builtin": False
            })
    
    # Add custom categories from template files
    if os.path.exists(TEMPLATES_DIR):
        for file_path in Path(TEMPLATES_DIR).glob("*.json"):
            try:
                with open(file_path, "r") as f:
                    template_data = json.load(f)
                    category = template_data.get("category", "General")
                    
                    category_found = False
                    for c in categories:
                        if c["id"] == category:
                            category_found = True
                            break
                            
                    if not category_found:
                        categories.append({
                            "id": category,
                            "name": category,
                            "icon": "📁",
                            "is_builtin": False
                        })
            except Exception as e:
                print(f"Error reading template category {file_path}: {str(e)}")
    
    return categories

def get_template_list():
    """Get list of all available templates from both built-in and file-based sources"""
    templates = []
    
    # Ensure directory exists
    if not os.path.exists(TEMPLATES_DIR):
        init_templates_directory()
    
    # Add templates from TEMPLATE_CATEGORIES
    for category_id, category_data in TEMPLATE_CATEGORIES.items():
        for template in category_data.get('templates', []):
            templates.append({
                "id": template["id"],
                "name": template["name"],
                "intent": template.get("use_case", category_data["name"]),
                "tone": template.get("tone", "Professional"),
                "schema": template.get("schema", "Article"),
                "category": category_id,
                "is_builtin": True
            })
    
    # Add templates from INITIAL_TEMPLATES
    for template_id, template_data in INITIAL_TEMPLATES.items():
        # Check if template is already in the list
        if not any(t["id"] == template_id for t in templates):
            templates.append({
                "id": template_id,
                "name": template_data["name"],
                "intent": template_data.get("intent", "General"),
                "tone": template_data["tone"],
                "schema": template_data["schema"],
                "category": template_data.get("category", "General"),
                "is_builtin": False
            })
    
    # Add templates from template directory
    for file_path in Path(TEMPLATES_DIR).glob("*.json"):
        try:
            with open(file_path, "r") as f:
                template_data = json.load(f)
                template_id = file_path.stem
                
                # Skip if this template is already in the list
                if any(t["id"] == template_id for t in templates):
                    continue
                
                templates.append({
                    "id": template_id,
                    "name": template_data.get("name", template_id),
                    "intent": template_data.get("intent", template_data.get("use_case", "Custom")),
                    "tone": template_data.get("tone", "Professional"),
                    "schema": template_data.get("schema", "Article"),
                    "category": template_data.get("category", "General"),
                    "is_builtin": False
                })
        except Exception as e:
            print(f"Error reading template {file_path}: {str(e)}")
    
    # Sort by name
    templates.sort(key=lambda x: x["name"])
    
    return templates

def get_template(template_id):
    """Get a specific template by ID, checking both built-in and files"""
    # First check in TEMPLATE_CATEGORIES
    for category_id, category_data in TEMPLATE_CATEGORIES.items():
        for template in category_data.get('templates', []):
            if template["id"] == template_id:
                template_copy = template.copy()
                template_copy["category"] = category_id
                template_copy["is_builtin"] = True
                return template_copy
    
    # Check in INITIAL_TEMPLATES
    if template_id in INITIAL_TEMPLATES:
        template_data = INITIAL_TEMPLATES[template_id].copy()
        template_data["is_builtin"] = False
        return template_data
    
    # Check template files
    template_path = os.path.join(TEMPLATES_DIR, f"{template_id}.json")
    
    if os.path.exists(template_path):
        with open(template_path, "r") as f:
            template_data = json.load(f)
            template_data["is_builtin"] = False
            return template_data
    
    # If not found in either place, return default template
    return DEFAULT_TEMPLATE

def get_templates_by_category(category_id):
    """Get templates organized by category"""
    all_templates = get_template_list()
    
    # Group templates by category
    templates_by_category = {}
    
    for template in all_templates:
        category = template["category"]
        
        if category not in templates_by_category:
            category_info = next((c for c in get_all_categories() if c["id"] == category), 
                               {"id": category, "name": category, "icon": "📁"})
            
            templates_by_category[category] = {
                "id": category,
                "name": category_info["name"],
                "icon": category_info.get("icon", "📁"),
                "templates": []
            }
        
        templates_by_category[category]["templates"].append(template)
    
    # If no templates found for requested category, add an empty entry
    if category_id not in templates_by_category:
        category_info = next((c for c in get_all_categories() if c["id"] == category_id), 
                           {"id": category_id, "name": category_id, "icon": "📁"})
        
        templates_by_category[category_id] = {
            "id": category_id,
            "name": category_info["name"],
            "icon": category_info.get("icon", "📁"),
            "templates": []
        }
    
    return templates_by_category

def save_template(template_id, template_data):
    """Save a template to disk"""
    # Ensure directory exists
    if not os.path.exists(TEMPLATES_DIR):
        os.makedirs(TEMPLATES_DIR, exist_ok=True)
    
    # For built-in templates, check if we're allowed to modify
    for category_id, category_data in TEMPLATE_CATEGORIES.items():
        for template in category_data.get('templates', []):
            if template["id"] == template_id:
                # Can't save built-in templates directly
                return False
        
    # Save template file
    template_path = os.path.join(TEMPLATES_DIR, f"{template_id}.json")
    
    with open(template_path, "w") as f:
        json.dump(template_data, f, indent=4)
    
    # Also update index file
    index_path = os.path.join(TEMPLATES_DIR, "index.json")
    try:
        with open(index_path, "r") as f:
            template_index = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        template_index = {}
    
    template_index[template_id] = template_data
    
    with open(index_path, "w") as f:
        json.dump(template_index, f, indent=4)
    
    return True

def delete_template(template_id):
    """Delete a template if it's not built-in"""
    # Check if it's a built-in template (can't delete these)
    for category_id, category_data in TEMPLATE_CATEGORIES.items():
        for template in category_data.get('templates', []):
            if template["id"] == template_id:
                return False
    
    # Check if it's an initial template (can delete these, but take caution)
    is_initial = template_id in INITIAL_TEMPLATES
    
    # Delete template file
    template_path = os.path.join(TEMPLATES_DIR, f"{template_id}.json")
    
    if os.path.exists(template_path):
        os.remove(template_path)
        
        # Also remove from index file
        index_path = os.path.join(TEMPLATES_DIR, "index.json")
        try:
            with open(index_path, "r") as f:
                template_index = json.load(f)
                
            if template_id in template_index:
                del template_index[template_id]
                
            with open(index_path, "w") as f:
                json.dump(template_index, f, indent=4)
        except Exception:
            pass
        
        return True
    else:
        return False

def load_templates_from_directory(directory_path):
    """Load all JSON template files from a directory"""
    templates = {}
    
    if os.path.exists(directory_path):
        for file_path in Path(directory_path).glob("*.json"):
            try:
                with open(file_path, "r") as f:
                    template_data = json.load(f)
                    template_id = file_path.stem
                    
                    # Convert to required format if needed
                    if "prompt_body" in template_data:  # New format
                        templates[template_id] = {
                            "name": template_data.get("template_name", template_id),
                            "intent": template_data.get("intent", ""),
                            "tone": template_data.get("tone", ""),
                            "schema": template_data.get("schema", ""),
                            "category": template_data.get("intent", "Other"),
                            "template": template_data.get("prompt_body", ""),
                            "fields": {}  # We'll extract fields later
                        }
                        
                        # Extract fields based on {{field_name}} pattern
                        if templates[template_id]["template"]:
                            placeholders = re.findall(r'\{\{(\w+)\}\}', templates[template_id]["template"])
                            for field in placeholders:
                                field_label = field.replace('_', ' ').title()
                                templates[template_id]["fields"][field] = {
                                    "label": f"📝 {field_label}",
                                    "type": "text",
                                    "required": True
                                }
                            
                            # Replace {{field}} with {field} for compatibility
                            templates[template_id]["template"] = re.sub(
                                r'\{\{(\w+)\}\}', 
                                r'{\1}', 
                                templates[template_id]["template"]
                            )
            except Exception as e:
                print(f"Error loading template {file_path}: {str(e)}")
    
    return templates

# Initialize templates directory on import
init_templates_directory()