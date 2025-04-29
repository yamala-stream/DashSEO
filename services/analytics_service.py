"""
Analytics Service for SEO Prompt Generator
Handles data processing for analytics dashboard
"""
import pandas as pd
from datetime import datetime, timedelta
from utils.database import DatabaseManager
from config import DB_PATH

# Initialize the database manager
db_manager = DatabaseManager(DB_PATH)

def get_prompt_metrics():
    """
    Get summary metrics for prompt generation
    
    Returns:
    - Dictionary of metrics
    """
    # Get prompt data
    prompts_df = db_manager.get_prompts_df()
    
    # Default values if dataframe is empty
    metrics = {
        "total_prompts": 0,
        "unique_keywords": 0,
        "categories": 0,
        "weekly_trend": 0
    }
    
    if not prompts_df.empty:
        # Calculate metrics
        metrics["total_prompts"] = len(prompts_df)
        
        if "primary_keyword" in prompts_df.columns:
            metrics["unique_keywords"] = prompts_df["primary_keyword"].nunique()
        
        if "category" in prompts_df.columns:
            metrics["categories"] = prompts_df["category"].nunique()
        
        # Calculate trend (prompts in last week vs previous week)
        if "timestamp" in prompts_df.columns:
            prompts_df["date"] = pd.to_datetime(prompts_df["timestamp"]).dt.date
            
            today = pd.to_datetime("today").date()
            one_week_ago = pd.to_datetime("today") - pd.Timedelta(days=7)
            two_weeks_ago = pd.to_datetime("today") - pd.Timedelta(days=14)
            
            prompts_last_week = len(prompts_df[prompts_df["date"] >= one_week_ago.date()])
            prompts_previous_week = len(prompts_df[(prompts_df["date"] >= two_weeks_ago.date()) & 
                                                 (prompts_df["date"] < one_week_ago.date())])
            
            if prompts_previous_week > 0:
                metrics["weekly_trend"] = ((prompts_last_week - prompts_previous_week) / 
                                         prompts_previous_week * 100)
            else:
                metrics["weekly_trend"] = 0
    
    return metrics

def get_prompt_time_data():
    """
    Get time series data for prompt generation
    
    Returns:
    - DataFrame with date and count columns
    """
    # Get prompt data
    prompts_df = db_manager.get_prompts_df()
    
    # Default empty dataframe
    time_data = pd.DataFrame(columns=["date", "count"])
    
    if not prompts_df.empty and "timestamp" in prompts_df.columns:
        # Format timestamp
        prompts_df["date"] = pd.to_datetime(prompts_df["timestamp"]).dt.date
        
        # Group by date
        time_data = prompts_df.groupby("date").size().reset_index(name="count")
        time_data["date"] = pd.to_datetime(time_data["date"])
    
    # If we have no data, return sample data for development
    if time_data.empty:
        # Create sample data for last 30 days
        today = pd.to_datetime("today")
        dates = [today - timedelta(days=i) for i in range(30)]
        counts = [int(i % 7 + 1) for i in range(30)]  # Sample pattern
        
        time_data = pd.DataFrame({
            "date": dates,
            "count": counts
        })
    
    return time_data

def get_category_distribution():
    """
    Get category distribution data for prompts
    
    Returns:
    - DataFrame with category and count columns
    """
    # Get prompt data
    prompts_df = db_manager.get_prompts_df()
    
    # Default empty dataframe
    category_data = pd.DataFrame(columns=["category", "count"])
    
    if not prompts_df.empty and "category" in prompts_df.columns:
        # Group by category
        category_data = prompts_df.groupby("category").size().reset_index(name="count")
        category_data = category_data.sort_values("count", ascending=False)
    
    # If we have no data, return sample data for development
    if category_data.empty:
        categories = ["Business", "Technical", "Educational", "News", "Marketing"]
        counts = [12, 8, 6, 5, 3]
        
        category_data = pd.DataFrame({
            "category": categories,
            "count": counts
        })
    
    return category_data

def get_recent_prompts(limit=10):
    """
    Get recent prompts for display
    
    Parameters:
    - limit: Maximum number of prompts to return
    
    Returns:
    - DataFrame with prompt data
    """
    # Get prompt data
    prompts_df = db_manager.get_prompts_df()
    
    if not prompts_df.empty:
        # Sort by timestamp
        recent_prompts = prompts_df.sort_values("timestamp", ascending=False).head(limit)
        
        # Format timestamp
        if "timestamp" in recent_prompts.columns:
            recent_prompts["timestamp"] = pd.to_datetime(recent_prompts["timestamp"]).dt.strftime('%Y-%m-%d %H:%M')
        
        return recent_prompts
    
    # Return empty dataframe if no data
    return pd.DataFrame(columns=["timestamp", "template_id", "primary_keyword", "category", "audience"])

def get_template_usage():
    """
    Get template usage statistics
    
    Returns:
    - DataFrame with template usage data
    """
    # Get template usage data
    template_usage_df = db_manager.get_template_usage_stats()
    
    # If we have no data, return sample data for development
    if template_usage_df.empty:
        templates = ["ai_concepts", "beginner_guides", "blog_post", "business_analysis", "technical_guide"]
        counts = [15, 12, 9, 7, 5]
        last_used = [datetime.now() - timedelta(days=i) for i in range(5)]
        
        template_usage_df = pd.DataFrame({
            "template_id": templates,
            "usage_count": counts,
            "last_used": last_used
        })
    
    return template_usage_df

def get_template_time_data():
    """
    Get time series data for template usage
    
    Returns:
    - DataFrame with date, template_id, and count columns
    """
    # Get prompt data
    prompts_df = db_manager.get_prompts_df()
    
    # Default empty dataframe
    template_time_data = pd.DataFrame(columns=["date", "template_id", "count"])
    
    if not prompts_df.empty and "timestamp" in prompts_df.columns and "template_id" in prompts_df.columns:
        # Convert timestamp to datetime
        prompts_df["date"] = pd.to_datetime(prompts_df["timestamp"]).dt.date
        
        # Group by date and template
        template_time_data = prompts_df.groupby(["date", "template_id"]).size().reset_index(name="count")
        template_time_data["date"] = pd.to_datetime(template_time_data["date"])
    
    # If we have no data, return sample data for development
    if template_time_data.empty:
        templates = ["ai_concepts", "beginner_guides", "blog_post"]
        
        # Create sample data for last 14 days
        today = pd.to_datetime("today")
        dates = []
        template_ids = []
        counts = []
        
        for i in range(14):
            date = today - timedelta(days=i)
            for template in templates:
                dates.append(date)
                template_ids.append(template)
                counts.append(int((i % 5) * (templates.index(template) + 1) / 3) + 1)
        
        template_time_data = pd.DataFrame({
            "date": dates,
            "template_id": template_ids,
            "count": counts
        })
    
    return template_time_data

def get_template_metrics():
    """
    Get template performance metrics
    
    Returns:
    - DataFrame with template metrics
    """
    # Get template usage data
    template_usage_df = db_manager.get_template_usage_stats()
    prompts_df = db_manager.get_prompts_df()
    
    # Default empty dataframe
    template_metrics = pd.DataFrame(columns=["Template Name", "usage_count", "keyword_diversity", "Last Used"])
    
    if not template_usage_df.empty:
        # Get templates
        from utils.template_store import get_template_list
        templates = get_template_list()
        template_map = {t["id"]: t["name"] for t in templates}
        
        # Create template metrics table
        template_metrics = template_usage_df.copy()
        template_metrics["Template Name"] = template_metrics["template_id"].map(lambda x: template_map.get(x, x))
        
        if "last_used" in template_metrics.columns:
            template_metrics["Last Used"] = pd.to_datetime(template_metrics["last_used"]).dt.strftime('%Y-%m-%d')
        
        # Calculate template diversity (number of unique primary keywords per template)
        if not prompts_df.empty and "primary_keyword" in prompts_df.columns and "template_id" in prompts_df.columns:
            template_diversity = prompts_df.groupby("template_id")["primary_keyword"].nunique().reset_index()
            template_diversity.columns = ["template_id", "keyword_diversity"]
            
            # Merge with metrics
            template_metrics = pd.merge(template_metrics, template_diversity, on="template_id", how="left")
    
    # If we have no data, return sample data for development
    if template_metrics.empty:
        templates = ["AI Concepts", "Beginner Guides", "Blog Post", "Business Analysis", "Technical Guide"]
        ids = ["ai_concepts", "beginner_guides", "blog_post", "business_analysis", "technical_guide"]
        counts = [15, 12, 9, 7, 5]
        diversity = [8, 6, 5, 4, 3]
        last_used = [(datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(5)]
        
        template_metrics = pd.DataFrame({
            "template_id": ids,
            "Template Name": templates,
            "usage_count": counts,
            "keyword_diversity": diversity,
            "Last Used": last_used
        })
    
    return template_metrics

def get_top_keywords(limit=10):
    """
    Get top keywords by usage
    
    Parameters:
    - limit: Maximum number of keywords to return
    
    Returns:
    - DataFrame with keyword usage data
    """
    # Get keyword data
    primary_keywords_df = db_manager.get_keywords_by_type("primary")
    
    if not primary_keywords_df.empty:
        # Sort by usage count
        top_keywords = primary_keywords_df.sort_values("usage_count", ascending=False).head(limit)
        return top_keywords
    
    # Return sample data if no real data is available
    keywords = ["AI", "Machine Learning", "Neural Networks", "Data Science", "NLP", 
               "Computer Vision", "Deep Learning", "ChatGPT", "Python", "TensorFlow"]
    counts = [15, 12, 10, 8, 7, 6, 5, 4, 3, 2]
    
    return pd.DataFrame({
        "keyword": keywords,
        "usage_count": counts
    })

def get_keyword_category_data():
    """
    Get keyword usage by category
    
    Returns:
    - DataFrame with keyword, category, and count columns
    """
    # Get keyword data
    primary_keywords_df = db_manager.get_keywords_by_type("primary")
    prompts_df = db_manager.get_prompts_df()
    
    # Default empty dataframe
    keyword_category_data = pd.DataFrame(columns=["primary_keyword", "category", "count"])
    
    if (not primary_keywords_df.empty and not prompts_df.empty and 
        "category" in prompts_df.columns and "primary_keyword" in prompts_df.columns):
        
        # Get top keywords
        top_keywords = primary_keywords_df.sort_values("usage_count", ascending=False).head(5)["keyword"].tolist()
        
        # Filter prompts to include only top keywords
        filtered_prompts = prompts_df[prompts_df["primary_keyword"].isin(top_keywords)]
        
        if not filtered_prompts.empty:
            # Group by keyword and category
            keyword_category_data = filtered_prompts.groupby(["primary_keyword", "category"]).size().reset_index(name="count")
    
    # If we have no data, return sample data for development
    if keyword_category_data.empty:
        keywords = ["AI", "Machine Learning", "NLP", "Deep Learning", "Computer Vision"]
        categories = ["Business", "Technical", "Educational", "News", "Marketing"]
        data = []
        
        # Create sample combinations
        for keyword in keywords:
            for category in categories[:3]:  # Not all categories for each keyword
                if keywords.index(keyword) % 2 == categories.index(category) % 2:  # Just a pattern
                    data.append({
                        "primary_keyword": keyword,
                        "category": category,
                        "count": keywords.index(keyword) + categories.index(category) + 1
                    })
        
        keyword_category_data = pd.DataFrame(data)
    
    return keyword_category_data

def get_keyword_trends_data():
    """
    Get keyword usage trends over time
    
    Returns:
    - DataFrame with date, primary_keyword, and count columns
    """
    # Get keyword data
    primary_keywords_df = db_manager.get_keywords_by_type("primary")
    prompts_df = db_manager.get_prompts_df()
    
    # Default empty dataframe
    keyword_trends_data = pd.DataFrame(columns=["date", "primary_keyword", "count"])
    
    if (not primary_keywords_df.empty and not prompts_df.empty and 
        "timestamp" in prompts_df.columns and "primary_keyword" in prompts_df.columns):
        
        # Convert timestamp to datetime
        prompts_df["date"] = pd.to_datetime(prompts_df["timestamp"]).dt.date
        
        # Get top keywords for trend analysis
        top_keywords = primary_keywords_df.sort_values("usage_count", ascending=False).head(5)["keyword"].tolist()
        
        # Filter prompts to include only top keywords
        filtered_prompts = prompts_df[prompts_df["primary_keyword"].isin(top_keywords)]
        
        if not filtered_prompts.empty:
            # Group by date and keyword
            keyword_trends_data = filtered_prompts.groupby(["date", "primary_keyword"]).size().reset_index(name="count")
            keyword_trends_data["date"] = pd.to_datetime(keyword_trends_data["date"])
    
    # If we have no data, return sample data for development
    if keyword_trends_data.empty:
        keywords = ["AI", "Machine Learning", "NLP", "Deep Learning", "Computer Vision"]
        
        # Create sample data for last 14 days
        today = pd.to_datetime("today")
        data = []
        
        for i in range(14):
            date = today - timedelta(days=i)
            for keyword in keywords[:3]:  # Use only first 3 keywords for cleaner visualization
                # Create a realistic pattern with some randomness
                if i % (keywords.index(keyword) + 2) == 0:  # Different frequency per keyword
                    count = max(1, keywords.index(keyword) + (14 - i) // 3)  # Trend increases towards recent dates
                    data.append({
                        "date": date,
                        "primary_keyword": keyword,
                        "count": count
                    })
        
        keyword_trends_data = pd.DataFrame(data)
    
    return keyword_trends_data