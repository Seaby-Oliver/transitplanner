User Guide
===========

This is the user guide on the transitplanner code, mean to explain what each part of the code does to
any individual who whishes to use it

Overview
--------

This tool computes predicted transit times for known exoplanets, given their
orbital parameters and an observing time window, using your location and telescope parameters which you input. It is intended for planning
photometric observations, helping you identify which targets are observable from the given site and when their transits occur.

This guide explains each step of the workflow in more detail than the Quick Start, including input parameters, output interpretation, and recommended observing practices.

Input Parameters
----------------

TransitPlanner requires several pieces of information to be provided by the user in order compute observable
targets. These are entered interactively in the CLI, but their meaning is
explained here.

**Longitude / Latitude**
    Geographic coordinates of the observatory in degrees. Positive longitude is
    east of Greenwich.

**Telescope aperture**
    Diameter of the telescope in inches. Used to estimate achievable SNR.

**Declination limits**
    Minimum and maximum declination the telescope can access.

**Minimum SNR**
    The lowest acceptable signal-to-noise ratio for a transit to be considered
    observable.

**Start date**
    Beginning of the observing window, in ``dd/mm/yy`` format.

**Observation span**
    Number of days after the start date to search for transits.

**Minimum altitude**
    Minimum altitude (in degrees) the target must reach during transit.

Running the CLI
---------------

TransitPlanner includes an interactive command-line interface.  
To launch it, run::

    python -m transitplanner.cli

The program will check NASA and exoclock databases and then prompt you for
observatory information such as longitude, latitude, telescope aperture, and
observation constraints.

After this, the CLI will prompt you for observatory and instrument parameters.
Each prompt includes validation to ensure values are within reasonable ranges.

How Targets Are Selected
------------------------

TransitPlanner evaluates each known exoplanet using the following criteria:

1. **Transit occurs within the specified date range.**
2. **Target is above the minimum altitude** at some point during transit.
3. **Declination is within the user-defined limits.**
4. **Estimated SNR exceeds the minimum threshold.**
5. **Transit depth and duration are sufficient for detection** with the given
   telescope aperture.

The result is a numbered list of all planets meeting these constraints.

Selecting a Target
------------------

Once the list of observable planets is displayed, select a target by entering
its **number**, not its name.

For example: Enter planet number: 31

Interpreting the Output
-----------------------

After selecting a target, TransitPlanner provides several key quantities:

**Observation Time**
    Total time the target remains above the minimum altitude during transit.

**Predicted Duration**
    Expected duration of the transit in hours.

**Predicted Depth**
    Estimated transit depth in magnitudes.

**Estimated Error**
    Expected photometric uncertainty based on telescope aperture and target
    brightness.

A model light curve is also generated to illustrate the expected signal shape.

How TransitPlanner Builds the Observable Planet List
----------------------------------------------------

The CLI brings together several internal modules, each responsible for a
different stage of the workflow. When the user enters their observing
parameters, the following sequence occurs:

1. **Visibility calculation**
   Module: ``core.visibility.find_observable_exoplanets``  
   This function computes which exoplanets have transits occurring within the
   user’s date range and are above the minimum altitude at the specified
   longitude and latitude. The output is a preliminary list of geometrically
   visible planets.

2. **Catalogue loading**
   Modules:
   - ``io.nasa.load_nasa_data``  
   - ``io.exoclock.load_exoclock_data``  

   These functions load ephemeris and photometric data from NASA Exoplanet
   Archive and ExoClock. This includes period, T0, transit depth, magnitude, and
   duration.

3. **Data enrichment**
   Module: ``observability.enrich.enrich_planets``  
   The visibility list is merged with catalogue data so each planet now has
   complete information needed for SNR and observability calculations.

4. **Signal-to-noise estimation**
   Module: ``observability.snr.snr_formula``  
   For each planet, the expected SNR is computed using telescope aperture,
   transit depth, magnitude, and transit duration.

5. **Observability filtering**
   Module: ``observability.filters.apply_filters``  
   Declination limits and SNR thresholds are applied. Each planet is labelled as
   *Observable* or *Not Observable*.

6. **Summary table generation**
   Module: ``observability.summary.check_observability_table``  
   A full table of all planets (including filtered-out ones) is exported as CSV
   and Excel files.

7. **Light curve simulation**
   Modules:
   - ``lightcurve.simulator.generate_lightcurve``  
   - ``lightcurve.plotting.plot_lightcurve``  

   After the user selects a planet from the observable list, a model transit
   light curve is generated and plotted. The CLI prints predicted duration,
   depth, and estimated photometric error.


Additional Notes
----------------

- When selecting a planet, enter the **number**, not the name.
- Dates must be entered in ``dd/mm/yy`` format.
- Some transits may be excluded if ephemeris uncertainty is high.





