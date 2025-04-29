from utils.database import DatabaseManager
from config import DB_PATH

# Initialize database manager
db_manager = DatabaseManager(DB_PATH)

def get_primary_keywords():
    """Get all primary keywords"""
    # Placeholder implementation
    # In a real implementation, you would fetch from database
    return ["SEO", "Digital Marketing", "Content Strategy", "AI Writing", "Google Ranking"]

def get_secondary_keywords():
    """Get all secondary keywords"""
    # Placeholder implementation
    return ["keywords", "optimization", "search engine", "ranking", "traffic", "conversion"]

def add_keyword(keyword, keyword_type, category=""):
    """Add a new keyword"""
    # Placeholder - in real implementation, add to database
    print(f"Adding keyword: {keyword} ({keyword_type})")
    return True