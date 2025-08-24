# 📰 AI News Article Extractor Agent

This project is an intelligent news article extractor powered by **Gemini 1.5 Pro (Google Generative AI)** and built using **Streamlit**. It scrapes a news article from a given URL, extracts structured metadata using LangChain and Gemini, stores the data in **Airtable**, and **automatically sends an email via Zapier** if the article is related to **Trade**.
---

## 🔧 Features

- ✅ Scrapes full article content from any public URL
- ✅ Uses Gemini Pro to extract key metadata:
  - `headline` (max 7 words)
  - `date` (YYYY-MM-DD format)
  - `country` (ISO 3166-1 alpha-2)
  - `category` (Trade, Economy, Politics, etc.)
- ✅ Stores extracted data in **Airtable**
- ✅ Auto email alert via **Zapier** for Trade articles
- ✅ Simple Streamlit interface

---

## 🛠 Tech Stack

- Python
- Streamlit
- LangChain
- Google Gemini 1.5 Pro (Generative AI)
- Airtable API
- BeautifulSoup (HTML parsing)
- Zapier (email automation)
- Regex + JSON parsing
- Requests (HTTP client)
---
## 🚀 Demo

 
 
 
 
---

## 📦 Installation

```bash
git clone https://github.com/yourusername/news-extractor-agent.git
cd news-extractor-agent
pip install -r requirements.txt
________________________________________
🧪 Environment Setup
Create a .env file in your root directory:
GEMINI_API_KEY=your_google_gemini_api_key
AIRTABLE_API_KEY=your_airtable_api_key
AIRTABLE_BASE_ID=your_airtable_base_id
AIRTABLE_TABLE_NAME=Articles
________________________________________
▶️ Usage
Run the app using Streamlit:
streamlit run app.py
1.	Paste a valid article URL into the input box.
2.	Click "Submit URL".
3.	The app will:
o	Scrape the article content.
o	Extract structured metadata via Gemini.
o	Display the results.
o	Store the info in Airtable.
o	(If category = "Trade") trigger a Zapier email alert.
________________________________________
📄 Example Output
{
  "headline": "India Expands Global Trade",
  "date": "2025-06-08",
  "country": "IN",
  "category": "Trade"
}
________________________________________
🧠 Gemini Prompt Overview
The Gemini model is prompted with a detailed system message and the first 5000 characters of the article:
•	Output format is strictly JSON.
•	Categories must be from a defined list.
•	Prompts exclude markdown (```json) to ease parsing.
________________________________________
📤 Airtable Integration
Create a base in Airtable with a table named Articles and the following fields:
Field	Type
Headline	Single line
Date	Date
Country	Single line
Category	Single select (Trade, Politics, etc.)
Article URL	URL
The app posts extracted data using Airtable’s REST API.
________________________________________
📧 Email Alerts via Zapier
This project uses Zapier to send automated email alerts when a new Airtable record is added with category = Trade.
🔄 Zapier Workflow
•	Trigger App: Airtable
o	Trigger: New Record in View
o	Filter: Category = Trade
•	Action App: Gmail / Email by Zapier
o	Action: Send Email
o	Email Template:
o	📢 New Trade Article Alert!
o	
o	Headline: {{Headline}}
o	Date: {{Date}}
o	Country: {{Country}}
o	Read more: {{Article URL}}
✨ You can customize the Zap to send notifications to Slack, Telegram, Discord, or even SMS.
________________________________________
📁 File Structure
📦news-extractor-agent
 ┣ 📄app.py               # Main Streamlit app
 ┣ 📄.env                 # Environment config
 ┣ 📄requirements.txt     # Python dependencies
 ┗ 📄README.md            # Project documentation
________________________________________
🗺️ Future Improvements
•	🔍 Multilingual article support
•	🧠 Smarter category classification using fine-tuned model
•	🧾 Richer metadata extraction (author, location, summary)
•	🔗 Social media sharing of extracted articles
•	📊 Airtable dashboard for analytics

