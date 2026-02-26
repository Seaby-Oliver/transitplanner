Installation
=============

This is how to install the transitplanner python package to help you observe your exoplanet transits onto your system

Prerequisites
-------------

Before installing, ensure you have the following:

- **Python 3.10 or later**  
  To check your Python version, open Command Prompt and run::  

      python --version

  If Python is not installed, download it from the official website and ensure you tick  
  **"Add Python to PATH"** during installation.

- **pip (Python package manager)**  
  Check if pip is installed by running::  

      pip --version

  If pip is missing, reinstall Python and ensure the "Add to PATH" option is selected.

- **Git (required if cloning the repository manually)**  
  Check if Git is installed by running::  

      git --version

  If Git is not installed, download it from the official Git website.

- **(Optional but recommended) A virtual environment**  
  This keeps your installation isolated from other Python packages.  
  Create one with::  

      python -m venv venv

  Activate it on Windows with::  

      venv\Scripts\activate


Installing from GitHub
----------------------

The project can be installed directly from the GitHub repository using ``pip``::

    pip install git+https://github.com/Salmanul-Farisi-551/transitplanner.git

Verifying the Installation
--------------------------

To confirm the installation was successful, run::

    python -m transitplanner --help

If the help message appears, the installation is complete.

Troubleshooting
---------------

If you encounter issues:

- Ensure your virtual environment is activated.
- Upgrade pip::

      pip install --upgrade pip

- Check that Python and Git are correctly installed.



