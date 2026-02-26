.. transitplanner documentation master file, created by
   sphinx-quickstart on Fri Feb  6 11:14:07 2026.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

transitplanner documentation
============================

Basic Problem
-------------

Future Exoplanet observations such as the proposed Ariel mission to study exoplanet atmospheres will require precise and up to date measurements
of the exoplanets transit timings and duration so that as little time as possible is wasted observing a star with no transit occuring.

The goal of this code is to give the user a selection of exoplanets to observe that are visible from their location and telescope parameters
such as aperture size and will give a sufficiently high signal to noise ratio in order to get a clear transit detection.

Once the position and telescope parameters are plugged in, a table of observable exoplanets will be produced with parameters such as exoplanet name,
position, star brightness, minimum required aperture size to observe, transit duration and next best observable time etc.

Once this is computed, the user can choose any planet they wish and observe the transit! After this it is suggested to produce a light curve of the data 
collected so a transit curve can be plotted in order to keep the transit duration and start/end times as up to date as possible by uploading it to
exoclock as all of this will help future observation missions.


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   Installation
   Quick Start
   User Guide
   Developer Guide

