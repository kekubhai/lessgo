import os
from datetime import datetime, timedelta
from typing import List
import re  # Add this import for regex pattern matching
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
            # Use proper method to get messages
            updates = await self.bot.get_updates(timeout=30)
            messages = []
            
            # Loop through updates to find channel messages
            for update in updates:
                if update.channel_post and update.channel_post.chat.username == channel:
                    messages.append(update.channel_post)
            
            cutoff_time = datetime.now() - timedelta(hours=max_age_hours)
            
            for message in messages:
                if not message.text:
                    continue
                    
                if message.date < cutoff_time:
                    continue
                    
                # Check for keywords
                if any(keyword.lower() in message.text.lower() for keyword in keywords):
                    # Create job listing
                    job = JobListing(
                        title=self._extract_job_title(message.text) or "Job Opening",
                        company=channel,
                        description=message.text[:500] + "..." if len(message.text) > 500 else message.text,
                        link=f"https://t.me/{channel}/{message.message_id}",
                        platform="Telegram",
                        posted_time=message.date,
                        location="Not specified"
                    )
                    jobs.append(job)
                    
        except Exception as e:
            print(f"Error fetching messages from channel {channel}: {str(e)}")
            
        return jobs

    def _extract_job_title(self, text: str) -> str:
        """Extract a job title from message text"""
        # Simple implementation - look for common patterns
        title_patterns = [
            r'(?i)hiring[:\s]+([^.!?\n]+)',
            r'(?i)position[:\s]+([^.!?\n]+)',
            r'(?i)job[:\s]+([^.!?\n]+)'
        ]
        
        for pattern in title_patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1).strip()
        
        # If no pattern matches, return first line or first 50 chars
        first_line = text.split('\n')[0].strip()
        return first_line[:50] + "..." if len(first_line) > 50 else first_line
        
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