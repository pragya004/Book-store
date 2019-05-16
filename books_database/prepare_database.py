import pandas as pd
import requests

def get_book_url(isbn):

    url = "http://openlibrary.org/api/volumes/brief/isbn/"
    response = requests.get(url + isbn + ".json")
    data = response.json()

    try:
        if data["items"] != []:
            for item in data["items"]:
                if "itemURL" in item:
                    return item["itemURL"]
        else:
            return None
    except Exception as e:

        return None


def main():
    
    CSV_FILE = "books.csv"
    df = pd.read_csv("books.csv",header=0)
    df_filtered = df[[  "isbn", "authors", "original_publication_year",
                        "original_title", "average_rating", "image_url"]]

    df_filtered.dropna(inplace = True)
    df_filtered["publication_year"] = df_filtered["original_publication_year"].astype(int)
    df_filtered["isbn"] = df_filtered["isbn"].apply(lambda x: "0"*(10-len(x)) + x if len(x) < 10 else x)


    book_urls = []

    print("Fetching urls...")

    total_rows = df.shape[0]

    print("total books: %d"%(total_rows))

    success_count = 0
    total_count   = 0

    for isbn in df_filtered["isbn"][:1000]:
        book_url = get_book_url(isbn)
        book_urls.append(book_url)

        if book_url != None:
            success_count += 1

        total_count += 1

        print("Downloaded: %.2f%% (%d/%d) | URL got: (%d/%d)" %(total_count/total_rows, 
                                                                total_count, 
                                                                total_rows,
                                                                success_count,
                                                                total_rows ), end="\r")


    print("Download Complete")

    df_filtered["book_read_url"] = pd.Series(book_urls)

    df_filtered.to_csv("filtered_data.csv")


main()

