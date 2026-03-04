import urllib.request, json
from datetime import datetime, timedelta
import numpy as np
from astropy.time import Time
from astropy.coordinates import SkyCoord, EarthLocation, AltAz
from astroplan import Observer
import astropy.units as u
from .geometry import radec_to_altaz
from .ephemeris import next_transit
from ..io.exoclock import load_exoclock_data




def find_observable_exoplanets(
        longitude, latitude,
        start_date_str, span_days,
        min_altitude,
        telescope_aperture_inches):

    start_date = datetime.strptime(start_date_str, "%d/%m/%y")
    end_date = start_date + timedelta(days=span_days)

    # ------------------------- Change 1: Pre-create location and observer once -------------------------
    location = EarthLocation(lat=latitude*u.deg, lon=longitude*u.deg)
    observer = Observer(location=location, name="Observer", timezone="UTC")
    # -----------------------------------------------------------------------------------------------

    # ------------------------- Change 2: Precompute start/end times once -----------------------------
    t_start = Time(start_date)
    t_end   = Time(end_date)
    t_start_bjd = t_start.tdb.jd
    # -----------------------------------------------------------------------------------------------

    exoclock_planets = load_exoclock_data()
    results = []

    for planet in exoclock_planets.values():

        if "min_telescope_inches" not in planet:
            continue
        if planet["min_telescope_inches"] > telescope_aperture_inches:
            continue

        ra = planet.get("ra_j2000")
        dec = planet.get("dec_j2000")
        if ra is None or dec is None:
            continue

        try:
            coord = SkyCoord(ra=ra, dec=dec, unit=(u.hourangle, u.deg))
        except Exception:
            continue

        t0 = planet.get("ephem_mid_time")
        period_days = planet.get("ephem_period")
        duration_hours = planet.get("duration_hours")
        depth_mmag = planet.get("depth_r_mmag")
        r_mag = planet.get("r_mag")

        if t0 is None or period_days is None or duration_hours is None:
            continue

        # ------------------------- Change 3: Precompute half duration once -----------------------------
        half_duration = (duration_hours / 2.0) * u.hour
        # -----------------------------------------------------------------------------------------------

        current_mid_jd = next_transit(t0, period_days, t_start_bjd)
        current_mid = Time(current_mid_jd, format="jd", scale="tdb")

        while current_mid <= t_end:

            transit_start = current_mid - half_duration
            transit_end   = current_mid + half_duration

            # ------------------------- Change 4: Vectorized Sun altitude call -----------------------------
            sun_times = Time([transit_start, current_mid, transit_end])
            sun_altitudes = observer.sun_altaz(sun_times).alt.deg  # returns array of 3
            sun_alt_start, sun_alt_mid, sun_alt_end = sun_altitudes
            # -----------------------------------------------------------------------------------------------

            # Skip transit if Sun is not fully below -18 deg at all key times
            if not (sun_alt_start < -18 and sun_alt_mid < -18 and sun_alt_end < -18):
                current_mid += period_days * u.day
                continue

            # ------------------------- Change 5: Pre-create AltAz frames ----------------------------------
            frame_start = AltAz(obstime=transit_start, location=location)
            frame_mid   = AltAz(obstime=current_mid, location=location)
            frame_end   = AltAz(obstime=transit_end, location=location)

            alt_start, az_start = coord.transform_to(frame_start).alt.deg, coord.transform_to(frame_start).az.deg
            alt_mid,   az_mid   = coord.transform_to(frame_mid).alt.deg,   coord.transform_to(frame_mid).az.deg
            alt_end,   az_end   = coord.transform_to(frame_end).alt.deg,   coord.transform_to(frame_end).az.deg
            # -----------------------------------------------------------------------------------------------

            #if not (
            #    alt_start >= min_altitude and
            #    alt_mid >= min_altitude and
            #    alt_end >= min_altitude
            #):
            #    current_mid += period_days * u.day
            #    continue

            results.append({
                "Object": planet["name"],
                "Priority": planet.get("priority"),
                "Min Aperture (inches)": planet.get("min_telescope_inches"),
                "RA": ra,
                "Dec": dec,
                "R Magnitude": r_mag,
                "Transit Depth (mmag)": depth_mmag,
                "Duration (hours)": float(round(duration_hours, 2)),
                "Transit Start (UTC)": transit_start.utc.iso,
                "Mid-Transit (UTC)": current_mid.utc.iso,
                "Transit End (UTC)": transit_end.utc.iso
            })

            current_mid += period_days * u.day

    return results
                
                

