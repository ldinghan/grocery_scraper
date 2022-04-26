from ntuc_scraper import scrape as NTUCscrape
from giant_scraper import scrape as GIANTscrape
from displaydata import getSheet
import os

def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)

def main():
	chromedriver_path = "C:/Users/user/.wdm/drivers/chromedriver/win32/99.0.4844.51/chromedriver.exe"
	count = 0
	with open('grocery.txt', 'r') as f:
		items = f.readlines()
		total = len(items)
		print(items)

		for query in items:
			print("\n")
			print(query)
			getSheet(query, NTUCscrape(query, chromedriver_path), GIANTscrape(query, chromedriver_path))
			count += 1
			clearConsole()
			print(f'{count} item(s) out of {total} completed')
	os.system('"xlwt result.xls"')


if __name__ == "__main__":
	#q = input("what do you want to search for?")
	main()
	
