from flask import Flask, render_template

from model.model import Book

app = Flask(__name__)

@app.route('/')
def index():
    most_popular_books = [Book("Book1", "isbn1", "author1", "1")]
    return render_template('homepage.html', books=most_popular_books)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404
if __name__ == '__main__':
    app.run()