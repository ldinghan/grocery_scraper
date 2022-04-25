from ntuc_scraper import scrape as NTUCscrape
from giant_scraper import scrape as GIANTscrape
from displaydata import getSheet

def main():
	count = 0
	with open('grocery.txt', 'r') as f:
		items = f.readlines()
		total = len(items)
		print(items)

		for query in items:
			print("\n")
			print(query)
			getSheet(query, NTUCscrape(query), GIANTscrape(query))
			count += 1
			print(f'{count} item(s) out of {total} completed')



if __name__ == "__main__":
	#q = input("what do you want to search for?")
	main()
	
