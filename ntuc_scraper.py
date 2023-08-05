from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


def scrape(query, chromedriverpath):
	chrome_options = Options()
	chrome_options.add_argument('--headless')
	chrome_options.add_argument('--no-sandbox')
	
	url = f"https://www.fairprice.com.sg/search?query={query}&sorting=RELEVANCE"
	s = Service(chromedriverpath)


	driver = webdriver.Chrome(service=s, options = chrome_options)
	driver.get(url)

	productElement = BeautifulSoup(driver.page_source, 'html.parser').find("span", attrs={"weight": "bold", "class":"sc-1bsd7ul-1 eUIGON"})


	if not productElement:
		return f'No results found for "{query}"'

	html = driver.page_source
	driver.quit()

	soup = BeautifulSoup(html, 'html.parser')

	items = soup.find_all("a", attrs={"class":"sc-1plwklf-3 gEvWGD"})
	items_list = []



	for item in items:
		item_link = f"https://www.fairprice.com.sg{item['href']}"
		item_name = item.find("span", attrs={"class":"sc-1bsd7ul-1 eKBQTR", "weight":"normal"}).get_text()
		item_amount = item.find("span", attrs={"class":"sc-1bsd7ul-1 kBXURc"}).get_text()
		current_price = item.find('span', class_="sc-1bsd7ul-1 sc-1svix5t-1 cyZSLh ilXfia").get_text()

		current_item = {"name": item_name, "amount": item_amount, "price": current_price, "offers": '', "usual_price":'', "discount": '', "link":item_link}
		usual_price = item.find('span', class_="sc-1bsd7ul-1 sc-1svix5t-0 kRqzHi dEsYvT")
		discount = '0'
		if usual_price:
			usual_price = usual_price.get_text()
			usual_price_num = float(usual_price[1:])
			current_price_num = float(current_price[1:])
			discount = f"{int(100*(usual_price_num - current_price_num) / usual_price_num)}%"
			current_item["usual_price"] = usual_price
			current_item["discount"] = discount
		offers = item.find_all('div', class_="sc-16yemxd-0 bsriWD")
		offers_list = []
		if offers:
			for offer in offers:
				curr_offer = offer.get_text()
				offers_list.append(curr_offer) 
			current_item["offers"] = offers_list

		available = item.find("button", attrs={"data-testid":"SvgAddToCart", "class":"sc-1axwsmm-7 fUDOJI"})
		if not available:
			current_item["name"] = f'(OUT OF STOCK) {item_name}'
		items_list.append(current_item)
	return items_list
