'''
Feel free to email me at peterwahomemaina003@gmail.com

This code is helpful to Techies and anyone in general
this is a web scraper in python
It scrapes and searches for the desired jobs through google and acts as Google in premium

It comes with the necessary links for easier navigation and application

you can run this code on a python environment eg google_colab(Recommended) or use jupiter notebooks 
'''


!pip install selenium
!apt-get update # Update package lists
!apt install chromium-chromedriver -y  # Install chromedriver
import os
os.environ["PATH"] += ":/usr/bin/chromedriver"  # Add chromedriver to PATH
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

def scrape_google_jobs(search_term, location):
    """Scrapes job data (title, company, link) from Google Jobs using Selenium."""
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run Chrome in headless mode (no GUI)
    options.add_argument('--no-sandbox')  # Required for running in Docker
    options.add_argument('--disable-dev-shm-usage')  # Required for running in Docker

    # Add User-Agent to mimic a real browser
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(options=options)
    url = f"https://www.google.com/search?q={search_term}+jobs+in+{location}"
    driver.get(url)

    job_data = []
    # Wait for job cards to load, increasing timeout to 20 seconds
    WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[data-sgocid='jobs']"))
    )

    job_cards = driver.find_elements(By.CSS_SELECTOR, "div[data-sgocid='jobs']")
    for job_card in job_cards:
        try:
            job_title = job_card.find_element(By.CSS_SELECTOR, 'div[role="heading"]').text.strip()
            company = job_card.find_element(By.CSS_SELECTOR, 'div[class*="company"]').text.strip()
            link = job_card.find_element(By.TAG_NAME, 'a').get_attribute('href')
            job_data.append({"title": job_title, "company": company, "link": link})

        except Exception as e:
            print(f"Error processing job card: {e}")
            continue

    driver.quit()
    return job_data

search_term = "Software Engineer"
location = "Nairobi"

job_data = scrape_google_jobs(search_term, location)
print("Found jobs on Google:")
for job in job_data:
    print(f"Title: {job['title']}")
    print(f"Company: {job['company']}")
    print(f"Link: {job['link']}")
    print("-" * 20)  