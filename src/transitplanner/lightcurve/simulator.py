import numpy as np
import pylightcurve as plc

def generate_lightcurve(planet_name, snr, filter="COUSINS_R"):
    """

    This function retrieves transit parameters using pylightcurve, constructs
    a time array for the observation window, computes relative flux, magnitude,
    and error estimates based on the SNR, and identifies key transit markers.

    Parameters
    planet_name .
    snr.
    filter 

    Returns
    obstime :
        Observation time array in hours from start of transit.
    transit_flux : 
        Relative flux values for the synthetic lightcurve.
    info :
        Dictionary containing additional lightcurve metadata:
            
    """

    planet = plc.get_planet(planet_name)
    startend = float('{:.3f}'.format((planet.transit_duration(filter) / 2) + 0.0417))
    time_array = np.arange(planet.mid_time - startend, planet.mid_time + startend, 0.001)
    obstime = (time_array - time_array[0]) * 24
    transit_flux = planet.transit(time_array, "BJD_TDB", filter)

    mag = -2.5 * np.log10(transit_flux / 100)
    magdepth = np.max(mag) - np.min(mag)

    indepth = np.abs(transit_flux - planet.transit_depth(filter)).argmin()
    ingress = np.abs(obstime - 1).argmin()
    endobs = obstime[-1] - 1
    egress = np.abs(obstime - endobs).argmin()
    grad = np.gradient(transit_flux)
    grad2 = np.gradient(grad)

    error = planet.transit_depth(filter) / snr
    t2 = ingress + (np.abs(grad2[ingress:indepth] - np.max(grad2)).argmin())
    t3 = indepth + (np.abs(grad2[indepth:egress]-np.max(grad2)).argmin())

    info = {
        "duration_hours": planet.transit_duration(filter) * 24,
        "depth_mag": magdepth,
        "depth_flux": planet.transit_depth(filter),
        "error": error,
        "markers": (ingress,t2, indepth, t3, egress),
    }

    return obstime, transit_flux, info
