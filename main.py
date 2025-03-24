import schedule
import time
from datetime import datetime
from scrapers import LinkedInScraper ,TelegramScraper  # TwitterScraper commented out
from notifiers import WhatsAppNotifier
import config

def scrape_and_notify():
    """Main function that handles job scraping and notifications"""
    
    print(f"🔍 Starting job search at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Initialize all scrapers that are enabled in config
    active_scrapers = []
    if config.PLATFORMS["linkedin"]:
        active_scrapers.append(LinkedInScraper())
    # if config.PLATFORMS["twitter"]:
    #     active_scrapers.append(TwitterScraper())
    if config.PLATFORMS["telegram"]:
        active_scrapers.append(TelegramScraper())
    
    # Initialize WhatsApp notifier
    try:
        notifier = WhatsAppNotifier()
    except ValueError as e:
        print(f"❌ Error setting up WhatsApp: {str(e)}")
        return
    
    # Collect jobs from all platforms
    all_jobs = []
    for scraper in active_scrapers:
        try:
            print(f"📱 Searching on {scraper.__class__.__name__}")
            
            # Get and filter jobs
            jobs = scraper.search_jobs(
                keywords=config.KEYWORDS,
                locations=config.LOCATIONS
            )
            filtered_jobs = scraper.filter_jobs(
                min_salary=config.MIN_SALARY,
                max_age_hours=config.MAX_AGE_HOURS
            )
            
            all_jobs.extend(filtered_jobs)
            print(f"✅ Found {len(filtered_jobs)} matching jobs")
            
        except Exception as e:
            print(f"❌ Error with {scraper.__class__.__name__}: {str(e)}")
    
    # Send notifications if we found any jobs
    if all_jobs:
        try:
            notifier.send_notification(all_jobs, config.MESSAGE_TEMPLATE)
            print(f"📱 Sent notifications for {len(all_jobs)} jobs")
        except Exception as e:
            print(f"❌ Error sending notifications: {str(e)}")
    else:
        print("ℹ️ No new jobs found")

def main():
    """Entry point of the application"""
    
    print("🚀 Job Scraper Starting...")
    print(f"⚙️ Configured to search for: {', '.join(config.KEYWORDS)}")
    print(f"📍 In locations: {', '.join(config.LOCATIONS)}")
    
    # Schedule daily runs
    schedule.every().day.at(config.SCHEDULE_TIME).do(scrape_and_notify)
    print(f"⏰ Scheduled to run daily at {config.SCHEDULE_TIME}")
    
    # Run once immediately
    print("▶️ Running initial search...")
    scrape_and_notify()
    
    # Keep the script running
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    main()