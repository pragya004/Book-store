import pandas as pd 

def main():

	columns = ["product_name","brand","category 1","category 2","retail_price","discounted_price","image"]

	df = pd.read_csv("womens.csv",header=0)
	
	# print(df.shape[0])

	df = df[df["product_category_tree"].str.contains(pat="Clothing >> Women's Clothing",case=False,regex="False")]
	df["product_category_tree"] = df["product_category_tree"].str.replace('"',"").str.lstrip("[").str.rstrip("]")
	df["product_category_tree"] = df["product_category_tree"].str.slice(32)
	df["image"] = df["image"].str.replace('"',"").str.lstrip("[").str.rstrip("]").str.split(",").str[0]

	# # print(df["category 1"].unique())
	# # print(df["category 2"].unique())
	# # print(df["category 3"].unique())
	# # print(df["category 4"].unique())
	df["category 1"] = df["product_category_tree"].str.split(">>").str[0]
	df["category 2"] = df["product_category_tree"].str.split(">>").str[1]
	# # df["category 3"] = df["product_category_tree"].str.split(">>").str[2]
	# # df["category 4"] = df["product_category_tree"].str.split(">>").str[3]
	# # # # print(df.shape[0])

	df.fillna(method='ffill',inplace=True)
	print(pd.isna(df["discounted_price"]).sum())

	df[columns].to_csv("womens.csv")
	
main()