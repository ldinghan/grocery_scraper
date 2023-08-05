from ntuc_scraper import scrape as NTUCscrape
from displaydata import getSheet
import os

def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)

def main():
	chromedriver_path = "/usr/local/bin/chromedriver"
	count = 0
	with open('grocery.txt', 'r') as f:
		items = f.read().splitlines()
		total = len(items)
		print(items)

		for query in items:
			print("\n")
			print(query)
			getSheet(query, NTUCscrape(query, chromedriver_path))
			NTUCscrape(query, chromedriver_path)
			count += 1
			print(f'{count} item(s) out of {total} completed')

	os.system('open xlwt_result.xls')

if __name__ == "__main__":
	main()
	
