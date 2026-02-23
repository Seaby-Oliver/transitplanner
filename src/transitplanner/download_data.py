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
