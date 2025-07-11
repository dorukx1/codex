"""Entry point for the Codex multi-tool app."""

import streamlit as st
from text_analysis import analyze_sentiment, plot_sentiment
from weather import fetch_weather
from web_scraper import scrape_url
from finance import init_db, add_expense, get_monthly_summary
from code_analysis import analyze_code


st.title("Codex Multi-Tool App")

# Weather Module
st.header("Weather")
city = st.text_input("City")
if st.button("Get Weather") and city:
    try:
        data = fetch_weather(city)
        st.json(data)
    except Exception as e:
        st.error(str(e))

# Text Analysis Module
st.header("Text Analysis")
text = st.text_area("Enter text for sentiment analysis")
if st.button("Analyze Sentiment") and text:
    result = analyze_sentiment(text)
    st.write(result)
    plot_sentiment(result["polarity"])

# Web Scraper Module
st.header("Web Scraper")
url = st.text_input("URL to scrape")
if st.button("Scrape URL") and url:
    try:
        scrape_url(url)
        st.success("Content downloaded to ./scraped directory")
    except Exception as e:
        st.error(str(e))

# Finance Module
st.header("Personal Finance")
init_db()
category = st.text_input("Expense Category")
amount = st.number_input("Amount", min_value=0.0, format="%f")
if st.button("Add Expense") and category:
    add_expense(category, amount)
    st.success("Expense added")

month = st.text_input("Month (YYYY-MM)")
if st.button("Show Summary") and month:
    data = get_monthly_summary(month)
    st.write(data)

# Code Analysis Module
st.header("Code Analysis")
code = st.text_area("Paste Python code here")
if st.button("Analyze Code") and code:
    suggestions = analyze_code(code)
    st.write(suggestions)
