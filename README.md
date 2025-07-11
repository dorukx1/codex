# Codex Multi-Tool Application

This project provides a simple Streamlit interface combining several utilities:

- **Weather:** Fetch current conditions and a 5-day forecast for any city using the OpenWeatherMap API. Set your API key in the `OPENWEATHER_API_KEY` environment variable.
- **Text Analysis:** Perform sentiment analysis of user text via TextBlob and visualize the result with matplotlib.
- **Web Scraper:** Download text and images from a provided URL using BeautifulSoup. Results are saved to the `scraped/` directory.
- **Personal Finance:** Track expenses in a local SQLite database and display monthly summaries.
- **Code Analysis:** Basic static analysis of pasted Python code to suggest simple optimizations.

## Requirements

Install dependencies with:

```bash
pip install -r requirements.txt
```

## Running

Launch the Streamlit app:

```bash
streamlit run codex_app/main.py
```
