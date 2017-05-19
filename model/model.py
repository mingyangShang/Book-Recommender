class Book(object):
    def __init__(self, name, cover, isbn, author, score):
        self.name, self.cover, self.isbn, self.author, self.score = name, cover, isbn, author, score

    def __str__(self):
        return "%s" %(self.name)