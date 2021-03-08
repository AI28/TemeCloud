from copy import deepcopy

class Book:

    def __init__(self, title, author, publishing_year, genre):
        self.title = title
        self.author = None
        self.author = deepcopy(author)
        self.publishing_year = publishing_year
        self.genre = genre
