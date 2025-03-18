import os
from datetime import datetime, timezone
from typing import List
import tweepy
from .base_scraper import BaseScraper, JobListing
from dotenv import load_dotenv

class TwitterScraper(BaseScraper):
    def __init__(self):
        super().__init__()
        load_dotenv()
        self.api = None
        self.client = None

    def authenticate(self) -> bool:
        try:
            api_key = os.getenv('TWITTER_API_KEY')
            api_secret = os.getenv('TWITTER_API_SECRET')
            access_token = os.getenv('TWITTER_ACCESS_TOKEN')
            access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
            bearer_token = os.getenv('TWITTER_BEARER_TOKEN')
            
            if not all([api_key, api_secret, bearer_token]):
                raise ValueError("Twitter credentials not found in .env file")
            
            # Initialize v2 client
            self.client = tweepy.Client(
                bearer_token=bearer_token,
                consumer_key=api_key,
                consumer_secret=api_secret,
                access_token=access_token,
                access_token_secret=access_token_secret
            )
            return True
            
        except Exception as e:
            print(f"Twitter authentication failed: {str(e)}")
            return False

    def search_jobs(self, keywords: List[str], locations: List[str]) -> List[JobListing]:
        if not self.client:
            if not self.authenticate():
                return []

        self.jobs = []
        
        # Construct search queries
        for keyword in keywords:
            for location in locations:
                try:
                    # Create search query with job-related terms
                    query = f"{keyword} (hiring OR job OR position OR opportunity) {location} -is:retweet"
                    
                    # Search tweets
                    tweets = self.client.search_recent_tweets(
                        query=query,
                        max_results=100,
                        tweet_fields=['created_at', 'text', 'entities', 'author_id']
                    )
                    
                    if not tweets.data:
                        continue
                        
                    for tweet in tweets.data:
                        try:
                            # Get tweet author info
                            author = self.client.get_user(id=tweet.author_id)
                            company = author.data.name
                            
                            # Extract URL if present
                            job_url = None
                            if tweet.entities and 'urls' in tweet.entities:
                                for url in tweet.entities['urls']:
                                    if 'expanded_url' in url:
                                        job_url = url['expanded_url']
                                        break
                            
                            # Create job listing
                            job_listing = JobListing(
                                title=f"{keyword} - {location}",
                                company=company,
                                description=tweet.text,
                                link=job_url if job_url else f"https://twitter.com/user/status/{tweet.id}",
                                platform="Twitter",
                                posted_time=tweet.created_at.replace(tzinfo=None),
                                location=location
                            )
                            
                            self.jobs.append(job_listing)
                            
                        except Exception as e:
                            print(f"Error processing tweet: {str(e)}")
                            continue
                            
                except Exception as e:
                    print(f"Error searching Twitter jobs: {str(e)}")
                    continue

        return self.jobs 