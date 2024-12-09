from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup
from threading import Lock

app = FastAPI()

lock = Lock()

scraped_data = []

class ScrapeRequest(BaseModel):
    keyword: str

def scrape_jobs(keyword: str):
    """
    Scrape jobs from Wellfound for a specific keyword.
    """
    global scraped_data
    url = f"https://wellfound.com/role/{keyword}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://wellfound.com/",
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        companies = []
        positions = []
        additional_details = []

        for job_listing in soup.find_all("h2", class_="inline text-md font-semibold"):
            companies.append(job_listing.text.strip())
        
        for job_listing in soup.find_all("a", class_="mr-2 text-sm font-semibold text-brand-burgandy hover:underline"):
            positions.append(job_listing.text.strip())

        for job_listing in soup.find_all("span", class_="pl-1 text-xs"):
            additional_details.append(job_listing.text.strip())

        jobs = []
        for company, position, detail in zip(companies, positions, additional_details):
            jobs.append({
                "company": company,
                "title": position,
                "additional_details": detail,
            })

        with lock:
            scraped_data = jobs

    except Exception as e:
        print(f"Error during scraping: {e}")


@app.post("/scrape")
def start_scraping(request: ScrapeRequest, background_tasks: BackgroundTasks):
    """
    Start the scraping process in the background.
    """
    background_tasks.add_task(scrape_jobs, request.keyword)
    return {"message": "Scraping initiated. Fetch data later using /data."}

@app.get("/data")
def get_scraped_data():
    """
    Fetch the scraped data.
    """
    if not scraped_data:
        raise HTTPException(status_code=404, detail="No data available yet.")
    return {"jobs": scraped_data}

