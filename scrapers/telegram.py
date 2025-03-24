import os
from datetime import datetime, timedelta
from typing import List
from telegram import Bot
from telegram.error import TelegramError
import asyncio
from .base_scraper import BaseScraper, JobListing
from dotenv import load_dotenv

class TelegramScraper(BaseScraper):
    def __init__(self):
        super().__init__()
        load_dotenv()
        self.bot = None
        self.channels = os.getenv('TELEGRAM_JOB_CHANNELS', '').split(',')

    def authenticate(self) -> bool:
        try:
            token = os.getenv('TELEGRAM_BOT_TOKEN')
            if not token:
                raise ValueError("Telegram bot token not found in .env file")
            
            self.bot = Bot(token=token)
            return True
        except Exception as e:
            print(f"Telegram authentication failed: {str(e)}")
            return False

    async def _fetch_channel_messages(self, channel: str, keywords: List[str], max_age_hours: int = 24) -> List[JobListing]:
        """Fetch recent messages from a Telegram channel."""
        jobs = []
        try:
            # Get recent messages
            messages = await self.bot.get_chat_history(
                chat_id=channel,
                limit=100
            )
            
            cutoff_time = datetime.now() - timedelta(hours=max_age_hours)
            
            for message in messages:
                try:
                    # Skip old messages
                    if message.date < cutoff_time:
                        continue
                    
                    # Check if message contains any of our keywords
                    text = message.text.lower() if message.text else ""
                    if not any(keyword.lower() in text for keyword in keywords):
                        continue
                    
                    # Create job listing
                    job_listing = JobListing(
                        title=text.split('\n')[0][:100],  # Use first line as title
                        company=channel,
                        description=text,
                        link=f"https://t.me/{channel}/{message.message_id}",
                        platform="Telegram",
                        posted_time=message.date,
                        location="Not specified"
                    )
                    
                    jobs.append(job_listing)
                    
                except Exception as e:
                    print(f"Error processing Telegram message: {str(e)}")
                    continue
                    
        except Exception as e:
            print(f"Error fetching messages from channel {channel}: {str(e)}")
            
        return jobs

    def search_jobs(self, keywords: List[str], locations: List[str]) -> List[JobListing]:
        if not self.bot:
            if not self.authenticate():
                return []

        self.jobs = []
        
        # Create event loop for async operations
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            # Fetch messages from all channels
            for channel in self.channels:
                channel_jobs = loop.run_until_complete(
                    self._fetch_channel_messages(channel, keywords)
                )
                self.jobs.extend(channel_jobs)
                
        finally:
            loop.close()

        return self.jobs 