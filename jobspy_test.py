import csv
import logging
import pandas as pd
from jobspy import scrape_jobs

# 🔹 Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# 🔹 Scrape jobs from Indeed & LinkedIn
jobs = scrape_jobs(
    site_name=["indeed", "linkedin"],  # ✅ Still scraping both sites
    search_term="software engineer",
    location="San Francisco, CA",
    pages=25,  # ✅ Increased pages for deeper scraping
    max_results=500,  # ✅ Increased max job limit
    date_posted="last_24_hours"
)

# 🔹 Check if we got results
if not jobs.empty:
    logging.info(f"✅ Scraped {len(jobs)} jobs from Indeed & LinkedIn.")

    # ✅ Keep only relevant fields
    valid_columns = ["site", "title", "company", "location", "description"]
    jobs = jobs[[col for col in valid_columns if col in jobs.columns]]

    # ✅ Remove duplicate jobs (same title, company, and location)
    jobs.drop_duplicates(subset=["title", "company", "location"], keep="first", inplace=True)

    # ✅ Clean text fields (e.g., remove HTML from descriptions)
    jobs["description"] = jobs["description"].str.replace(r"<.*?>", "", regex=True)

    # ✅ Fill missing values with empty strings
    jobs.fillna("", inplace=True)

    # ✅ Convert to list of dicts for CSV writing
    jobs_dicts = jobs.to_dict(orient="records")

    # ✅ Save to jobs.csv
    csv_filename = "jobs.csv"
    with open(csv_filename, "w", newline="", encoding="utf-8") as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=jobs.columns)
        dict_writer.writeheader()
        dict_writer.writerows(jobs_dicts)

    logging.info(f"📂 Jobs saved to {csv_filename}")

else:
    logging.warning("⚠️ No jobs found. Try adjusting search parameters.")
