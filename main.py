import schedule
import time
from datetime import datetime
import config
from scrapers.linkedin_scraper import LinkedInScraper
from scrapers.twitter_scraper import TwitterScraper
from scrapers.telegram_scraper import TelegramScraper
from notifiers.whatsapp_notifier import WhatsAppNotifier

def run_job_search():
    print(f"Starting job search at {datetime.now()}")
    
    # Initialize scrapers based on config
    scrapers = []
    if config.PLATFORMS.get("linkedin"):
        scrapers.append(LinkedInScraper())
    if config.PLATFORMS.get("twitter"):
        scrapers.append(TwitterScraper())
    if config.PLATFORMS.get("telegram"):
        scrapers.append(TelegramScraper())
    
    # Initialize notifier
    notifier = WhatsAppNotifier()
    
    # Collect all jobs from all platforms
    all_jobs = []
    for scraper in scrapers:
        try:
            jobs = scraper.search_jobs(config.KEYWORDS, config.LOCATIONS)
            filtered_jobs = scraper.filter_jobs(
                min_salary=config.MIN_SALARY,
                max_age_hours=config.MAX_AGE_HOURS
            )
            all_jobs.extend(filtered_jobs)
            print(f"Found {len(filtered_jobs)} jobs from {scraper.__class__.__name__}")
        except Exception as e:
            print(f"Error with scraper {scraper.__class__.__name__}: {str(e)}")
    
    # Send notifications for new jobs
    if all_jobs:
        try:
            notifier.send_notification(all_jobs, config.MESSAGE_TEMPLATE)
            print(f"Sent notifications for {len(all_jobs)} jobs")
        except Exception as e:
            print(f"Error sending notifications: {str(e)}")
    else:
        print("No new jobs found")

def main():
    print("Job Scraper Service Starting...")
    
    # Schedule the job to run at the configured time
    schedule.every().day.at(config.SCHEDULE_TIME).do(run_job_search)
    
    # Also run once immediately
    run_job_search()
    
    # Keep the script running
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    main() 