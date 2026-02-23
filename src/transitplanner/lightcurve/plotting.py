import matplotlib.pyplot as plt

def plot_lightcurve(obstime, flux, info, title="Light Curve"):
    """
    This function visualises the simulated transit flux as a function of
    observation time. It also overlays error bars at key transit phases,
    specifically ingress, mid transit and egress.

    Marker indices and photometric uncertainty are provided through the
    info dictionary, which is produced by the light curve simulation stage.

    Parameters
    
    obstime : array-like
        Observation time array in hours from start of transit.
    flux : array-like
        Relative flux values for the lightcurve.
    info : dict
        Dictionary containing lightcurve metadata, including markers and errors.
    title : str, optional
        Plot title. Default is "Light Curve".

    
      it  Displays and saves the plot.
    """
    
    ingress, indepth, egress = info["markers"]
    error = info["error"]

    print(f"Observation Time: {(info['duration_hours']+ 2):.3f}")
    print(f"Predicted duration: {info['duration_hours']:.3f} hours")
    print(f"Predicted depth: {info['depth_mag']:.3f} mag")
    print(f"Estimated error: {info['error']:.5f}")
    plt.figure()
    plt.plot(obstime, flux)
    plt.errorbar(obstime[[ingress, indepth, egress]],  flux[[ingress, indepth, egress]], error, fmt="o", color="red" )
    plt.xlabel("Observation Time (Hours)")
    plt.ylabel("Relative Flux")
    plt.title(title)
    plt.savefig("lightcurve.png", dpi=150, bbox_inches="tight")
    plt.show()

