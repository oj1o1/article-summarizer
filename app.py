import streamlit as st
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import os
from dotenv import load_dotenv
import google.generativeai as genai  # Google Generative AI SDK

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Configure Google AI API
genai.configure(api_key=GOOGLE_API_KEY)

# Set up the Gemini model
model = genai.GenerativeModel("gemini-pro")  # Gemini Pro for text generation

def is_valid_url(url):
    """Validate the format of a URL."""
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

def fetch_article_content(url):
    """Fetch article content from the given URL."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise an exception for HTTP errors
        soup = BeautifulSoup(response.content, "html.parser")
        paragraphs = soup.find_all("p")
        content = " ".join([para.get_text() for para in paragraphs])
        if not content.strip():
            return "Error: No readable content found on the page."
        return content
    except requests.exceptions.RequestException as e:
        return f"Error fetching content: {e}"

def summarize_text(content):
    """Generate a summary of the text using Google Gemini AI."""
    try:
        response = model.generate_content(f"Summarize this article: {content}")
        return response.text
    except Exception as e:
        return f"Error generating summary: {e}"

# Streamlit UI
st.title("Article Summarizer with Google Gemini AI")
url = st.text_input("Enter the URL of the article:")

if st.button("Summarize"):
    if not is_valid_url(url):
        st.error("Invalid URL. Please enter a valid URL starting with http:// or https://.")
    else:
        with st.spinner("Fetching and summarizing..."):
            article = fetch_article_content(url)
            if article.startswith("Error"):
                st.error(article)
            else:
                summary = summarize_text(article)
                if summary.startswith("Error"):
                    st.error(summary)
                else:
                    st.success("Summary:")
                    st.write(summary)

