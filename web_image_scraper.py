# David Kislyak
# web_image_scraper.py
# Image crawler for sites

from requests_html import HTMLSession
import wget
import ssl
import sys

# -----Scraper functions-----
# TODO: Parametrize image location for param scrapes
IMAGES_DIRECTORY = "./images"


# single image downloader
def get_image(url: str):
    # Fixes SSL Error
    ssl._create_default_https_context = ssl._create_unverified_context
    wget.download(url, IMAGES_DIRECTORY)


# page multiple images scrape
def scrape_page(url: str):
    # Create Instance
    session = HTMLSession()

    # Retrieve html content
    r = session.get(url).html

    # Trigger javascript dynamic images (causes 0.05 - 3.0 scrape delay)
    # TODO: add launch parameter to enable and disable JS image scraping
    r.render()

    # Find all image elements
    b = r.find("img", first=False)

    # Split each element into a parameter Dict (like src, alt, etc...)
    # and retrieve url from "src" key
    if len(b) == 1:
        get_image(url[0:-1] + (b[0].attrs['src']))
    else:  # Multiple image elements
        for i in b:
            get_image(url[0:-1] + i.attrs['src'])


# -----User Selection functions-----
def parameter_scrape():
    if sys.argv[1] == "-h" or sys.argv[1] == "--help":
        print("ImageScraper usage:\n"
              + "-h\n"
              + "--help         :to see this menu.\n"
              + "-i <url>\n"
              + "--image <url>  :to scrape a single image.\n"
              + "-p <url>\n"
              + "--page <url>   :to scrape all images off a page.\n")

    elif sys.argv[1] == "-i" or sys.argv[1] == "--image":
        get_image(sys.argv[2])

    elif sys.argv[1] == "-p" or sys.argv[1] == "--page":
        scrape_page(sys.argv[2])


def interactive_scrape():
    print("What would you like to scrape:\n"
          + "1.) A single image?\n"
          + "2.) An entire page of images?\n")
    menu_selection = input("Please enter your selection: ")

    if menu_selection == "1":
        page_url = input("Enter the url of the image you would like scraped:")
        get_image(page_url)
    elif menu_selection == "2":
        page_url = input("Enter the url of the image you would like scraped:")
        scrape_page(page_url)
    # TODO: implement error message/reprompt for incorrect user input


if __name__ == "__main__":
    if len(sys.argv) >= 2:
        parameter_scrape()
    else:
        interactive_scrape()
