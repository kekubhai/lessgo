from typing import List, Dict

# Job search configuration
KEYWORDS: List[str] = [
    "software engineer",
    "python developer",
    "full stack developer",
    "data scientist"
]

# Platforms to scrape
PLATFORMS: Dict[str, bool] = {
    "linkedin": True,
    "twitter": True

}

# Time settings (24-hour format)
SCHEDULE_TIME = "09:00"  # When to run the scraper daily
NOTIFICATION_COOLDOWN = 3600  # Minimum seconds between notifications for same job

# Job filtering
MIN_SALARY = 0  # Minimum salary to consider (0 for any)
MAX_AGE_HOURS = 24  # Only consider jobs posted in last 24 hours

# Message template
MESSAGE_TEMPLATE = """
🚨 New Job Alert! 🚨

Position: {title}
Company: {company}
Platform: {platform}
Posted: {posted_time}
Salary: {salary}

Description: {description}

Apply here: {link}
"""

# Locations to search in
LOCATIONS: List[str] = [
    "Remote",
    "United States",
    "United Kingdom"
    "India"
] 