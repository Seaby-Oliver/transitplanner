Developer Guide
===================================

This guide provides an overview of the internal structure of TransitPlanner and
is intended for contributors or developers who want to extend or modify the
codebase.

Project Structure
-----------------

TransitPlanner is organised into several top-level packages:

- ``core`` – geometric visibility calculations
- ``observability`` – SNR estimation, filtering, summary tables
- ``lightcurve`` – transit simulation and plotting
- ``io`` – data loading from NASA Exoplanet Archive and ExoClock
- ``cli`` – user-facing command-line interface

Each package contains small, focused functions that are combined by the CLI to
form the full workflow.

CLI Workflow
------------

The CLI (``transitplanner/cli.py``) is the main entry point. It performs the
following steps:

1. Collects user inputs (location, telescope aperture, date range, constraints).
2. Calls ``core.visibility.find_observable_exoplanets`` to compute geometric
   visibility.
3. Loads catalogue data using ``io.nasa.load_nasa_data`` and
   ``io.exoclock.load_exoclock_data``.
4. Merges catalogue information with the visibility list using
   ``observability.enrich.enrich_planets``.
5. Computes SNR for each planet using ``observability.snr.snr_formula``.
6. Applies declination and SNR filters via ``observability.filters.apply_filters``.
7. Generates a summary table using ``observability.summary.check_observability_table``.
8. Prompts the user to select a planet and generates a model light curve using
   ``lightcurve.simulator.generate_lightcurve`` and
   ``lightcurve.plotting.plot_lightcurve``.

This modular design allows each subsystem to be developed independently.

Key Modules
-----------

**Visibility (``core.visibility``)**  
Handles altitude calculations, transit timing checks, and geometric filtering.

**Observability (``observability.*``)**  
Adds catalogue data, computes SNR, applies filters, and generates summary tables.

**Light Curve Simulation (``lightcurve.*``)**  
Creates synthetic transit light curves and plots them.

**Data Loading (``io.*``)**  
Fetches and parses data from NASA Exoplanet Archive and ExoClock.

Extending TransitPlanner
------------------------

To add new features:

- **New observability criteria**  
  Add a function in ``observability.filters`` and include it in the CLI loop.

- **New catalogue sources**  
  Add a loader in ``io`` and merge it in ``observability.enrich``.

- **New output formats**  
  Extend ``observability.summary`` or add new exporters.

- **New visualisations**  
  Add plotting functions in ``lightcurve.plotting``.

Testing
-------

Tests should be added for:

- visibility calculations  
- SNR estimation  
- data loading  
- light curve generation

Coding Standards
----------------

- Keep functions small and single-purpose.
- Document assumptions and units (degrees, hours, magnitudes, etc.).

