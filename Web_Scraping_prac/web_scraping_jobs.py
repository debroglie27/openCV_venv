from bs4 import BeautifulSoup
import requests

html_text = requests.get('https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords=python&txtLocation=').text
soup = BeautifulSoup(html_text, 'lxml')
jobs = soup.find_all('li', class_='clearfix job-bx wht-shd-bx')

for job in jobs:
    published_date = job.find('span', class_='sim-posted').span.text

    if 'few' in published_date:
        company_name = job.find('h3', class_='joblist-comp-name').text.strip()
        skills = job.find('span', class_='srp-skills').text.replace(' ', '').strip()
        more_info = job.header.h2.a['href']

        print(f'\nCompany Name: {company_name}')
        print(f'Skills Required: {skills}')
        print(f'More Info: {more_info}')
