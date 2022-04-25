from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time

def scrape(query):
	chrome_options = Options()
	chrome_options.add_argument('--headless')
	chrome_options.add_argument('--no-sandbox')

	url = f"https://giant.sg/search?q={query}"
	s = Service("C:/Users/user/.wdm/drivers/chromedriver/win32/99.0.4844.51/chromedriver.exe")

	def scrollFunction(numberOfScrolls):
		for i in range(numberOfScrolls):
			driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
			time.sleep(3)



	driver = webdriver.Chrome(service=s, options = chrome_options)
	driver.get(url)

	productElement = BeautifulSoup(driver.page_source, 'html.parser').find("span", attrs={"class":"page-heading-title"})
	numberOfProducts = int(productElement.get_text().split(' ')[2])
	if numberOfProducts == 0:
		return f'No results found for "{query}"'
	numberOfScrolls = min(numberOfProducts // 36, 3)
	scrollFunction(numberOfScrolls)


	html = driver.page_source
	driver.quit()





	soup = BeautifulSoup(html, 'html.parser')

	items = soup.find_all("div", attrs={"class":"col-lg-2 col-md-4 col-6 col_product open-product-detail algolia-click open-single-page"})
	items_list = []

	for item in items:
		item_link = f"https://giant.sg{item['data-url']}"
		item_brand = item.find("a", attrs={"class":"to-brand-page"})
		item_name = item.find("a", attrs={"class":"product-link"}).get_text()
		if item_brand:
			item_brand = item_brand.get_text()
			item_name = f"{item_brand} {item_name}"
		item_amount = item.find("span", attrs={"class":"size"}) or item.find("span", attrs={"class":"gram-price"})
		item_amount = item_amount.get_text().strip("Size: ")
		current_price = item.find("div", attrs={"class":"price_now"}).get_text()
		current_item = {"name": item_name, "amount": item_amount, "price": current_price, "offers": '', "usual_price":'', "discount": '', "link":item_link}
		usual_price = item.find("span", attrs={"style":"text-decoration:line-through;"})
		discount = '0'
		if usual_price:
			usual_price = usual_price.get_text()
			usual_price_num = float(usual_price[1:])
			current_price_num = float(current_price[1:])
			discount = f"{int(100*(usual_price_num - current_price_num) / usual_price_num)}%"
			current_item["discount"] = discount
			current_item["usual_price"] = usual_price

		else:
			offers = item.find_all('div', attrs={"class":"price_promo price_bundle"})
			offers_list = []
			if offers:
				for offer in offers:
					curr_offer = offer.get_text()
					offers_list.append(curr_offer)
				current_item["offers"] = offers_list

		unavailable = item.find("div", attrs={"class":"out-of-stock"})
		if unavailable:
			current_item["name"] = f'(OUT OF STOCK) {item_name}'

		items_list.append(current_item)
	return items_list
		

		
