import time
import tushare as ts
import pandas as pd
import datetime, calendar
import sys

#reload(sys)
#sys.setdefaultencoding('utf-8')

class StockBasics:
	def __init__(self, df):
		self.code = df.code
		self.name = df.name
		self.industry = df.industry
		self.area = df.area
		self.pe = df.pe
		self.outstanding = df.outstanding
		self.totals = df.totals
		self.totalAssets = df.totalAssets
		self.liquidAssets = df.liquidAssets
		self.fixedAssets = df.fixedAssets
		self.reserved = df.reserved
		self.reservedPerShare = df.reservedPerShare
		self.esp = df.esp
		self.bvps = df.bvps
		self.pb = df.pb
		self.timeToMarket = df.timeToMarket
		self.undp = df.undp
		self.perundp = df.perundp
		self.rev = df.rev
		self.profit = df.profit
		self.gpr = df.gpr
		self.npr = df.npr
		self.holders = df.holders

def update_stock_base_info():
#	df = ts.get_concept_classified()
#	df.to_csv('./data/stock_concept.csv')

#	df = ts.get_industry_classified()
#	df.to_csv('./data/stock_industry.csv')

	df = ts.get_stock_basics()
	df.to_csv('./data/stock_basics.csv')
	#print df
	return df

def update_k_data():
	df = pd.read_csv('./data/stock_basics.csv')
	for i in range(len(df.index)):
		stock0 =  StockBasics(df.ix[i])
		k_data = ts.get_k_data("%06d"%stock0.code)
		k_data.to_csv("./data/%06d.csv"%stock0.code)
		#print "./data/%06d.csv"%stock0.code

def is_stock_suspended(k_data):
	k_date_len = len(k_data.index)
	last_date = k_data.ix[k_date_len-1].date
	last_datetime = datetime.datetime.strptime(last_date, "%Y-%m-%d")
	deltaDays=datetime.timedelta(days=10)
	now = datetime.datetime.now()
	if (now - last_datetime) > deltaDays:
		return True
	else:
		return False

def is_rise_stock(k_data, percent,  days):
	if len(k_data.index) < days:
		return False
	tail_data = k_data.tail(days)
	if tail_data.iloc[0].close > tail_data.iloc[-1].close:
		return False
	nums = 0.0
	for i in range(len(tail_data.index)):
		if i == 0:
			continue
		if tail_data.iloc[i].close > tail_data.iloc[i-1].close:
			nums = nums + 1
	if nums/days*100 >= percent:
		rise_percent = tail_data.iloc[-1].close/tail_data.iloc[0].close - 1
		print ("%06d %f(%f/%f)(rise:%f|%f,%f)"%(tail_data.iloc[i].code, nums/days, nums, days, rise_percent, tail_data.iloc[0].close, tail_data.iloc[-1].close))
		
		return True
	else:
		return False

def is_3xx_stock(k_data):
	if k_data.ix[0].code > 299999 and k_data.ix[0].code < 400000:
		return True
	else:
		return False

def is_small_stock(socket_base, value):
	if socket_base.totals < value:
		return True
	else:
		return False

def is_last_day_rise_stock(k_data):
	if k_data.iloc[len(k_data.index)-1].close > k_data.iloc[len(k_data.index)-1].open:
		return True
	else:
		return False

def is_volume_abnormal_stock(k_data, multiplier, days):
	if len(k_data.index) < 10:
		return False

	if days > len(k_data.index):	
		days = len(k_data.index)

	tail_data = k_data.tail(days)

	for i in range(days-1):
#		print ("-----")
#		print (tail_data.iloc[i].volume)
#		print (tail_data.iloc[i+1].volume)
		if (tail_data.iloc[i].volume*multiplier < tail_data.iloc[i+1].volume):
			return True

	return False

def is_new_stock(k_data, days):
	data_len = len(k_data.index)
	if data_len <= days and data_len > 0:
		print (data_len)
		print (k_data)
		return True
	return False
		

def stock_with_concept(concept):
	df = pd.read_csv('./data/stock_concept.csv')
	slist = []
	for i in range(len(df.index)):
		if df.iloc[i].c_name == concept:
			slist.append(df.iloc[i].code)
			#print ("%06d"%df.iloc[i].code)
	return slist

def update_data():
	update_stock_base_info()
	update_k_data()

def choose_stocks():
	df = pd.read_csv('./data/stock_basics.csv')
	for i in df.index:
		stock0 =  StockBasics(df.ix[i])
		k_data = pd.read_csv("./data/%06d.csv"%stock0.code)
		#is_new_stock(k_data, 5)
		#if not is_new_stock(k_data, 5):
		#	continue
		if not is_volume_abnormal_stock(k_data, 2, 2):
			continue
		is_rise_stock(k_data, 65, 20)		

def find_stock_with_newstock():
	slist_tmp = stock_with_concept("次新股")
	slist = []
	for code in slist_tmp:
		k_data = pd.read_csv("./data/%06d.csv"%code)
#		for 

def find_stock_with_volume():
	df = pd.read_csv('./data/stock_basics.csv')
	for i in df.index:
		stock0 =  StockBasics(df.ix[i])
		k_data = pd.read_csv("./data/%06d.csv"%stock0.code)
		if (is_volume_abnormal_stock(k_data, 10, 20)):
			print("%06d"%stock0.code)
		
	

def red_green_array(code):
	str = ""
	k_data = pd.read_csv("./data/%06d.csv"%code)
	for i in range(len(k_data.index)):
		if k_data.iloc[i].close >= k_data.iloc[i].open:
			str = str + '1'
		else:
			str = str + '0'	

#	print (str)
	return str

def find_stock_with_rga(rga):
	df = pd.read_csv('./data/stock_basics.csv')
	for i in df.index:
		stock0 = StockBasics(df.ix[i])
		k_data = pd.read_csv("./data/%06d.csv"%stock0.code)
		if len(k_data.index) > 66:
			continue
		str = red_green_array(stock0.code)
		if rga in str:
			print ("%06d"%stock0.code)
		
	
def debug():
	find_stock_with_rga("011101010010010001010001111100011100001011100111101010000111")

def start():
#	print (slist)
	print("start...")
#	update_data()
	find_stock_with_rga("1111111000")
#	debug()
#	find_stock_with_volume()

start()
#debug()
