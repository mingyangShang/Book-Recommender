from flask import Flask, render_template, request, session, make_response, json

from model.model import Book, User
import utils

app = Flask(__name__)

curr_user = User("","","","","")

@app.route('/')
def index():
    most_popular_books = [Book("Book1", "https://img3.doubanio.com/lpic/s29436066.jpg", "isbn1", "author1", "1")] * 10
    # if(curr_user and curr_user.name):
    #     recommend_books = utils.recommend_books(curr_user)
    # else:
    #     recommend_books = utils.popular_books(10)
    return render_template('index.html', books=most_popular_books)
    # return render_template('index.html', books=most_popular_books)

@app.route('/books/<bookid>/')
def book_info(bookid):
    curr_book = utils.bookinfo(bookid)
    interested_books = utils.recommend_item([curr_book])
    return render_template('bookpage.html', book=Book("Book1", "https://img3.doubanio.com/lpic/s29436066.jpg", "isbn1", "author1", "1"),
                           interested_books = [Book("Book2", "https://img3.doubanio.com/lpic/s29436066.jpg", "isbn2", "author2", "2")] * 10)

@app.route('/user/<username>/')
def user_info(username):
    return render_template('userpage.html', username="starkshang", books=[Book("Book1", "https://img3.doubanio.com/lpic/s29436066.jpg", "isbn1", "author1", "1")] * 10)

@app.route('/login/')
def login():
    return render_template('login.html')

@app.route('/buy/book/<bookid>/', methods=['POST', 'GET'])
def buy(bookid):
    succeed = utils.buy_book(curr_user.id, bookid)
    if succeed:
        return json.dumps({"result": 1, "msg": "Buy Succeed!", "content": {}})
    else:
        return json.dumps({"result": -1, "error": "Buy Failed!", "content": {}})

@app.route('/search/')
def search():
    print 'search:', request.args
    if request.method == 'GET':
        search_key = request.args['search_text']
        books = utils.search(search_key)
        return render_template('search-result-page.html', books=[Book("Book1", "https://img3.doubanio.com/lpic/s29436066.jpg", "isbn1", "author1", "1")] * 10)


@app.route('/register/', methods=['POST'])
def register():
    if request.method == 'POST':
       if request.form['type'] == 'signup':
           username, userpwd = request.form['username'], request.form['password']
           if len(username) >0 and len(userpwd) > 6:
               return json.dumps({"result": 1, "msg": "Register Succeed!", "content": {"username": username}})
           else:
               return json.dumps({"result":-1, "error": "invalid username or password"})
       elif request.form['type'] == 'signin':
           username, userpwd = request.form['account'], request.form['password']
           # curr_user = utils.login(username, userpwd)
           return json.dumps({"result": 1, "msg": "Login Succeed!", "content": {"username": username}})

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404
if __name__ == '__main__':
    app.run()