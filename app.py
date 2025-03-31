import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Set page title
st.title("Web Scraper with Streamlit")

# Input URL
url = st.text_input("Enter website URL:", "http://quotes.toscrape.com")

# Headers to mimic a real browser
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def fetch_page(url):
    """Fetch the HTML content of a webpage."""
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching {url}: {e}")
        return None

def parse_quotes(html):
    """Extract quotes and authors from the HTML content."""
    soup = BeautifulSoup(html, "html.parser")
    quotes = []
    
    for quote_block in soup.select(".quote"):
        text = quote_block.find(class_="text").get_text(strip=True)
        author = quote_block.find(class_="author").get_text(strip=True)
        quotes.append({"Quote": text, "Author": author})
    
    return quotes

# Scrape button
if st.button("Scrape Website"):
    st.write(f"Scraping {url}...")
    
    html_content = fetch_page(url)
    
    if html_content:
        data = parse_quotes(html_content)
        
        if data:
            df = pd.DataFrame(data)
            st.write("### Extracted Data")
            st.dataframe(df)

            # Download button for CSV
            csv_data = df.to_csv(index=False).encode("utf-8")
            st.download_button("Download CSV", csv_data, "scraped_data.csv", "text/csv")
        else:
            st.warning("No data found.")
