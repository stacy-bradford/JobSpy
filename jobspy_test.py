import csv
import logging
import pandas as pd
from jobspy import scrape_jobs

# 🔹 Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# 🔹 Define Scraper Settings for Indeed
jobs = scrape_jobs(
    site_name=["indeed"],  # ✅ Focus only on Indeed
    search_term="software engineer",
    location="San Francisco, CA",
    pages=3,  # ✅ Increase pages to get more jobs
    max_results=100,  # ✅ Try to get more results
    date_posted="last_24_hours"  # ✅ Ensure we get recent jobs
)

# 🔹 Check if we got results
if not jobs.empty:
    logging.info(f"✅ Scraped {len(jobs)} jobs from Indeed.")

    # ✅ Drop unnecessary columns & clean up data
    valid_columns = ["title", "company", "location", "description"]
    jobs = jobs[[col for col in valid_columns if col in jobs.columns]]
    
    # ✅ Remove duplicate job postings
    jobs.drop_duplicates(subset=["title", "company", "location"], keep="first", inplace=True)

    # ✅ Clean text fields (e.g., remove HTML from descriptions)
    jobs["description"] = jobs["description"].str.replace(r"<.*?>", "", regex=True)

    # ✅ Fill missing values with empty strings to prevent issues
    jobs.fillna("", inplace=True)

    # ✅ Convert to list of dicts for CSV writing
    jobs_dicts = jobs.to_dict(orient="records")

    # ✅ Define CSV filename
    csv_filename = "jobs.csv"

    # ✅ Save to CSV
    with open(csv_filename, "w", newline="", encoding="utf-8") as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=jobs.columns)
        dict_writer.writeheader()
        dict_writer.writerows(jobs_dicts)

    logging.info(f"📂 Indeed jobs saved to {csv_filename}")

else:
    logging.warning("⚠️ No jobs found on Indeed. Try adjusting search parameters.")
