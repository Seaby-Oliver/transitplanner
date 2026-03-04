# Imports
import urllib.request, json
from astroquery.ipac.nexsci.nasa_exoplanet_archive import NasaExoplanetArchive
import matplotlib.pyplot as plt
import pandas as pd
from .core.visibility import find_observable_exoplanets
from .observability.enrich import enrich_planets
from .observability.snr import snr_formula
from .io.summary import check_observability_table
from .observability.filters import apply_filters
from .lightcurve.simulator import generate_lightcurve
from .lightcurve.plotting import plot_lightcurve
from .io.nasa import load_nasa_data
from .io.exoclock import load_exoclock_data

import time
import tracemalloc

tracemalloc.start()

def main():
    # User inputs
    longitude = float(input("Enter longitude (degrees): "))
    latitude = float(input("Enter latitude (degrees): "))
    telescope_aperture_inches = float(input("Enter telescope aperture (inches): "))
    DEC_MIN = float(input("Enter min declination (deg): "))
    DEC_MAX = float(input("Enter max declination (deg): "))
    SNR_LIM = float(input("Enter min SNR: "))
    start_date_str = input("Enter start date (dd/mm/yy): ")
    span_days = int(input("Enter observation span (days): "))
    min_altitude = float(input("Enter min altitude (deg): "))


    start = time.time()
    
    # 1. Visibility stage
    planet_list = find_observable_exoplanets(
        longitude,
        latitude,
        start_date_str,
        span_days,
        min_altitude,
        telescope_aperture_inches
    )
    
    end = time.time()
    Run_time_target_prediction = end - start
    
    if not planet_list:
        print("No transits found in the observing window.")
        return

    start = time.time()

    # 2. Load catalogues
    exoclock_planets = load_exoclock_data()

    end = time.time()
    Run_time_loading_ExoClock = end - start

    length_of_exoclock_database = len(exoclock_planets)
    start = time.time()

    nasa=load_nasa_data()

    end = time.time()
    Run_time_loading_NASA = end - start
    
    # 3. Enrich planet data
    planet_list = enrich_planets(planet_list, exoclock_planets, nasa)
    

    start = time.time()
    
    # 4. Compute SNR and observability
    for planet in planet_list:
        duration_min = planet["Duration (hours)"] * 60

        planet["SNR"] = snr_formula(
            planet["R Magnitude"],
            planet["Transit Depth (mmag)"],
            duration_min,
            telescope_aperture_inches
        )
        planet["Status"] = "Observable" if apply_filters(planet, DEC_MIN, DEC_MAX, SNR_LIM) else "Not Observable"
        
    end = time.time()    
    Run_time_visibility = end - start 

    # 5. Summary table
    check_observability_table(
        planet_list,
        export_csv="exoplanet_summary.csv",
        export_excel="exoplanet_summary.xlsx"
    )

    # 6. Select observable planets
    observable_planets = [p for p in planet_list if p["Status"] == "Observable"]
  
    if not observable_planets:
        print("No observable planets in the selected window.")
        return

    print("Observable planets:")
    for i, planet in enumerate(observable_planets):
        print(f"{i+1}. {planet['Object']} - Transit at {planet['Transit Start (UTC)']}")

    selection = int(input("Select planet number to model: ")) - 1

    start = time.time()
    
    target_name = observable_planets[selection]["Object"]
    snr = observable_planets[selection]["SNR"]

    # 7. Light curve
    obstime, flux, info = generate_lightcurve(target_name, snr)

    print(f"Observation Time: {(info['duration_hours']+ 2):.3f}")
    print(f"Predicted duration: {info['duration_hours']:.3f} hours")
    print(f"Predicted depth: {info['depth_mag']:.3f} mag")
    print(f"Estimated error: {info['error']:.5f}")
    
    plot_lightcurve(obstime, flux, info, title=f"{target_name} Predicted Light Curve")

    end = time.time()
    Run_time_LIGHT_curve_prediction = end - start
    
    current, peak = tracemalloc.get_traced_memory()
    print(" ")
    print("Peak memory usage:", peak / 10**6, "MB")
    tracemalloc.stop()
    
    print(" ")
    print("no of planets processed:",length_of_exoclock_database)
    print("transit prediction runtime:", Run_time_target_prediction, "seconds")
    print("ExoClock data  runtime:", Run_time_loading_ExoClock, "seconds")
    print("NASA data runtime:", Run_time_loading_NASA, "seconds")
    print("visibility constarints runtime:", Run_time_visibility, "seconds")
    print("light curve prediction runtime:", Run_time_LIGHT_curve_prediction, "seconds")

   
if __name__ == "__main__":
    main()





























