import pandas as pd
# import csv
from urllib import request

# with open("womens.csv") as f:
# 	reader = csv.reader(f)
# 	for _ in range(568):
# 		next(reader)

# 	# print(next(reader))
# 	for i,j in enumerate(reader):
		
# 		url = j[6].replace('"',"").lstrip("[").rstrip("]").split(",")[0]
# 		extension = os.path.splitext(url)[1]
		
# 		try:
# 			response = request.urlopen(url)

# 			with open("images/"+str(i+568)+extension,"wb") as f:
# 				f.write(response.read())
# 		except:
# 			print("problem")

# 	print("Done")


def main():
	df = pd.read_csv("womens3.csv",header=0)
	urls = list(df["image"])
	c = list(df["category 1"])

	i = 1152

	headers = {}

	headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"

	for link,j in zip(urls[1153:],c[1153:]):

		try:
			req = request.Request(url=link,headers=headers)

			response = request.urlopen(req)

			with open("images/"+j+str(i)+".jpeg","wb") as f:
				f.write(response.read())
		except:
			print("problem")

		print("product",i)

		i += 1

	print("Done")

main()