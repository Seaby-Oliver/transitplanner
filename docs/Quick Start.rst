Quick Start
=============

This section provides the fastest way to begin using TransitPlanner after
installation.

Running the CLI
---------------

TransitPlanner includes an interactive command-line interface.  
To launch it, run::

    python -m transitplanner.cli

The program will check NASA and exoclock databases and then prompt you for
observatory information such as longitude, latitude, telescope aperture, and
observation constraints.

Example interactive session::

    python -m transitplanner.cli
    Enter longitude (degrees): 5
    Enter latitude (degrees): 5
    Enter telescope aperture (inches): 8
    Enter min declination (deg): -30
    Enter max declination (deg): 60
    Enter min SNR: 5
    Enter start date (dd/mm/yy): 19/02/26
    Enter observation span (days): 5
    Enter min altitude (deg): 20

Once the required information is entered, TransitPlanner will compute a list of
observable exoplanets numbered from 1 to x

The code may take a few seconds to minutes to run so be patient

Once it has finished it will produce a list of observable exoplanets with your constraints inputted earlier
After this you will be prompted to choose your exoplanet, do so and it will give you observing details such as::

	Observation Time: 4.938
	Predicted duration: 2.938 hours
	Predicted depth: 0.009 mag
	Estimated error: 0.00035

And then also produce a sample light curve from model data

Additional Notes
----------------

- When selecting a planet from the observable list, enter the **number**, not the
  planet name (e.g., enter ``31`` rather than ``XO-3b``).

- Dates must be entered in the format ``dd/mm/yy``. For example, use
  ``19/02/26`` instead of ``19/02/2026``.


