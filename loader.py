import json
import pandas as pd
import glob

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
		print("Length of data_wheels: ", len(self.data_wheels))
		print("Length of data_wheels[statuses]: ", len(self.data_wheels["statuses"]))
		return pd.DataFrame([x["text"] for x in self.data_wheels["statuses"]])

	def get_doors_as_pandas_dataframe(self):
		print("Length of data_doors: ", len(self.data_doors))
		print("Length of data_doors[statuses]: ", len(self.data_doors["statuses"]))
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

class wiki_Loader:
	def __init__(self, folder):
		self.folder = folder
		self.data_wheels = None
		self.data_doors = None
		self.load()
  
	def load(self):
		files_wheels = glob.glob(self.folder + '/wheels_wiki_pages/*.txt')
		files_doors = glob.glob(self.folder + '/doors_wiki_pages/*.txt')
		self.data_wheels = []
		self.data_doors = []
		for f in files_wheels:
			with open(f, 'r') as f:
				text = f.read()
				# remove duplicate \n
				for _ in range(100):
					text = text.replace('\n\n', '\n')
				self.data_wheels.append(text)
		for f in files_doors:
			with open(f, 'r') as f:
				text = f.read()
				for _ in range(100):
					text = text.replace('\n\n', '\n')
				self.data_doors.append(text)
    
	def get_wheels_as_pandas_dataframe(self):
		return pd.DataFrame(self.data_wheels)

	def get_doors_as_pandas_dataframe(self):
		return pd.DataFrame(self.data_doors)

if __name__ == "__main__":
	loader = Twitter_Loader('data/twitter')
	# print(loader.get_wheels_as_pandas_dataframe())
	# print(loader.get_doors_as_pandas_dataframe())
	print(loader.get_wheels_as_pandas_dataframe().shape)
	print(loader.get_doors_as_pandas_dataframe().shape)

	loader = Reddit_Loader('data/reddit')
	# print(loader.get_wheels_as_pandas_dataframe())
	# print(loader.get_doors_as_pandas_dataframe())
	print(loader.get_wheels_as_pandas_dataframe().shape)
	print(loader.get_doors_as_pandas_dataframe().shape)
	loader = wiki_Loader('data/wiki')
	# print(loader.get_wheels_as_pandas_dataframe())
	# print(loader.get_doors_as_pandas_dataframe())
	print(loader.get_wheels_as_pandas_dataframe().shape)
	print(loader.get_doors_as_pandas_dataframe().shape)