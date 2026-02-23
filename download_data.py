"""
NASA Data Update Utility - TransitPlanner
-----------------------------------------
This script fetches the most recent planetary parameters from the NASA Exoplanet 
Archive and saves them as a local Parquet file.

WHY WE USE THIS:
1. Speed: Reading a local Parquet file takes <1 second, compared to 7+ minutes via API.
2. Stability: The program works offline and isn't affected if NASA's API is down.
3. Consistency: Ensures everyone on the team is using the same data version.

MAINTENANCE COMMANDS (Run these in your terminal to update the team):
1.  python download_data.py
2.  git add src/transitplanner/data/nasa_data.parquet
3.  git commit -m "Update NASA exoplanet database snapshot"
4.  git push origin main
"""

from astroquery.ipac.nexsci.nasa_exoplanet_archive import NasaExoplanetArchive
import pandas as pd
import os

print("Downloading data from NASA... this will take a few minutes.")
# This fetches the table
table = NasaExoplanetArchive.query_criteria("pscomppars")
df = table.to_pandas()

# This creates the data folder inside your src directory
data_dir = os.path.join("src", "transitplanner", "data")
os.makedirs(data_dir, exist_ok=True)

# This saves the file in the fast Parquet format
file_path = os.path.join(data_dir, "nasa_data.parquet")
df.to_parquet(file_path)

print(f"Success! File saved at: {file_path}")
