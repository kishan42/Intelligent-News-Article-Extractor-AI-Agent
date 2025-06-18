

import os
import re
import json
import requests
import streamlit as st
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

# Set your API Keys (use environment variables or hardcode for testing)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyC_n3U-S_LkaUlQEGJNb8CYdGldHC-3OcE")
AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY", "patSVHOoGj1boHSMs.7923101f5e44fcb28d2e6858e0c87342ef21ae43c4b84add82fa668047df17e9")
AIRTABLE_BASE_ID = os.getenv("AIRTABLE_BASE_ID", "app4kDe9tX8VuIF7R")
AIRTABLE_TABLE_NAME = os.getenv("AIRTABLE_TABLE_NAME", "Articles")


# Initialize Gemini model
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro-latest",
    google_api_key=GEMINI_API_KEY,
    temperature=0.5
)

def fetch_article_text(url: str) -> str:
    """Download the article and extract text."""
    try:
        resp = requests.get(url)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        paragraphs = soup.find_all("p")
        return "\n".join(p.get_text() for p in paragraphs)
    except Exception as e:
        st.error(f"Error fetching article: {e}")
        return ""

def extract_json_from_string(text: str) -> dict | None:
    """Extract JSON object from a string."""
    match = re.search(r"\{[\s\S]*\}", text)
    if match:
        json_str = match.group()
        try:
            return json.loads(json_str)
        except json.JSONDecodeError:
            return None
    return None

def extract_with_gemini(article_text: str) -> dict | None:
    """Use Gemini to extract structured data from article text."""
    system_prompt = (
        "You are a news article extractor. "
        "Given an article, return a JSON with the following keys:\n"
        "• headline (max 7 words)\n"
        "• date (YYYY-MM-DD format)\n"
        "• country (ISO 3166-1 alpha-2 code)\n"
        "• category (Trade, Economy, Politics, Technology, Sports, Religion, Other)\n"
        "Return only valid JSON. Do not include ```json``` or any extra text."
    )
    user_prompt = f"""
Article (first 5000 characters):
---
{article_text[:5000]}
---
"""
    try:
        response = llm.invoke(system_prompt + "\n" + user_prompt)
        return extract_json_from_string(response.content)  # <-- FIXED
    except Exception as e:
        st.error(f"Error during Gemini extraction: {e}")
        return None


def send_to_airtable(fields: dict) -> dict:
    """Send extracted data to Airtable."""
    url = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{AIRTABLE_TABLE_NAME}"
    headers = {
        "Authorization": f"Bearer {AIRTABLE_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {"fields": fields}
    try:
        resp = requests.post(url, headers=headers, json=payload)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        st.error(f"Error sending data to Airtable: {e}")
        return {}

# Streamlit UI
st.title("📰 News Article Extractor (Gemini + LangChain)")

article_url = st.text_input("Enter article URL")
if st.button("Submit URL"):
    if article_url:
        with st.spinner("Fetching and extracting..."):
            text = fetch_article_text(article_url)
            if text:
                extracted = extract_with_gemini(text)
                if extracted:
                    st.subheader("📄 Extracted Info")
                    st.json(extracted)
                    record = {
                            "Headline": extracted.get("headline"),
                            "Date": extracted.get("date"),
                            "Country": extracted.get("country"),
                            "Category": extracted.get("category"),
                            "Article URL": article_url
                        }
                    result = send_to_airtable(record)
                    if result.get("id"):
                        st.success(f"Data sent to Airtable. Record ID: {result.get('id')}")
                else:
                    st.error("Failed to extract JSON from the article.")
            else:
                st.error("Failed to fetch article text.")
    else:
        st.warning("Please enter a valid URL.")
