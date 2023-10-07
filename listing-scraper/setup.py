from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

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
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="web scraping, real estate, property listings",
    url="https://github.com/tsayles/listing-scraper"
)

