import os
from datetime import datetime
from typing import List
from linkedin_api import Linkedin
from .base_scraper import BaseScraper, JobListing
from dotenv import load_dotenv

class LinkedInScraper(BaseScraper):
    def __init__(self):
        super().__init__()
        load_dotenv()
        self.api = None

    def authenticate(self) -> bool:
        try:
            username = os.getenv('LINKEDIN_USERNAME')
            password = os.getenv('LINKEDIN_PASSWORD')
            
            if not username or not password:
                raise ValueError("LinkedIn credentials not found in .env file")
            
            self.api = Linkedin(username, password)
            return True
        except Exception as e:
            print(f"LinkedIn authentication failed: {str(e)}")
            return False

    def search_jobs(self, keywords: List[str], locations: List[str]) -> List[JobListing]:
        if not self.api:
            if not self.authenticate():
                return []

        self.jobs = []
        for keyword in keywords:
            for location in locations:
                try:
                    # Search for jobs
                    results = self.api.search_jobs(
                        keywords=keyword,
                        location=location,
                        limit=25
                    )

                    # Process each job listing
                    for job in results:
                        try:
                            # Get detailed job info
                            job_detail = self.api.get_job(job['entityUrn'].split(':')[-1])
                            
                            # Create job listing object
                            job_listing = JobListing(
                                title=job_detail.get('title', 'No Title'),
                                company=job_detail.get('companyDetails', {}).get('company', {}).get('name', 'Unknown Company'),
                                description=job_detail.get('description', {}).get('text', 'No description available'),
                                link=f"https://www.linkedin.com/jobs/view/{job['entityUrn'].split(':')[-1]}",
                                platform="LinkedIn",
                                posted_time=datetime.fromtimestamp(job_detail.get('postedAt', 0)/1000),
                                salary=job_detail.get('salaryInsights', {}).get('compensationText', None),
                                location=job_detail.get('formattedLocation', location)
                            )
                            
                            self.jobs.append(job_listing)
                        except Exception as e:
                            print(f"Error processing job listing: {str(e)}")
                            continue

                except Exception as e:
                    print(f"Error searching LinkedIn jobs: {str(e)}")
                    continue

        return self.jobs 