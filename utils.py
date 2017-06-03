# Author liuhaozhen
# -*- coding: utf-8 -*-

import MySQLdb;
from operator import itemgetter;
from model.model import Book, User

# 根据ISBN号(book_id)查找书籍
# 根据书名(title)查找书籍
# 根据作者(author)查找书籍
# 根据ISBN号、书名、作者查找书籍
# 根据ISBN号查找所有读者
# 根据读者ID查找所有已读书籍
# 根据读者ID查找读者信息
# 根据读者ID、ISBN号推荐书籍
# 获取评分最高的若干本书籍


# 建立数据库连接
def MysqlConn():
	conn=None;
	cursor=None;
	try:
		conn=MySQLdb.connect(host="localhost",user="root",passwd="199406",db="lhz",connect_timeout=10);
		cursor=conn.cursor();
		flag=True;
	except Exception,e:
		print "Can not Connect to Mysql server";
		flag=False;
	return conn,cursor,flag;

# 根据ISBN号(book_id)查找书籍
def QueryByBookId(cursor,book_id):
	book_list=[];
	sql="select * from books where book_id='%s'" %(book_id);
	cursor.execute(sql);
	alldata=cursor.fetchall();
	for element in alldata:
		book_list.append(list(element));
	return book_list;

# 根据书名(title)查找书籍
def QueryByBookTitle(cursor,title):
	title_list=[];
	sql="select * from books where title='%s'" %(title);
	cursor.execute(sql);
	alldata=cursor.fetchall();
	for element in alldata:
		title_list.append(list(element));
	return title_list;

# 根据作者(author)查找书籍
def QueryByBookAuthor(cursor,author):
	author_list=[];
	sql="select * from books where author='%s'" %(author);
	cursor.execute(sql);
	alldata=cursor.fetchall();
	for element in alldata:
		author_list.append(list(element));
	return author_list;

# 根据ISBN号、书名、作者查找书籍
def QueryByBookInfo(cursor,book_id,title,author):
	books_list=[];
	sql="select * from books where book_id='%s' and title='%s' and author='%s'" %(book_id,title,author);
	cursor.execute(sql);
	alldata=cursor.fetchall();
	for element in alldata:
		books_list.append(list(element));
	return books_list;

# 根据ISBN号查找所有读者
def QueryUserListByBookId(cursor,book_id):
	user_list=[];
	sql="select * from users where user_id in (select user_id from book_user where book_id='%s')" %(book_id);
	cursor.execute(sql);
	alldata=cursor.fetchall();
	for element in alldata:
		user_list.append(list(element));
	return user_list;

# 根据读者ID查找所有已读书籍
def QueryBookListByUserId(cursor,user_id):
	book_list=[];
	sql="select * from books where book_id in (select book_id from user_book where user_id='%s')" %(user_id);
	cursor.execute(sql);
	alldata=cursor.fetchall();
	for element in alldata:
		book_list.append(list(element));
	return book_list;

# 根据读者ID查找读者信息
def QueryByUserId(cursor,user_id):
	user_list=[];
	sql="select * from users where user_id='%s'" %(user_id);
	cursor.execute(sql);
	alldata=cursor.fetchall();
	for element in alldata:
		user_list.append(list(element));
	return user_list;


# 根据读者ID、ISBN号推荐书籍
def QueryRecommendBook(cursor, user_id, book_id):
	all_recommend={};
	rank=[];
	recommend_list=[];
	K=5;
	N=5;
	# 针对挑选前K个最相似的
	user_K=[];
	sql="select user_j from user_sim where user_i='%s' order by similarity desc LIMIT %d" %(user_id,K);
	cursor.execute(sql);
	alldata=cursor.fetchall();
	for element in alldata:
		user_K.append(element[0]);

	# 得到K个用户的阅读书目
	books_K=[];
	for user_k in user_K:
		temp_list=QueryBookListByUserId(cursor,user_k);
		for element in temp_list:
			books_K.append(element[0]);

	for book_id in books_K:
		temp_list=QueryUserListByBookId(cursor,book_id);
		user_read_list=[];
		for element in temp_list:
			user_read_list.append(element[0]);
		user_intersection_list=list(set(user_K).intersection(set(user_read_list)));

		similarity=0.0;
		for user in user_intersection_list:
			similarity+=float(QuerySimilarity(cursor,user_id,user));
		all_recommend[book_id]=similarity;

	top_list=sorted(all_recommend.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)[:N];
	for item in top_list:
		rank.append(item[0]);
		
	for book_id in rank:
		recommend_list.extend(QueryByBookId(cursor,book_id));
	return recommend_list;

# 获取评分最高的若干本书籍
def QueryBestBooks(cursor,K):
	book_list=[];
	sql="select * from books order by avg desc limit %d" %(K);
	cursor.execute(sql);
	alldata=cursor.fetchall();
	for element in alldata:
		book_list.append(list(element));
	return book_list;

# 查询两个user之间的相似度
def QuerySimilarity(cursor,user_i,user_j):
	similarity=0.0;
	sql="select similarity from user_sim where user_i='%s' and user_j='%s'" %(user_i,user_j);
	cursor.execute(sql);
	alldata=cursor.fetchall();
	return alldata[0][0];

# 关闭数据库连接
def MysqlClose(conn,cursor,flag):
	if flag==True:
		cursor.close;
		conn.close;

def main():
	conn,cursor,flag=MysqlConn();

	# 根据ISBN号(book_id)查找书籍
	book_id="0156711427";
	book_list=[];
	book_list=QueryByBookId(cursor,book_id);
	# print book_list;

	# 根据书名(title)查找书籍
	title="Politically Correct Bedtime Stories: Modern Tales for Our Life and Times";
	title_list=[];
	title_list=QueryByBookTitle(cursor,title);
	# print title_list;

	# 根据作者(author)查找书籍
	author="Greg Egan";
	author_list=[];
	author_list=QueryByBookAuthor(cursor,author);
	# print author_list;

	# 根据ISBN号、书名、作者查找书籍
	book_id="006109398X";
	title="The Treasure Box";
	author="Orson Scott Card";
	books_list=[];
	books_list=QueryByBookInfo(cursor,book_id,title,author);
	# print books_list;

	# 根据ISBN号查找所有读者
	book_id="0440234743";
	user_read_list=[];
	user_read_list=QueryUserListByBookId(cursor, book_id);
	# print user_read_list;

	# 根据读者ID查找所有已读书籍
	user_id='277378';
	book_read_list=[];
	book_read_list=QueryBookListByUserId(cursor,user_id);
	# print book_read_list;

	# 根据读者ID查找读者信息
	user_id='10';
	user_list=[];
	user_list=QueryByUserId(cursor,user_id);
	# print user_list;

	# 根据读者ID、ISBN号推荐书籍
	user_id='10';
	book_id="0440234743";
	book_recommend_list=[];
	book_recommend_list=QueryRecommendBook(cursor,user_id,book_id);
	print book_recommend_list;

	# 获取评分最高的若干本书籍
	K=5;
	best_book_list=[];
	best_book_list=QueryBestBooks(cursor,K);
	print best_book_list;

	MysqlClose(conn,cursor,flag);

def register(name, passwd, age, location):
	"""
	:param name, passwd, age, location
	:param
	"""
	return User() # TODO parameter

def login(name, passwd):
	return User() # TODO parameter


def search(key):
	books = []
	return books

def recommend_item(books):
	"""
	:param books:list,
	:return list
	"""
	return [Book()] * 10

def recommend_books(user):
	"""
	:param user
	:return list
	"""
	return [Book()] * 10

def popular_books(k):
	"""
	:param k(int):number of books
	:return books(list)
	"""
	return [Book()] * 10


if __name__ == '__main__':
	main();
