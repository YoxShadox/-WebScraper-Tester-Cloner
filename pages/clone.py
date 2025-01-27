import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import streamlit as st
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import base64

def check_robots_txt(url):
    parsed_url = urlparse(url)
    robots_url = urljoin(f"{parsed_url.scheme}://{parsed_url.netloc}", "/robots.txt")
    response = requests.get(robots_url)
    if response.status_code == 200:
        if "Disallow: /" in response.text:
            return False
    return True

def scrape_website(url):
    options = Options()
    options.headless = True
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)
    html = driver.page_source
    driver.quit()
    return html

def download_css(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    return ""

def download_js(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    return ""

def download_image(url):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        return response.content
    return None

def download_html(content):
    return content

st.title("Website Cloner")

st.write("Disclaimer: Ensure that you have permission to scrape the website and that you comply with its terms of service.")

url = st.sidebar.text_input("Enter the URL of the website you want to clone:")

if url:
    if check_robots_txt(url):
        st.write("Cloning is allowed by robots.txt")
        html_content = scrape_website(url)
        soup = BeautifulSoup(html_content, 'html.parser')
        
        css_files = []
        for link in soup.find_all('link', rel='stylesheet'):
            css_url = urljoin(url, link['href'])
            css_content = download_css(css_url)
            css_files.append((link['href'].split('/')[-1], css_content))
            new_style_tag = soup.new_tag("style")
            new_style_tag.string = css_content
            link.replace_with(new_style_tag)
        
        js_files = []
        for script in soup.find_all('script', src=True):
            js_url = urljoin(url, script['src'])
            js_content = download_js(js_url)
            js_files.append((script['src'].split('/')[-1], js_content))
            new_script_tag = soup.new_tag("script")
            new_script_tag.string = js_content
            script.replace_with(new_script_tag)
        
        for img in soup.find_all('img', src=True):
            img_url = urljoin(url, img['src'])
            img_content = download_image(img_url)
            if img_content:
                img_base64 = base64.b64encode(img_content).decode('utf-8')
                img['src'] = f"data:image/jpeg;base64,{img_base64}"
        
        about_section = soup.new_tag("section", id="about")
        about_section.string = "This clone tool is used to replicate the structure and content of a webpage for educational and testing purposes."
        soup.body.append(about_section)
        
        feature_section = soup.new_tag("section", id="feature")
        feature_section.string = "Features of this clone tool include downloading HTML, CSS, JavaScript, and images from the specified URL."
        soup.body.append(feature_section)
        
        footer = soup.new_tag("footer")
        footer.string = "This is the footer content from home.py."
        soup.body.append(footer)
        
        st.components.v1.html(str(soup), height=800, width=800, scrolling=True)
        
        st.write("Download CSS Files:")
        for filename, content in css_files:
            st.download_button(label=f"Download {filename}", data=content, file_name=filename, mime="text/css")
        
        st.write("Download JavaScript Files:")
        for filename, content in js_files:
            st.download_button(label=f"Download {filename}", data=content, file_name=filename, mime="application/javascript")
        
        st.write("Download HTML File:")
        st.download_button(label="Download HTML", data=download_html(str(soup)), file_name="cloned_website.html", mime="text/html")

st.write("""### About the Website Cloner Tool

The **Website Cloner Tool** is a Python-based application developed using the **Streamlit framework** to enable users to replicate the structure and components of a website. It serves as an educational and testing resource, designed to help developers and learners analyze the architecture of web pages. This tool allows users to download the HTML, CSS, JavaScript, and image resources of a webpage while maintaining ethical practices by adhering to permissions specified in the website's `robots.txt` file.

---

### Purpose of the Tool

The primary objective of this tool is to provide users with an accessible way to understand and explore the design and functionality of web pages. Whether you are a web development enthusiast, a designer, or a tester, this tool helps you dissect website structures, study layouts, or experiment with prototyping offline. By enabling users to download and analyze a website’s resources, it acts as a valuable learning aid for understanding the interplay between HTML, CSS, JavaScript, and images in building functional and visually appealing web pages.

---

### Key Features

#### **1. URL Input and Validation**
Users can input the URL of the website they wish to clone. The tool then performs a validation check using the `robots.txt` file to ensure that scraping the website is permitted. This feature aligns the tool with ethical practices and web scraping guidelines.

#### **2. Web Scraping Using Selenium**
The tool utilizes **Selenium WebDriver** to render dynamic content from the webpage. Selenium ensures that the tool can extract content even from websites that require JavaScript execution to fully load. This capability makes it versatile for cloning modern, interactive websites.

#### **3. Content Extraction and Embedding**
   - **HTML**: The raw structure of the webpage is downloaded and modified to include embedded resources for offline accessibility.
   - **CSS**: External stylesheets are fetched, and their content is embedded inline within the `<style>` tags. This ensures the cloned page retains its original styling.
   - **JavaScript**: JavaScript files linked externally are downloaded and integrated directly into the cloned page by replacing `<script>` tags with the actual script code.
   - **Images**: Images are fetched and converted to Base64 strings, allowing them to be embedded directly within the `<img>` tags. This eliminates dependency on external links.

#### **4. Custom Sections and Footer**
To make the cloned page more informative, custom sections are added:
   - An **"About" section** explaining the tool's purpose and use case.
   - A **"Feature" section** highlighting the functionalities of the cloned page.
   - A **Footer** section for additional notes or acknowledgments.

#### **5. Interactive Preview and Downloads**
The tool provides users with an interactive preview of the cloned webpage within the Streamlit interface. Additionally, users can download the following resources:
   - Individual CSS files.
   - JavaScript files.
   - A complete HTML file with embedded resources.

#### **6. User-Friendly Interface**
The Streamlit framework ensures a simple and intuitive user experience. All functionalities, from inputting the URL to downloading resources, are accessible through an easy-to-navigate graphical interface.

---

### Benefits and Use Cases

#### **Educational Value**
   - Aspiring web developers can study the structure of real-world websites.
   - Helps in understanding the interaction between HTML, CSS, and JavaScript.
   - Provides a practical resource for learning about responsive and dynamic web design.

#### **Testing and Prototyping**
   - Testers can clone websites to examine their layouts and functionality in isolated environments.
   - Designers can create offline prototypes for brainstorming and development without relying on live internet connections.

#### **Backup and Reference**
   - The tool can be used to create backups of website designs for archival purposes or future reference.
   - Teams working on similar designs can use the cloned pages as a base for collaboration.

---
         
### Conclusion

The **Website Cloner Tool** is a powerful and ethical resource for exploring and understanding web development. It bridges the gap between theoretical learning and practical application by allowing users to dissect and analyze real-world web pages. Its robust functionality, combined with a user-friendly interface and adherence to ethical standards, makes it an invaluable tool for developers, testers, and learners alike.
""")

st.markdown("""
    <style>
        body {
            background: linear-gradient(120deg, #a1c4fd, #c2e9fb);
            animation: gradient-animation 8s ease infinite;
        }
        @keyframes gradient-animation {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        .main {
            padding: 20px;
            font-family: 'Arial', sans-serif;
        }
        h1 {
            text-align: center;
            font-size: 3rem;
            color: #4CAF50;
            animation: text-slide-in 1.5s ease-out;
        }
        @keyframes text-slide-in {
            from { transform: translateY(-100px); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }
        .interactive-section {
            background: white;
            padding: 20px;
            margin: 20px 0;
            border-radius: 10px;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s ease, background-color 0.3s ease;
        }
        .interactive-section:hover {
            transform: scale(1.05);
            background-color: #f0f8ff;
        }
        .interactive-section:active {
            animation: pulse 0.4s;
        }
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.1); }
            100% { transform: scale(1); }
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            border-radius: 5px;
            font-size: 16px;
            padding: 10px 20px;
            transition: background-color 0.3s ease, box-shadow 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #357ab8;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.2);
        }
        footer {
            text-align: center;
            color: #888888;
            font-size: 1em;
            margin-top: 50px;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown('<footer>© 2025 Web Cloner Tool. All rights reserved.</footer>', unsafe_allow_html=True)
