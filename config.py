import os

# Database Settings
DB_PATH = os.getenv("DB_PATH", "data/seo_generator.db")
TEMPLATES_DIR = os.getenv("TEMPLATES_DIR", "data/templates")

# App Settings
DEBUG = os.getenv("DEBUG", "True") == "True"
APP_TITLE = "SEO Prompt Generator"
APP_DESCRIPTION = "Generate optimized SEO prompts for content creation"

# Default theme
DEFAULT_THEME = "BOOTSTRAP"  # Options: BOOTSTRAP, CYBORG, DARKLY, etc.