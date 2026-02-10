# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import os
import sys
import django

# Add project root to Python path
sys.path.insert(0, os.path.abspath('../..'))

# Set Django settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'news_project.settings'
django.setup()

# Optional: use the Read the Docs theme
html_theme = 'sphinx_rtd_theme'



project = 'News Capstone Project'
copyright = '2026, mokati mojalefa'
author = 'mokati mojalefa'
release = '1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',  # supports Google-style docstrings
]


templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']
