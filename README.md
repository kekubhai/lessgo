# Social Media Job Scraper

This project automatically scrapes job listings from various social media platforms and sends them to you via WhatsApp.

## Features
- Scrapes job listings from:
  - LinkedIn
  - Twitter (X)
  - Telegram
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
   # LinkedIn credentials
   LINKEDIN_USERNAME=your_email
   LINKEDIN_PASSWORD=your_password

   # Twitter (X) credentials
   TWITTER_API_KEY=your_twitter_api_key
   TWITTER_API_SECRET=your_twitter_api_secret
   TWITTER_ACCESS_TOKEN=your_access_token
   TWITTER_ACCESS_TOKEN_SECRET=your_access_token_secret
   TWITTER_BEARER_TOKEN=your_bearer_token

   # Telegram credentials
   TELEGRAM_BOT_TOKEN=your_bot_token
   TELEGRAM_JOB_CHANNELS=channel1,channel2,channel3

   # WhatsApp number (with country code)
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

## Platform Setup

### Twitter (X)
1. Create a Twitter Developer account at https://developer.twitter.com
2. Create a new project and app
3. Generate API keys and tokens
4. Enable OAuth 2.0
5. Add the credentials to your `.env` file

### Telegram
1. Create a new bot using @BotFather on Telegram
2. Get the bot token
3. Add your bot to the job channels you want to monitor
4. Add the bot token and channel usernames to your `.env` file

### LinkedIn
1. Use your LinkedIn account credentials
2. Make sure you have a premium account for better job search results

## Note
- Make sure you have Chrome/Firefox installed for Selenium
- WhatsApp Web needs to be logged in first time
- The script uses pywhatkit for WhatsApp integration
- For Telegram, make sure your bot has permission to read channel messages
- Twitter API has rate limits, so be mindful of the frequency of searches 