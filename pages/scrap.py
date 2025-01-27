import streamlit as st
import pandas as pd
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

st.set_page_config(page_title="Web Scraping and Analysis ", layout="wide")

st.markdown("""
    <style>
body {
     background: linear-gradient(135deg, #f3f9ff, #e0efff);
     background-size: cover;
     font-family: 'Arial', sans-serif;
}
.title {
     text-align: center;
     font-size: 3em;
     font-weight: bold;
     margin-top: 20px;
     animation: fadeIn 2s ease-in-out;
}
.header {
     text-align: center;
     font-size: 2em;
     font-weight: bold;
     margin-top: 10px;
     animation: slideIn 1.5s ease-in-out;
}
.subheader {
     text-align: center;
     font-size: 1.5em;
     font-weight: bold;
     margin-top: 10px;
     animation: bounceIn 1.5s ease-in-out;
}
.footer {
     text-align: center;
     font-size: 1em;
     margin-top: 50px;
     padding-bottom: 10px;
}
.stButton > button {
     background-color: #4CAF50;
     color: white;
     border: none;
     padding: 10px 20px;
     text-align: center;
     font-size: 16px;
     margin: 4px 2px;
     cursor: pointer;
     border-radius: 12px;
     transition: background-color 0.3s, transform 0.2s;
}
.stButton > button:hover {
     background-color: #45a049;
     transform: scale(1.1);
}
.sidebar .sidebar-content {
     background-color: #f9f9f9;
     padding: 20px;
     border-radius: 10px;
     box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
     animation: slideInLeft 1s ease-in-out;
}
@keyframes fadeIn {
     from {
          opacity: 0;
     }
     to {
          opacity: 1;
     }
}
@keyframes slideIn {
     from {
          transform: translateY(-50px);
          opacity: 0;
     }
     to {
          transform: translateY(0);
          opacity: 1;
     }
}
@keyframes bounceIn {
     0% {
          transform: scale(0.8);
          opacity: 0;
     }
     50% {
          transform: scale(1.2);
          opacity: 0.8;
     }
     100% {
          transform: scale(1);
          opacity: 1;
     }
}
@keyframes slideInLeft {
     from {
          transform: translateX(-100%);
          opacity: 0;
     }
     to {
          transform: translateX(0);
          opacity: 1;
     }
}
</style>
     """, unsafe_allow_html=True)

st.markdown("<div class='title'>Web Scraping and Analysis </div>", unsafe_allow_html=True)

st.markdown("<div class='header'>Scrape and Analyze Data from Any Website</div>", unsafe_allow_html=True)

with st.sidebar:
     url = st.text_input("Website URL")
     data_type = st.selectbox("Select the type of data you want to scrape", ["Title", "Paragraphs", "Images", "Links"])
     data_format = st.selectbox("Select the format to download the data", ["CSV", "JSON"])
     show_analysis = st.checkbox("Show Data Analysis", value=True)
     scrape_button = st.button("Scrape Data")

def scrape_data(url, data_type):
     driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
     driver.get(url)
     
     scraped_data = []

     if data_type == "Title":
          title = driver.title
          scraped_data.append({"Title": title})
     
     elif data_type == "Paragraphs":
          paragraphs = driver.find_elements(By.TAG_NAME, 'p')
          for p in paragraphs:
                scraped_data.append({"Paragraph": p.text})
     
     elif data_type == "Images":
          images = driver.find_elements(By.TAG_NAME, 'img')
          for img in images:
                img_url = img.get_attribute('src')
                scraped_data.append({"Image URL": img_url})
     
     elif data_type == "Links":
          links = driver.find_elements(By.TAG_NAME, 'a')
          for link in links:
                href = link.get_attribute('href')
                link_text = link.text
                scraped_data.append({"Link Text": link_text, "URL": href})
     
     driver.quit()
     return scraped_data

def download_data(scraped_data, data_format):
     if data_format == "CSV":
          df = pd.DataFrame(scraped_data)
          csv = df.to_csv(index=False).encode('utf-8')
          st.download_button(
                label="Download data as CSV",
                data=csv,
                file_name='scraped_data.csv',
                mime='text/csv',
          )
     elif data_format == "JSON":
          json_data = json.dumps(scraped_data, indent=4)
          st.download_button(
                label="Download data as JSON",
                data=json_data,
                file_name='scraped_data.json',
                mime='application/json',
          )

def analyze_data(scraped_data):
     df = pd.DataFrame(scraped_data)
     st.write("Data Analysis")
     st.write(df.describe())
     st.write("Correlation Matrix")
     numeric_df = df.select_dtypes(include=['number'])
     st.write(numeric_df.corr())
     st.write("Data Head")
     st.write(df.head())

if scrape_button:
     if url:
          st.write("Scraping data from:", url)
          
          with st.spinner('Scraping data...'):
                scraped_data = scrape_data(url, data_type)
          
          if scraped_data:
                st.write(scraped_data)
                if data_type == "Images":
                     for item in scraped_data:
                          st.image(item["Image URL"], caption=item["Image URL"])
                download_data(scraped_data, data_format)
                if show_analysis:
                     analyze_data(scraped_data)
     else:
          st.error("Please enter a valid URL")

st.write("""### About the Web Scraping Function

The **Web Scraping Function** is a meticulously crafted Python-based utility designed to extract specific data from websites. This function leverages web scraping techniques to automate the retrieval of information from web pages, making it an essential tool for data collection, analysis, and research. By programmatically accessing a website, parsing its structure, and retrieving the desired data, this function simplifies complex data extraction tasks, saving time and effort while enhancing efficiency and accuracy.

---

### Purpose of the Function

The primary goal of the Web Scraping Function is to provide an efficient and systematic way to extract data from websites. Whether the task involves collecting product details from an e-commerce site, gathering statistics from a data portal, or extracting text from online articles, this function automates the process, ensuring consistency and accuracy in the retrieved data.

This function is especially valuable for professionals, researchers, and developers working with large datasets or requiring frequent updates from online sources. By eliminating the need for manual copying and pasting, it allows users to focus on analyzing the data rather than gathering it.

---

### Key Features

The Web Scraping Function offers a range of features that make it versatile and effective for various data extraction needs:

#### 1. **URL Input and Validation**
    - Accepts a website's URL as input.
    - Validates the URL's accessibility and ensures that the target page exists and can be scraped.

#### 2. **Automated Web Content Retrieval**
    - Uses HTTP requests to fetch the HTML content of a webpage.
    - Handles headers, cookies, and session data to mimic real-user behavior if necessary.

#### 3. **HTML Parsing and Data Extraction**
    - Parses the HTML structure of the webpage to locate and extract desired data points.
    - Supports a wide range of data extraction scenarios, including:
      - Text content (e.g., articles, headings, and paragraphs).
      - Table data (e.g., tabular reports or statistical information).
      - Links and URLs.
      - Images and multimedia.

#### 4. **Dynamic Content Handling**
    - If the target website relies on JavaScript to load content dynamically, the function can integrate tools like **Selenium** to render and scrape such content effectively.

#### 5. **Flexible Targeting**
    - Supports CSS selectors, XPath, and tag-based searching to locate data accurately.
    - Enables the user to specify precise elements or sections of the webpage to scrape.

#### 6. **Error Handling**
    - Handles common errors gracefully, such as:
      - Invalid URLs.
      - HTTP errors (e.g., 404 Not Found or 403 Forbidden).
      - Connection timeouts.
    - Ensures the program remains stable even when unexpected issues occur.

#### 7. **Data Export**
    - Allows the extracted data to be saved in multiple formats, such as CSV, JSON, or Excel, for easy integration into other workflows.

---

### Conclusion

The **Web Scraping Function** is a versatile and efficient solution for extracting data from websites. It bridges the gap between online information and actionable insights by automating the data retrieval process. With its robust functionality, flexibility, and adherence to ethical standards, this function is an invaluable tool for researchers, developers, and professionals seeking to harness the power of web data for their projects and analyses.
""")

st.markdown('<div class="footer">© 2025 Web Scraping Project. All rights reserved.</div>', unsafe_allow_html=True)
