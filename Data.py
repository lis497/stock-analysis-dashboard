import pandas as pd
import numpy as np
class Data:
	#class attribute for all class
	RISK_FREE_RATE = 0.04
	START_DATE = '2025-05-01'
	END_DATE = '2026-05-01'
	DEFAULT_COLUMN = ['SPY','AAPL', 'GOOGL','NVDA','AMD']
	
	def __init__(self, path: str):
		# add a _ before attribute so you don't mistakenly edit it
		# for local variables, call anything you like but not _
		self._df = pd.read_csv(path, index_col = 'date',parse_dates = True)
		

	@property #this df is a property of Data so you can remove (), all self... is property
	def df(self):
		return self._df
	@property
	def columns(self):
		return self._df.columns

	# in this case use default columns=None which is self.columns
	# None or "hello" = "hello"
	# or return the first truthy
	# and return the first falsy
	def get_stock_price(self, start_date=None, end_date=None, columns=None):
		return self._df.loc[start_date or self.START_DATE: end_date or END_DATE, columns or self.columns]


	def get_daily_return(self, start_date=None, end_date=None, columns=None):
		cls_ = type(self)
		return self._df.loc[start_date or self.START_DATE : end_date or cls_.END_DATE, columns or self.columns].pct_change().dropna()

	def get_cumulative_return(self, start_date=None, end_date=None, columns=None):
		return (1 + self.get_daily_return(start_date=start_date, end_date=end_date, columns=columns)).cumprod()

	def sharpe_ratio(self, start_date=None, end_date=None,columns=None):
		temp = self.get_daily_return(start_date=start_date, end_date=end_date,columns=columns)
		return (temp.mean() * 252 - self.RISK_FREE_RATE ) / (temp.std() * np.sqrt(252))

	def sortino_ratio(self, start_date=None, end_date=None,columns=None):
		daily_rf = self.RISK_FREE_RATE / 252
		temp = self.get_daily_return(start_date=start_date, end_date=end_date,columns=columns)
		downside_returns = temp[temp < daily_rf]
		downside_deviation = downside_returns.std() * np.sqrt(252)
		return (temp.mean() * 252 - self.RISK_FREE_RATE) / downside_deviation

	def get_beta(self, start_date='2025-05-01', end_date='2026-05-01'):
		selected = self._df.columns
		beta_daily_return = self._df.loc[start_date:end_date].pct_change().dropna()
		temp = []
		market_variance = beta_daily_return['SPY'].var()
		
		for col in self._df.columns:
			temp.append(beta_daily_return[col].cov(beta_daily_return['SPY']) / market_variance)
		# covariance = beta_daily_return[selected].cov(beta_daily_return['SPY'])
		
		df = pd.DataFrame(data=temp, index=self._df.columns)
		#print(df)
		
		return df

	def get_portfolio(self, start_date=START_DATE, end_date=END_DATE, columns=DEFAULT_COLUMN, shares=None):
		
		df0 = self.get_stock_price(start_date=start_date,end_date=end_date,columns=columns)
		if shares is None:
			shares = np.ones(len(columns))
		investment = df0.head(1).T.reset_index().iloc[:,1] * shares
		total = round(sum(investment),2)

		profit = df0.tail(1).T.reset_index().iloc[:,1] * shares
		total2 = round(sum(profit), 2)
		change = ((profit - investment) / investment * 100).round(2).astype(str) + "%"
		
		return round(investment,2), total, total2, profit, change







if __name__ == "__main__":
	print(__name__)
	test = Data("./resources/tech10_2.csv")
	# print(test.get_daily_return())
	# print(test.get_cumulative_return())
	# print(test.sharpe_ratio())
	# print(test.sortino_ratio())
	#print(test.get_beta())

	print(test.df) 
	# print(df.info)
	# print(df.shape)
	# print(df.get_columns())
	




