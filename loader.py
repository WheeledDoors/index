import json
import pandas as pd

class Twitter_Loader:
	def __init__(self, folder):
		self.folder = folder
		self.data_wheels = None
		self.data_doors = None
		self.load()
  
	def load(self):
		with open(self.folder + '/wheels.json', 'r') as f:
			self.data_wheels = json.load(f)
		with open(self.folder + '/doors.json', 'r') as f:
			self.data_doors = json.load(f)
	
	def get_wheels_as_pandas_dataframe(self):
		return pd.DataFrame([x["text"] for x in self.data_wheels["statuses"]])

	def get_doors_as_pandas_dataframe(self):
		return pd.DataFrame([x["text"] for x in self.data_doors["statuses"]])

class Reddit_Loader:
	def __init__(self, folder):
		self.folder = folder
		self.data_wheels = None
		self.data_doors = None
		self.load()
  
	def load(self):
		self.data_wheels = pd.read_csv(self.folder + '/wheels_reddit.csv')
		self.data_doors = pd.read_csv(self.folder + '/doors_reddit.csv')
  
	def get_wheels_as_pandas_dataframe(self):
		return self.data_wheels

	def get_doors_as_pandas_dataframe(self):
		return self.data_doors

if __name__ == "__main__":
	loader = Twitter_Loader('data/twitter')
	print(loader.get_wheels_as_pandas_dataframe())
	print(loader.get_doors_as_pandas_dataframe())

	loader = Reddit_Loader('data/reddit')
	print(loader.get_wheels_as_pandas_dataframe())
	print(loader.get_doors_as_pandas_dataframe())