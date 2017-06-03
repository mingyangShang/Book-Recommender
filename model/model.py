class Book(object):
    def __init__(self, name, cover, isbn, author, score):
        self.name, self.cover, self.isbn, self.author, self.score = name, cover, isbn, author, score

    def __str__(self):
        return "%s" %(self.name)

class User(object):
    def __init__(self, id, name, passwd, age, location):
        self.id, self.name, self.passwd, self.age, self.location = id, name, passwd, age, location
    def __str__(self):
        return "%s" %(self.name)
