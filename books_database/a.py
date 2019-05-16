import pandas as pd 

def main():

	df = pd.read_csv("flipkart_com-ecommerce_sample.csv",header=0)
	print(df.shape[0])
	df = df[df["product_category_tree"].str.contains(pat="Women",case=False,regex="False")]
	print(df.shape[0])
	df.to_csv("womens.csv")

main()
