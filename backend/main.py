from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ScrapeRequest(BaseModel):
    keyword: str

def scrape_jobs(keyword: str):
    """
    Scrape jobs from Wellfound for a specific keyword.
    """
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
        images = []

        # Extract company names
        for job_listing in soup.find_all("h2", class_="inline text-md font-semibold"):
            companies.append(job_listing.text.strip())

        # Extract job titles (roles)
        for job_listing in soup.find_all("a", class_="mr-2 text-sm font-semibold text-brand-burgandy hover:underline"):
            positions.append(job_listing.text.strip())

        # Extract additional details
        for job_listing in soup.find_all("span", class_="pl-1 text-xs"):
            additional_details.append(job_listing.text.strip())

        # Extract and process image links
        for img_tag in soup.find_all("img", class_="rounded-2xl object-contain"):
            image_url = img_tag.get("src")
            if image_url and "https" in image_url:
                images.append(image_url.split("https://", 1)[-1])

        # Combine extracted data into jobs
        jobs = []
        for company, position, detail, image in zip(companies, positions, additional_details, images):
            jobs.append({
                "company": company,
                "title": position,
                "additional_details": detail,
                "image_link": f"https://{image}",
            })

        return jobs

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during scraping: {e}")



@app.post("/scrape")
def scrape_and_fetch(request: ScrapeRequest):
    """
    Scrape jobs and return the data in one request.
    """
    jobs = scrape_jobs(request.keyword)
    if not jobs:
        raise HTTPException(status_code=404, detail="No jobs found for the given keyword.")
    return {"jobs": jobs}
