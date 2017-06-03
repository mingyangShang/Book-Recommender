from flask import Flask, render_template, request, session, make_response, json

from model.model import Book, User
import utils

app = Flask(__name__)

curr_user = User("","","","","")

@app.route('/')
def index():
    if(curr_user and curr_user.name):
        recommend_books = utils.recommend_books(curr_user.id)
    else:
        recommend_books = utils.popular_books(12)
    return render_template('index.html', books=recommend_books)
    # return render_template('index.html', books=most_popular_books)

@app.route('/books/<bookid>/')
def book_info(bookid):
    curr_book = utils.bookinfo(bookid)
    # interested_books = utils.recommend_item([curr_book])
    return render_template('bookpage.html', book=curr_book,
                           interested_books = [Book("Book2", "https://img3.doubanio.com/lpic/s29436066.jpg", "isbn2", "author2", "2")] * 10)

@app.route('/user/<username>/')
def user_info(username):
    return render_template('userpage.html', username=curr_user.name, books=[Book("Book1", "https://img3.doubanio.com/lpic/s29436066.jpg", "isbn1", "author1", "1")] * 10)

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
    if request.method == 'GET':
        search_key = request.args['search_text']
        if "page" in request.args:
            page = request.args["page"]
        else:
            page = 1
        books = utils.search(search_key)
        if len(books) % 12 == 0:
            max_page = len(books) // 12
        else:
            max_page = len(books) // 12 + 1
        if page < max_page:
            display_books = books[(page-1)*12, page*12]
        else:
            display_books = books[(min(page, max_page)-1)*12:]
        return render_template('search-result-page.html', books=display_books)


@app.route('/register/', methods=['POST'])
def register():
    if request.method == 'POST':
       if request.form['type'] == 'signup':
           username, userpwd = request.form['username'], request.form['password']
           user = utils.register(username, userpwd, 20, 'China')
           if user and user.name:
               return json.dumps({"result": 1, "msg": "Register Succeed!", "content": {"username": username}})
           else:
               return json.dumps({"result":-1, "error": "invalid username or password"})
       elif request.form['type'] == 'signin':
           username, userpwd = request.form['account'], request.form['password']
           user = utils.login(username, userpwd)
           if user and user.name:
               curr_user = user
               login_succeed = True
           else:
               login_succeed = False

           if login_succeed:
                return json.dumps({"result": 1, "msg": "Login Succeed!", "content": {"username": username}})
           else:
               return json.dumps({"result": -1, "msg": "Username or password wrong!", "content": {}})

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404
if __name__ == '__main__':
    app.run()