# Google Review Summariser

This is a lightweight AI-powered tool that extracts and summarises Google Maps reviews for any business location. It allows users to paste a Google Maps business link and returns a clean, readable summary using OpenAI's GPT-4.

## Features

- Clean chatbot-style interface (built with Gradio)
- Scrapes all available reviews with written text
- Summarises review content into strengths, weaknesses, and common themes
- Powered by OpenAI's GPT-4 API
- Ideal for competitor research, market validation, or general sentiment analysis

## Use Cases

- Perform quick competitor analysis before opening a new location
- Understand what real customers are saying about a business
- Scan reviews in bulk without manually reading them
- Collect insights from local businesses, cafes, service providers, and more

## Installation Instructions

### 1. Clone the repository

```bash
git clone https://github.com/Rakesh-v27/Google-Review-Summariser.git
cd Google-Review-Summariser
```

### 2. Create and activate a virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate     # On Windows: venv\Scripts\activate
```

### 3. Install project dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up your OpenAI API Key

Create a `.env` file in the project root and add your API key like this:

```
OPENAI_API_KEY=sk-your-openai-api-key-here
```

You can generate a key at: https://platform.openai.com/account/api-keys

## Running the App

To start the web app locally:

```bash
python app.py
```

Then open the URL shown in your terminal (usually http://127.0.0.1:7860) in a browser.

## Requirements

- Python 3.8+
- Google Chrome installed (for Selenium)
- OpenAI account and API key

## Project Structure

```
google-reviews-summariser/
├── app.py              # Gradio UI and OpenAI integration
├── scraper.py          # Selenium-based scraper
├── requirements.txt    # Python dependencies
├── .env                # OpenAI API key (not pushed to GitHub)
├── .gitignore
```


