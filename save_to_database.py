from project_bstore.models import Book
import pandas as pd

def main():
    
    for book in Book.objects.all():
        book.delete()

main()
