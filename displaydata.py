from ntuc_scraper import scrape as NTUCscrape
from xlwt import Workbook


wb = Workbook()
def getSheet(query, ntuc_data):
	sheet1 = wb.add_sheet(query)
	sheet1.write(0, 0, "STORE")
	sheet1.write(0, 1, "ITEM")
	sheet1.write(0, 2, "AMOUNT")
	sheet1.write(0, 3, "PRICE")
	sheet1.write(0, 4, "OFFERS")
	sheet1.write(0, 5, "USUAL PRICE")
	sheet1.write(0, 6, "DISCOUNT")
	sheet1.write(0, 7, "LINK")
	cwidth = 0

	for i, item in enumerate(ntuc_data):
		sheet1.write(i+1, 0, "NTUC")
		for j, key in enumerate(item):
			sheet1.write(i+1, j+1, item[key])
			cwidth = sheet1.col(j+1).width
			if (len(item[key])*367) > cwidth:
				sheet1.col(j+1).width = len(item[key])*367
	wb.save('xlwt_result.xls')