from setuptools import setup, find_packages

setup(
    name="listing-scraper",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "gspread",
        "oauth2client",
        "requests",
        "beautifulsoup4"
    ],
    author="Tom Sayles",
    author_email="TSayles@Soot-n-Smoke.com",
    description="A script to scrape property listings from Zillow, Redfin, and One Home and update them in a Google Sheet.",
    keywords="web scraping, real estate, property listings",
    url="https://github.com/tsayles/listing-scraper"
)
