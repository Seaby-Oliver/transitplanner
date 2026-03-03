from astroquery.ipac.nexsci.nasa_exoplanet_archive import NasaExoplanetArchive

def load_nasa_data():
    table = NasaExoplanetArchive.query_criteria("pscomppars")
    df = table.to_pandas()
    df.set_index('pl_name', inplace=True)
    return df
