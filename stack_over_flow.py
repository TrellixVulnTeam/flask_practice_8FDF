import requests
from bs4 import BeautifulSoup

ASK = 'q=python'
URL = 'https://stackoverflow.com/jobs'


def get_last_page():
    result = requests.get(f'{URL}?{ASK}')
    soup = BeautifulSoup(result.text, 'html.parser')
    pages = soup.find_all('a', {'class': 's-pagination--item'})
    last_page = pages[-2].get_text(strip=True)
    return int(last_page)


def get_jobs_info(job):
    url_number = job['data-jobid']
    title = job.find('a', {'class': 's-link'}).get_text(strip=True)
    location = []
    company, location = job.find('h3').find_all(
        'span', recursive=False)
    company = company.get_text(strip=True)
    location = location.get_text(strip=True)
    return{'title': title, 'company': company, 'location': location, "link": f'{URL}/{url_number}'}


def get_jobs(last_page, word):
    ASK = f'q={word}'
    jobs = []
    for page in range(last_page):
        print(f"Scraping stackOverFlow page:{page}")
        result = requests.get(f"{URL}?{ASK}&pg={page+1}")
        soup = BeautifulSoup(result.text, 'html.parser')

        job_box = soup.find('div', {'class': 'listResults'}).find_all(
            'div', {'class': '-job'})

        for job in job_box:
            jobs.append(get_jobs_info(job))
    return jobs


def get_stackOverFlow_jobs(word):
    last_page = get_last_page()
    true_last = 7
    jobs = get_jobs(true_last, word)
    return jobs
