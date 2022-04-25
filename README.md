# grocery_scraper

A Python web scraping project built using selenium. The programme takes in queries and searches for the items at supermarkets and stores that I frequent (Giant / Fairprice Supermarket). 

Features:
- Run on headless chrome
- Takes in input from .txt file
- Displays progress of items fetched / queried
- Stores data in a .xlsx file for simple reading and sorting / comparing
- Different queries are placed in different sheets of the same .xlsx file for grouping
- Takes approximately 30 seconds per query (may vary according to the number of products available that are similar to the query)
- Scalable and easy to expand to compare products from a wider variety of stores

To use:
- change the chrome webdriver path in the main.py file to the location of your chrome webdriver
- type out the items that you are looking out for in the grocery.txt file, separated line by line (i.e. each item on one line) - be as specific as possible for better results
- run the main.py file and wait for the scraping to be completed
- while the scraping is ongoing (file still running), do NOT open the xlsx file to prevent errors
- once the file has completed running, the xlsx file can now be opened for comparison of items





Required libraries / programmes:
- BeautifulSoup (bs4)
- Selenium
- xlwt
- chromedriver
