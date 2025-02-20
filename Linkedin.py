'''
Feel free to email me at peterwahomemaina003@gmail.com

This code is helpful to Techies and anyone in general
this is a web scraper in python
It scrapes and searches for the desired jobs through LinkedIn and acts as linked in premium

It comes with the necessary links for easier navigation and application

you can run this code on a python environment or use jupiter notebooks (Recommended)
'''
#Install neccesary dependancies

!pip install beautifulsoup4
import requests
from bs4 import BeautifulSoup

def scrape_linkedin_jobs(search_term, location):
    """Scrapes job data (title, company, link) from LinkedIn."""
    url = f"https://www.linkedin.com/jobs/search/?keywords={search_term}&location={location}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, "html.parser")
    job_data = []

    for job_element in soup.find_all("div", class_="base-card"):
        job_title_element = job_element.find("h3", class_="base-search-card__title")
        company_element = job_element.find("h4", class_="base-search-card__subtitle")
        link_element = job_element.find("a", class_="base-card__full-link")

        if job_title_element and company_element and link_element:
            job_title = job_title_element.text.strip()
            company = company_element.text.strip()
            link = link_element["href"]  # Extract the href attribute for the link

            job_data.append({"title": job_title, "company": company, "link": link})

    return job_data


search_term = "Software Engineer" #Replace the software engineer with the niche or job uou are looking for
location = "Kenya" #REplace this with desired country

job_data = scrape_linkedin_jobs(search_term, location)
print("Found jobs:")
for job in job_data:
    print(f"Title: {job['title']}")
    print(f"Company: {job['company']}")
    print(f"Link: {job['link']}")
    print("-" * 20)  # Separator