# Social Media Job Scraper

This project automatically scrapes job listings from various social media platforms and sends them to you via WhatsApp.

## Features
- Scrapes job listings from:
  - LinkedIn
  - Twitter
  - Other platforms can be added easily
- Sends job notifications via WhatsApp
- Configurable job search criteria
- Scheduled automatic runs

## Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Create a `.env` file with your credentials:
   ```
   LINKEDIN_USERNAME=your_email
   LINKEDIN_PASSWORD=your_password
   TWITTER_API_KEY=your_twitter_api_key
   TWITTER_API_SECRET=your_twitter_api_secret
   WHATSAPP_NUMBER=your_whatsapp_number
   ```

3. Run the script:
   ```bash
   python main.py
   ```

## Configuration
Edit `config.py` to customize:
- Job search keywords
- Platforms to scrape
- Notification frequency
- WhatsApp message format

## Note
- Make sure you have Chrome/Firefox installed for Selenium
- WhatsApp Web needs to be logged in first time
- The script uses pywhatkit for WhatsApp integration 