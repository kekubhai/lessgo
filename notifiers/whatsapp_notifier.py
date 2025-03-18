import os
import time
from typing import List
import pywhatkit as pwk
from datetime import datetime
from dotenv import load_dotenv
from scrapers.base_scraper import JobListing

class WhatsAppNotifier:
    def __init__(self):
        load_dotenv()
        self.phone_number = os.getenv('WHATSAPP_NUMBER')
        if not self.phone_number:
            raise ValueError("WhatsApp number not found in .env file")
        
        # Remove any non-numeric characters from phone number
        self.phone_number = ''.join(filter(str.isdigit, self.phone_number))
        
        # Track sent messages to avoid duplicates
        self.sent_messages = set()

    def format_message(self, job: JobListing, template: str) -> str:
        """Format the job listing using the template."""
        return template.format(
            title=job.title,
            company=job.company,
            platform=job.platform,
            posted_time=job.posted_time.strftime("%Y-%m-%d %H:%M"),
            salary=job.salary if job.salary else "Not specified",
            description=job.description[:200] + "..." if len(job.description) > 200 else job.description,
            link=job.link
        )

    def send_notification(self, jobs: List[JobListing], message_template: str) -> None:
        """Send WhatsApp notifications for new job listings."""
        for job in jobs:
            # Skip if we've already sent this job
            job_key = f"{job.link}_{job.title}_{job.company}"
            if job_key in self.sent_messages:
                continue

            try:
                message = self.format_message(job, message_template)
                
                # Get current time
                now = datetime.now()
                
                # Send message using pywhatkit
                # Add 2 minutes to current time to ensure WhatsApp Web is ready
                pwk.sendwhatmsg(
                    self.phone_number,
                    message,
                    now.hour,
                    now.minute + 2,
                    wait_time=15,
                    tab_close=True
                )
                
                # Add to sent messages
                self.sent_messages.add(job_key)
                
                # Wait between messages to avoid rate limiting
                time.sleep(20)
                
            except Exception as e:
                print(f"Error sending WhatsApp notification: {str(e)}")
                continue

    def clear_sent_messages(self) -> None:
        """Clear the sent messages cache."""
        self.sent_messages.clear() 