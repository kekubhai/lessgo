from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

@dataclass
class Job:
    """Represents a job listing from any platform"""
    title: str
    company: str
    description: str
    link: str
    platform: str  # LinkedIn, Twitter, Telegram
    posted_time: datetime
    salary: Optional[str] = None
    location: Optional[str] = None

class JobScraper(ABC):
    """Base class for all job scrapers"""
    
    def __init__(self):
        self.jobs: List[Job] = []
    
    @abstractmethod
    def authenticate(self) -> bool:
        """Set up authentication with the platform
        Returns: True if successful, False otherwise"""
        pass
    
    @abstractmethod
    def search_jobs(self, keywords: List[str], locations: List[str]) -> List[Job]:
        """Search for jobs matching keywords and locations
        Returns: List of matching jobs"""
        pass
    
    def filter_jobs(self, min_salary: int = 0, max_age_hours: int = 24) -> List[Job]:
        """Filter jobs based on criteria
        
        Args:
            min_salary: Minimum salary to consider (0 for any)
            max_age_hours: Maximum age of job posts to include
            
        Returns:
            List of jobs matching the criteria
        """
        now = datetime.now()
        filtered_jobs = []
        
        for job in self.jobs:
            # Check job age
            age_hours = (now - job.posted_time).total_seconds() / 3600
            if age_hours > max_age_hours:
                continue
            
            # Check salary if specified
            if job.salary and min_salary > 0:
                try:
                    # Extract first number from salary string
                    import re
                    salary_num = int(re.findall(r'\d+', job.salary)[0])
                    if salary_num < min_salary:
                        continue
                except (IndexError, ValueError):
                    pass  # Keep job if salary parsing fails
            
            filtered_jobs.append(job)
        
        return filtered_jobs 