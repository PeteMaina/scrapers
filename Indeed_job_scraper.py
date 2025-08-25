from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
from datetime import datetime, timedelta

# Setup Chrome for Colab
def get_driver():
    options = Options()
    options.binary_location = "/usr/bin/chromium-browser"
    options.add_argument("--headless")  # Run in headless mode (important for Colab)
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    return webdriver.Chrome(service=Service("/usr/bin/chromedriver"), options=options)

# Scraping Function
def scrape_indeed_jobs(query, location, days=4, num_pages=2):
    driver = get_driver()

    base_url = "https://www.indeed.com/jobs"
    job_listings = []

    for page in range(0, num_pages * 10, 10):
        url = f"{base_url}?q={query}&l={location}&start={page}"
        driver.get(url)
        time.sleep(5)  # Wait for page to load

        jobs = driver.find_elements(By.CLASS_NAME, "job_seen_beacon")

        for job in jobs:
            try:
                title = job.find_element(By.TAG_NAME, "h2").text
                company = job.find_element(By.CLASS_NAME, "companyName").text
                location = job.find_element(By.CLASS_NAME, "companyLocation").text
                post_date = job.find_element(By.CLASS_NAME, "date").text

                # Convert post date
                if "Today" in post_date:
                    post_date = datetime.now()
                elif "Yesterday" in post_date:
                    post_date = datetime.now() - timedelta(days=1)
                else:
                    try:
                        days_ago = int(post_date.split()[0])
                        post_date = datetime.now() - timedelta(days=days_ago)
                    except ValueError:
                        continue  # Skip invalid dates

                if post_date >= datetime.now() - timedelta(days=days):
                    job_listings.append({
                        "title": title,
                        "company": company,
                        "location": location,
                        "posted": post_date.strftime('%Y-%m-%d'),
                    })
            except Exception as e:
                continue

    driver.quit()
    return job_listings

# Example Usage
jobs = scrape_indeed_jobs("Software Engineer", "Nairobi")
for job in jobs:
    print(job)
