import gspread
from oauth2client.service_account import ServiceAccountCredentials

from itertools import zip_longest

class Sheet:

	def __init__(self):
		scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
		creds = ServiceAccountCredentials.from_json_keyfile_name('StratRouletteKey.json', scope)
		self.client = gspread.authorize(creds)

		self.sheet = self.client.open('DP strat roulette').sheet1

	def get_table(self):
		cols = [self.sheet.col_values(i) for i in range(1,5)]
		table = [row for row in zip_longest(*cols) if len(row) == 4 and row[0]] 

		return table[1:]

if __name__ == "__main__":
	sheet = Sheet()
	print(sheet.get_table()[0])