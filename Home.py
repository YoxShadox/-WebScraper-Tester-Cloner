import streamlit as st

# Set page configuration
st.set_page_config(page_title="Web Scraping Project", page_icon=":globe_with_meridians:", layout="wide")

# Custom CSS for background gradient and styling
st.markdown(
    """
    <style>
    body {
        background-size: cover;
        background-attachment: fixed;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        margin: 0;
        padding: 0;
        overflow-x: hidden;
    }

    .main {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 20px;
        padding: 30px;
    }

    .header {
        font-size: 3.5rem;
        font-weight: 800;
        color: #ffffff;
        text-align: center;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.7);
        animation: fadeIn 3s ease-in-out;
        margin-bottom: 20px;
    }

    .stButton>button {
        background: linear-gradient(135deg, #6a11cb, #2575fc);
        color: white;
        font-weight: bold;
        font-size: 1.1rem;
        border: none;
        border-radius: 30px;
        padding: 10px 20px;
        cursor: pointer;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease;
    }

    .stButton>button:hover {
        background: linear-gradient(135deg, #2575fc, #6a11cb);
        transform: scale(1.05);
        box-shadow: 0 6px 10px rgba(0, 0, 0, 0.3);
    }

    .stTextInput>div>div>input {
        border: 2px solid #6a11cb;
        border-radius: 8px;
        padding: 10px;
        font-size: 1rem;
        transition: border-color 0.3s ease;
    }

    .stTextInput>div>div>input:focus {
        border-color: #2575fc;
        outline: none;
    }

    .footer {
        text-align: center;
        padding: 10px;
        color: white;
        background: rgba(0, 0, 0, 0.5);
        bottom: 0;
        width: 100%;
        font-size: 0.9rem;
    }

    .animated-text {
        font-size: 2rem;
        color: #ffffff;
        text-align: center;
        margin-top: 20px;
        background: linear-gradient(90deg, #6a11cb, #2575fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: textSlide 3s linear infinite;
    }

    @keyframes fadeIn {
        0% { opacity: 0; }
        100% { opacity: 1; }
    }

    @keyframes textSlide {
        0% { background-position: 0%; }
        100% { background-position: 200%; }
    }

    .grid-section {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 20px;
        margin: 30px 0;
    }

    .card {
        background: white;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s, box-shadow 0.3s;
    }

    .card:hover {
        transform: translateY(-10px);
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
    }

    .card h3 {
        margin: 0;
        font-size: 1.5rem;
        color: #6a11cb;
    }

    .card p {
        font-size: 1rem;
        color: #333;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Header
st.markdown('<div class="header">Web Scraping Project</div>', unsafe_allow_html=True)

# Main content
st.markdown('<div class="animated-text">Effortlessly Extract, Clone, and Test Websites!</div>', unsafe_allow_html=True)

# Features grid
st.markdown(
    """
    <div class="grid-section">
        <div class="card">
            <h3>Data Scraping</h3>
            <p>Extract data from websites with dynamic content handling and customizable parameters.</p>
        </div>
        <div class="card">
            <h3>Website Cloning</h3>
            <p>Clone entire websites for offline use, preserving structure and assets.</p>
        </div>
        <div class="card">
            <h3>Testing</h3>
            <p>Run and debug your web scraping scripts in a controlled environment.</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# Main content
st.write("""

This website is designed to help you scrape data from various URLs, clone websites, and test your scraping scripts. 
We use powerful libraries such as Selenium to automate the scraping process and ensure you get the data you need efficiently.

### Features:
- **Data Scraping**: Extract data from any website using a URL.
  - Supports multiple formats (HTML, JSON, CSV).
  - Handles dynamic content using Selenium.
  - Customizable scraping parameters.
- **Website Cloning**: Clone entire websites for offline use or analysis.
  - Download all assets (HTML, CSS, JS, images).
  - Preserve website structure.
  - Useful for archiving and offline browsing.
- **Testing**: Test your scraping scripts to ensure they work correctly.
  - Run scripts in a controlled environment.
  - Debug and optimize your code.
  - Validate data extraction results.

### How to Use:
1. Enter the URL of the website you want to scrape.
2. Choose the scraping options and parameters.
3. Click the "Scrape" button to start the process.
4. View and download the scraped data.

### About the Project:
The Web Scraping Project is an open-source initiative aimed at providing tools and resources for efficient web scraping. Whether you are a data scientist, researcher, or developer, this platform offers a comprehensive solution for your web scraping needs. Our goal is to simplify the process of data extraction and make it accessible to everyone.

### Get Started:
Use the sidebar to navigate through different functionalities and start scraping data now!
""")

# Footer
st.markdown('<div class="footer">© 2025 Web Scraping Project. All rights reserved.</div>', unsafe_allow_html=True)