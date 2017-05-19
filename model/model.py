class Book(object):
    def __init__(self, name, isbn, author, score):
        self.name, self.isbn, self.author, self.score = name, isbn, author, score

    def __str__(self):
        return "%s" %(self.name)