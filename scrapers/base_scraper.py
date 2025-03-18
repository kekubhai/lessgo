from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

@dataclass
class JobListing:
    title: str
    company: str
    description: str
    link: str
    platform: str
    posted_time: datetime
    salary: Optional[str] = None
    location: Optional[str] = None

class BaseScraper(ABC):
    def __init__(self):
        self.jobs: List[JobListing] = []

    @abstractmethod
    def authenticate(self) -> bool:
        """Authenticate with the platform."""
        pass

    @abstractmethod
    def search_jobs(self, keywords: List[str], locations: List[str]) -> List[JobListing]:
        """Search for jobs with given keywords and locations."""
        pass

    def filter_jobs(self, min_salary: int = 0, max_age_hours: int = 24) -> List[JobListing]:
        """Filter jobs based on criteria."""
        now = datetime.now()
        filtered_jobs = []
        
        for job in self.jobs:
            # Filter by age
            age = (now - job.posted_time).total_seconds() / 3600
            if age > max_age_hours:
                continue

            # Filter by salary if available
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