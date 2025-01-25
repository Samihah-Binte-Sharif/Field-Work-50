"""
Author: Samihah Binte Sharif
Version: 1.0

This module demonstrates the usage of the `cloudscrapper` and the 'BeautifulSoup' library in Python for web scraping.
It covers various real-world examples including rendering JavaScript, extracting data, and
working with HTML elements. This script is designed as an educational tool for understanding
web scraping using Python.

"""

import cloudscraper
from bs4 import BeautifulSoup
from lxml import html

# def render_javascript(url):
#     """
#     Demonstrates how to render JavaScript using the `requests-html` library.
#     This function fetches the page content after JavaScript has been executed.

#     Parameters:
#     url : str
#         The URL of the website to scrape.

#     Returns:
#     None
#     """
#     session = HTMLSession()
#     try:
#         response = session.get(url)
#         response.html.render()  # This will download Chromium if not found
#         print("Rendered web page:", response.html.html)
#     except Exception as e:
#         print(f"An error occurred: {e}")
#     finally:
#         session.close()

def extract_information(url):
    """
    Extracts and prints specific information from a webpage using CSS selectors.

    Parameters:
    url : str
        The URL of the website to scrape.

    Returns:
    None
    """
    scraper = cloudscraper.create_scraper()
    try:
        response = scraper.get(url)
        if response.status_code == 200:
            print('Response Successful!!')
        else:
            print(f"Failed to fetch the webpage. Status code: {response.status_code}")
            
        soup = BeautifulSoup(response.text, 'html.parser')
        
        #print(soup.prettify())

        title_tag = soup.select('h2.text-contrast1 a')
        print(len(title_tag), "title tags found:")
        
        i=1
        for title in title_tag:
            print(f"Title {i}: {title.text}")
            i = i+1

        tree = html.fromstring(response.text)  # Create the lxml tree from the response

        # XPath for the publishing date 
        date_xpath = '/html/body/div[1]/div[1]/div[1]/header/div/div/div[4]/text()' 
        date = tree.xpath(date_xpath)

        if date:
            print("Publishing Date: ", date[0].strip())
        else:
            print("Publishing Date not found")
        
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    """
    Main function to execute the web scraping examples.
    """
    
    print("\nExtracting information from a web page...")
    extract_information('https://dailyamardesh.com/world')

if __name__ == "__main__":
    main()
