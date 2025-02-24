'''
Feel free to email me at peterwahomemaina003@gmail.com

This code is helpful to Techies and anyone in general
this is a web scraper in python
It scrapes and searches for the desired jobs through LinkedIn and acts as linked in premium

It comes with the necessary links for easier navigation and application

you can run this code on a python environment or use jupiter notebooks (Recommended)
'''
#Install neccesary dependancies
!pip install BeautifulSoup
!pip install requests

import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

def scrape_linkedin_jobs(search_term, location):
    """Scrapes job data (title, company, link, and date) from LinkedIn."""
    url = f"https://www.linkedin.com/jobs/search/?keywords={search_term}&location={location}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, "html.parser")
    job_data = []
    time_threshold = datetime.now() - timedelta(hours=72)

    for job_element in soup.find_all("div", class_="base-card"):
        job_title_element = job_element.find("h3", class_="base-search-card__title")
        company_element = job_element.find("h4", class_="base-search-card__subtitle")
        link_element = job_element.find("a", class_="base-card__full-link")
        date_element = job_element.find("time")  

        if job_title_element and company_element and link_element and date_element:
            job_title = job_title_element.text.strip()
            company = company_element.text.strip()
            link = link_element["href"]
            date_text = date_element.get("datetime", "").strip()  

            try:
                
                job_date = datetime.strptime(date_text, "%Y-%m-%d")
                
                if job_date.date() >= time_threshold.date():  
                    job_data.append({"title": job_title, "company": company, "link": link, "date": job_date})
            except ValueError:
                continue  

    return job_data


search_term = "Software Engineer"
location = "Kenya"

job_data = scrape_linkedin_jobs(search_term, location)
print("Found jobs in the last 72 hours:")
for job in job_data:
    print(f"Title: {job['title']}")
    print(f"Company: {job['company']}")
    print(f"Link: {job['link']}")
    print(f"Date: {job['date'].strftime('%Y-%m-%d')}")
    print("-" * 20)