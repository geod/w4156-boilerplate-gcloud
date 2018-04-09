import urllib2
from bs4 import BeautifulSoup
import sys

def main():
    if len(sys.argv) != 2:
        print "usage: python2 event_scraper.py <valid-meetup-url>"
        sys.exit(1)

    scraper_url = sys.argv[1]
    page = urllib2.urlopen(scraper_url)
    soup = BeautifulSoup(page, 'html.parser')

    title_box = soup.find('h1', attrs={'class': 'pageHead-headline text--pageTitle'}) 

    title = title_box.text.strip()

    time_box = soup.find('span', attrs={'class': 'eventTimeDisplay-startDate'}) 

    time = time_box.text.strip()


if __name__ == "__main__":
    main()