from flask import Flask, render_template

from model.model import Book

app = Flask(__name__)

@app.route('/')
def index():
    most_popular_books = [Book("Book1", "https://img3.doubanio.com/lpic/s29436066.jpg", "isbn1", "author1", "1")] * 10
    return render_template('index.html', books=most_popular_books)

@app.route('/books/<bookname>/')
def book_info(bookname):
    return render_template('bookpage.html', book=Book("Book1", "https://img3.doubanio.com/lpic/s29436066.jpg", "isbn1", "author1", "1"))

@app.route('/user/<username>/')
def user_info(username):
    return render_template('userpage.html', username="starkshang", books=[Book("Book1", "https://img3.doubanio.com/lpic/s29436066.jpg", "isbn1", "author1", "1")] * 10)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404
if __name__ == '__main__':
    app.run()