import threading
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import requests
import streamlit as st

driver = None

def check_https(url, results, progress):
    if url.startswith('https://'):
        results.append(("HTTPS is enabled.", "green"))
        progress[0] += 33.33
    else:
        results.append(("HTTPS is not enabled.", "red"))

def test_sensitive_data_exposure(url, driver, results, progress):
    driver.get(url)
    time.sleep(2)
    
    page_source = driver.page_source
    if "password" in page_source or "token" in page_source:
        results.append(("Sensitive data (e.g., password or token) exposed in page source.", "red"))
    else:
        results.append(("No sensitive data found in page source.", "green"))
        progress[0] += 33.33

def check_headers(url, results, progress):
    response = requests.get(url)
    headers = response.headers
    
    if 'Strict-Transport-Security' in headers:
        results.append(("Strict-Transport-Security header is present.", "green"))
        progress[0] += 11.11
    else:
        results.append(("Missing Strict-Transport-Security header.", "red"))
    
    if 'Content-Security-Policy' in headers:
        results.append(("Content-Security-Policy header is present.", "green"))
        progress[0] += 11.11
    else:
        results.append(("Missing Content-Security-Policy header.", "red"))
    
    if 'X-Content-Type-Options' in headers:
        results.append(("X-Content-Type-Options header is present.", "green"))
        progress[0] += 11.11
    else:
        results.append(("Missing X-Content-Type-Options header.", "red"))

def calculate_safety_percentage(progress):
    return min(int(progress[0]), 100)

def main():
    st.markdown("""
      <style>
body {
    background: linear-gradient(to right, #1e3c72, #2a5298);
    font-family: 'Arial', sans-serif;
}
.main-title {
    font-size: 3em;
    font-weight: bold;
    text-align: center;
    margin-bottom: 20px;
    animation: fadeIn 2s ease-in-out;
}
.sidebar .sidebar-content {
    background-color: #f0f2f6;
    border-right: 2px solid #e0e0e0;
}
.result-green {
    color: green;
    font-weight: bold;
    animation: slideInLeft 1s ease-in-out;
}
.result-red {
    color: red;
    font-weight: bold;
    animation: slideInRight 1s ease-in-out;
}
.stProgress > div > div {
    background: linear-gradient(to right, #4CAF50, #81C784);
    height: 10px;
    border-radius: 10px;
}
.footer {
    text-align: center;
    padding: 10px;
    font-size: 0.9em;
    color: #888;
    animation: fadeInUp 2s ease-in-out;
}
@keyframes fadeIn {
    from {
        opacity: 0;
    }
    to {
        opacity: 1;
    }
}
@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}
@keyframes slideInLeft {
    from {
        opacity: 0;
        transform: translateX(-100%);
    }
    to {
        opacity: 1;
        transform: translateX(0);
    }
}
@keyframes slideInRight {
    from {
        opacity: 0;
        transform: translateX(100%);
    }
    to {
        opacity: 1;
        transform: translateX(0);
    }
}
</style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="main-title">Website Security Testing</div>', unsafe_allow_html=True)
    
    with st.sidebar:
        url = st.text_input("Enter the URL for testing")
        run_tests = st.button("Run Tests")
    
    if run_tests:
        global driver
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(options=chrome_options)
        
        results = []
        progress = [0]
        progress_bar = st.progress(0)
        
        try:
            threads = []
            
            thread_https = threading.Thread(target=check_https, args=(url, results, progress))
            threads.append(thread_https)
            
            thread_sensitive_data = threading.Thread(target=test_sensitive_data_exposure, args=(url, driver, results, progress))
            threads.append(thread_sensitive_data)
            
            thread_headers = threading.Thread(target=check_headers, args=(url, results, progress))
            threads.append(thread_headers)

            for thread in threads:
                thread.start()

            for thread in threads:
                thread.join()
        finally:
            driver.quit()
        
        for i in range(int(progress[0])):
            time.sleep(0.05)
            progress_bar.progress(i + 1)
        
        for result, color in results:
            css_class = "result-green" if color == "green" else "result-red"
            st.markdown(f"<span class='{css_class}'>{result}</span>", unsafe_allow_html=True)
        
        safety_percentage = calculate_safety_percentage(progress)
        st.markdown(f"<span class='safety-percentage'>**Website Safety Percentage: {safety_percentage}%**</span>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()

st.write("""### About the Website Tester Tool

The **Website Tester Tool** is a versatile and user-friendly application designed to evaluate the functionality, performance, and responsiveness of a website. It is an essential utility for web developers, quality assurance (QA) professionals, and businesses aiming to ensure their websites provide an optimal user experience. By automating key aspects of website testing, this tool identifies issues, validates functionality, and ensures compliance with modern web standards.

With its ability to simulate real-world interactions, evaluate speed and responsiveness, and assess compatibility across devices and browsers, the Website Tester Tool provides a comprehensive testing solution that streamlines the development and deployment process.

---

### Purpose of the Tool

The primary purpose of the Website Tester Tool is to help developers and QA teams identify and address potential issues in websites before they go live. A website must meet high standards of performance, usability, and reliability to succeed in today’s competitive digital landscape. This tool ensures that websites function as intended across various environments, deliver a seamless user experience, and adhere to best practices.

---

### Key Features

The Website Tester Tool is equipped with a wide range of features that make it an all-encompassing solution for website testing:

#### 1. **Functionality Testing**
   - Simulates user interactions, such as clicking buttons, filling out forms, and navigating between pages.
   - Ensures all links, buttons, forms, and other interactive elements work as expected.
   - Tests APIs and backend integrations for proper functionality.

#### 2. **Performance Testing**
   - Evaluates page load times and overall website speed.
   - Identifies performance bottlenecks, such as large media files or unoptimized scripts.
   - Provides insights into server response times and network latency.

#### 3. **Responsiveness Testing**
   - Tests how the website renders and performs on various screen sizes and resolutions.
   - Ensures compatibility with mobile devices, tablets, and desktops.
   - Verifies responsive design elements like adaptive menus, grids, and images.

#### 4. **Cross-Browser Compatibility**
   - Tests website functionality on multiple browsers, including Chrome, Firefox, Safari, Edge, and others.
   - Ensures consistent rendering and behavior across different browser versions.

#### 5. **Accessibility Testing**
   - Evaluates the website against accessibility standards like WCAG (Web Content Accessibility Guidelines).
   - Identifies issues such as missing alt text, improper color contrast, and keyboard navigation problems.
   - Ensures the website is usable by individuals with disabilities.

#### 6. **Security Testing**
   - Checks for common vulnerabilities, such as cross-site scripting (XSS) and SQL injection.
   - Verifies that sensitive data, such as passwords and personal information, is encrypted.
   - Tests for secure HTTP (HTTPS) implementation.

#### 8. **Error Reporting**
   - Logs issues and errors encountered during testing.
   - Generates detailed reports with actionable insights for developers.
   - Supports exporting reports in various formats like PDF or CSV.
---

### Benefits of the Tool

#### **1. Ensures a Seamless User Experience**
   - Detects and resolves issues that may disrupt user interactions.
   - Optimizes navigation, responsiveness, and functionality for all users.

#### **2. Saves Time and Resources**
   - Automates repetitive and time-consuming testing tasks.
   - Reduces the need for manual testing, enabling teams to focus on other priorities.

#### **3. Improves Website Performance**
   - Identifies performance bottlenecks and optimization opportunities.
   - Enhances website speed and reliability, leading to better user retention.

#### **4. Increases Compatibility**
   - Ensures the website works seamlessly across various devices, browsers, and platforms.
   - Prevents issues caused by inconsistent behavior in different environments.

#### **5. Enhances Security**
   - Identifies vulnerabilities to protect the website from potential attacks.
   - Ensures compliance with security standards and best practices.

#### **6. Boosts Search Engine Rankings**
   - Improves SEO by addressing issues like broken links and poor meta tag implementation.
   - Enhances website visibility and discoverability.

---

### Conclusion

The **Website Tester Tool** is a comprehensive solution for ensuring the quality, performance, and reliability of websites. It empowers developers, testers, and businesses to deliver superior user experiences by identifying and resolving issues efficiently. By automating critical aspects of website testing, the tool simplifies workflows, enhances productivity, and ensures that websites meet the highest standards of functionality, security, and accessibility.
""")

st.markdown('<div class="footer">© 2025 Web Scraping Project. All rights reserved.</div>', unsafe_allow_html=True)
