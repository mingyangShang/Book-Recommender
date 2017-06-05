class Book(object):
    def __init__(self, name, cover, isbn, author, score, price=12, introduction="No introduction Now.",
                 year='1994', publication="HarperTorch"):
        self.name, self.cover, self.isbn, self.author, self.score = name, cover, isbn, author, score
        self.price, self.introduction = price, introduction
        self.year, self.publication = year, publication
        if self.price == None or self.price == 'None':
            self.price = 9.9
        if self.introduction == None or self.introduction == 'None':
            self.introduction = 'No introduction now.'

    def __str__(self):
        return "%s" %(self.name)

class User(object):
    def __init__(self, id, name, passwd, age, location):
        self.id, self.name, self.passwd, self.age, self.location = id, name, passwd, age, location
    def __str__(self):
        return "%s" %(self.name)
