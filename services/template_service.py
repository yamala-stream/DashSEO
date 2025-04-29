from utils.database import DatabaseManager
from config import DB_PATH

# Initialize database manager
db_manager = DatabaseManager(DB_PATH)

def get_templates():
    """Get all templates"""
    # Placeholder implementation
    # In a real implementation, you would fetch from database
    return [
        {
            "id": "default_template",
            "name": "Default SEO Template",
            "category": "General",
            "schema": "Article",
            "description": "A general purpose SEO content template"
        },
        {
            "id": "blog_post",
            "name": "Blog Post Template",
            "category": "Content",
            "schema": "BlogPosting",
            "description": "Template for creating blog post content"
        },
        {
            "id": "product_description",
            "name": "Product Description",
            "category": "E-commerce",
            "schema": "Product",
            "description": "Template for writing product descriptions"
        }
    ]

def get_template_by_id(template_id):
    """Get template by ID"""
    templates = get_templates()
    for template in templates:
        if template["id"] == template_id:
            return template
    return None