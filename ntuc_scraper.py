from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time

def scrape(query):
	chrome_options = Options()
	chrome_options.add_argument('--headless')
	chrome_options.add_argument('--no-sandbox')

	url = f"https://www.fairprice.com.sg/search?query={query}&sorting=RELEVANCE"
	s = Service("C:/Users/user/.wdm/drivers/chromedriver/win32/99.0.4844.51/chromedriver.exe")

	def scrollFunction(numberOfScrolls):
		for i in range(numberOfScrolls):
			driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
			time.sleep(3)



	driver = webdriver.Chrome(service=s, options = chrome_options)
	driver.get(url)

	productElement = BeautifulSoup(driver.page_source, 'html.parser').find("span", attrs={"weight":"bold","class":"sc-1bsd7ul-1 hfShPC"})
	if not productElement:
		return f'No results found for "{query}"'

	numberOfProducts = int(productElement.get_text().split(' ')[0])
	numberOfScrolls = min(numberOfProducts // 20, 5)
	scrollFunction(numberOfScrolls)


	html = driver.page_source
	driver.quit()

	soup = BeautifulSoup(html, 'html.parser')

	items = soup.find_all("a", attrs={"class":"sc-1plwklf-3 bmUXOR"})
	items_list = []



	for item in items:
		item_link = f"https://www.fairprice.com.sg{item['href']}"
		item_name = item.find("span", attrs={"class":"sc-1bsd7ul-1 gGWxuk", "weight":"normal"}).get_text()
		item_amount = item.find("span", attrs={"class":"sc-1bsd7ul-1 LLmwF"}).get_text()
		current_price = item.find('span', class_="sc-1bsd7ul-1 gJhHzP").get_text()

		current_item = {"name": item_name, "amount": item_amount, "price": current_price, "offers": '', "usual_price":'', "discount": '', "link":item_link}
		usual_price = item.find('span', class_="sc-1bsd7ul-1 sc-1svix5t-0 gGWxuk lfBriN")
		discount = '0'
		if usual_price:
			usual_price = usual_price.get_text()
			usual_price_num = float(usual_price[1:])
			current_price_num = float(current_price[1:])
			discount = f"{int(100*(usual_price_num - current_price_num) / usual_price_num)}%"
			current_item["usual_price"] = usual_price
			current_item["discount"] = discount
		offers = item.find_all('div', class_="sc-1plwklf-16 hRbyxZ")
		offers_list = []
		if offers:
			for offer in offers:
				curr_offer = offer.get_text()
				offers_list.append(curr_offer) 
			current_item["offers"] = offers_list

		available = item.find("button", attrs={"data-testid":"SvgAddToCart", "class":"sc-1axwsmm-7 euWJQc"})
		if not available:
			current_item["name"] = f'(OUT OF STOCK) {item_name}'
		items_list.append(current_item)
	return items_list
