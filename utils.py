# Author liuhaozhen
# -*- coding: utf-8 -*-

import MySQLdb;
import csv;
from operator import itemgetter;
from model.model import Book, User

user_sim={};
# 读取user_sim文件
with open("/Users/smy/PycharmProjects/Book-Recommender/User_Based/user_sim.csv") as f:
	reader=csv.reader(f);
	for row in reader:
		if user_sim.has_key(row[0])==False:
			user_sim[row[0]]={};
		user_sim[row[0]][row[1]]=float(row[2]);

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

# 查询两个user之间的相似度
def QuerySimilarity(cursor,user_i,user_j):
	similarity=0.0;
	sql="select similarity from user_sim where user_i='%s' and user_j='%s'" %(user_i,user_j);
	cursor.execute(sql);
	alldata=cursor.fetchall();
	return alldata[0][0];

def main():

	# print buy_book("100", "0898861411")
	# # 根据读者ID推荐书籍
	# user_id='100';
	# book_id="0440234743";
	# book_recommend_list=recommend_books(user_sim, user_id);
	# print book_recommend_list;
    #
	# # 根据ISBN号、书名、作者查找书籍
	# key="440234743";
	# books=search(key);
	# print books[0].name;
    #
	# # 获取评分最高的若干本书籍
	# books=popular_books(5);
	# print books[0].score;
    #
    #
	# # 新用户注册
	# name="lhz";
	# password="789789";
	# age="30";
	# location="bengbu";
	# user=register(name,password,age,location);
	# print user.name;
    #
	# # 用户登录
	# username = "lhz";
	# password = "789789";
	# user = login(username, password);
	# print user.id;

	print "dasd"
	print buyed_books("10")

def buy_book(userid, bookid):
	conn, flag = mysqlconn();
	cursor=conn.cursor();
	# 插入数据库
	sql = "insert into user_book (user_id, book_id) VALUES ('%s','%s')" % (userid, bookid);
	row_affected = cursor.execute(sql);
	conn.commit();
	mysqlclose(conn, flag);
	return row_affected > 0

# 建立数据库连接
def mysqlconn():
	conn=None;
	try:
		conn=MySQLdb.connect(host="localhost",user="root",passwd="password",db="lhz",connect_timeout=10);
		flag=True;
	except Exception,e:
		print "Can not Connect to Mysql server";
		flag=False;
	return conn,flag;

# 关闭数据库连接
def mysqlclose(conn,flag):
	if flag==True:
		cursor=conn.cursor();
		cursor.close;
		conn.close;

# 新用户注册
def register(name, passwd, age, location):
	"""
	:param name, passwd, age, location
	:param
	"""
	conn,flag=mysqlconn();
	# 获取users表中最大的user_id,最大值加1作为新的user的id
	sql="select max(cast(user_id AS SIGNED)) from users";
	cursor=conn.cursor();
	cursor.execute(sql);
	alldata=cursor.fetchall();
	max_id=alldata[0][0];
	user_id=str(max_id+1);
	# 插入数据库
	sql="insert into users (user_id, location, age, username, password) VALUES ('%s','%s','%s','%s','%s')" %(user_id,location,age,name,passwd);
	cursor.execute(sql);
	conn.commit();
	user=None;
	user=User(user_id,name,passwd,age,location);
	mysqlclose(conn,flag);
	return user;# 返回user对象

# 用户登录
def login(name, passwd):
	conn,flag=mysqlconn();
	sql="select * from users where username='%s' and password=%s" %(name,passwd);
	cursor=conn.cursor();
	cursor.execute(sql);
	alldata=cursor.fetchall();
	user=None;
	if len(alldata)==0:
		print "User or password wrong";
		return None
	else:
		for element in alldata:
			user=User(element[0],element[3],element[4],element[2],element[1]);
	mysqlclose(conn,flag);
	return user;# 返回user对象

# 根据读者user_name查找读者信息
def userinfo(name):
	conn,flag=mysqlconn();
	sql="select * from users where username='%s'" %(name);
	cursor=conn.cursor();
	cursor.execute(sql);
	alldata=cursor.fetchall();
	user=None;
	for element in alldata:
		user=User(element[0],element[3],element[4],element[2],element[1]);#id,name,passwd,age,location
	mysqlclose(conn,flag);
	return user;# 返回user对象

# 根据ISBN号、书名、作者查找书籍
def search(key):
	conn,flag=mysqlconn();
	sql="select * from books where book_id='%s' or title='%s' or author='%s'" %(key,key,key);
	cursor=conn.cursor();
	cursor.execute(sql);
	alldata=cursor.fetchall();
	books = [];
	for element in alldata:
		book=Book(element[1],element[5],element[0],element[2],element[8], price=element[9], introduction=element[10], year=element[3], publication=element[4]);#title,url_s,book_id,author,avg
		books.append(book);
	mysqlclose(conn,flag);
	return books;# 返回book列表

def recommend_books(sim_map, user_id):
	"""
	:param user_id,book_id
	:return list
	"""
	conn,flag=mysqlconn();
	cursor=conn.cursor();

	all_recommend={};
	rank=[];
	recommend_list=[];
	K=20;
	N=12;
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
			similarity+=sim_map[user_id][user];
		all_recommend[book_id]=similarity;

	top_list=sorted(all_recommend.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)[:N];
	for item in top_list:
		rank.append(item[0]);
		
	for book_id in rank:
		recommend_list.extend(search(book_id));
	if len(recommend_list) < 12:
		recommend_list = recommend_list + popular_books(12)
		recommend_list = recommend_list[:12]
	return recommend_list;

# 获取评分最高的若干本书籍
def popular_books(k):
	"""
	:param k(int):number of books
	:return books(list)
	"""
	conn,flag=mysqlconn();
	cursor=conn.cursor();
	sql="select * from books order by avg desc limit %d" %(k);
	cursor.execute(sql);
	alldata=cursor.fetchall();
	books = [];
	for element in alldata:
		book=Book(element[1],element[5],element[0],element[2],element[8], price=element[9], introduction=element[10], year=element[3], publication=element[4]);#title,url_s,book_id,author,avg
		books.append(book);
	mysqlclose(conn,flag);
	return books;# 返回book列表

# 根据ISBN号(book_id)查找书籍
def bookinfo(book_id):
	conn,flag=mysqlconn();
	sql="select * from books where book_id='%s'" %(book_id);
	cursor=conn.cursor();
	cursor.execute(sql);
	alldata=cursor.fetchall();
	book=None;
	for element in alldata:
		book=Book(element[1],element[5],element[0],element[2],element[8], price=element[9], introduction=element[10], year=element[3], publication=element[4]);#title,url_s,book_id,author,avg
	mysqlclose(conn,flag);
	return book;# 返回book对象

# 根据读者ID查找所有已买书籍
def buyed_books(user_id):
	conn,flag=mysqlconn();
	book_list=[];
	sql="select * from books where book_id in (select book_id from user_book where user_id='%s')" %(user_id);
	cursor=conn.cursor();
	cursor.execute(sql);
	alldata=cursor.fetchall();
	for element in alldata:
		book=Book(element[1],element[5],element[0],element[2],element[8], price=element[9], introduction=element[10], year=element[3], publication=element[4]);#title,url_s,book_id,author,avg
		book_list.append(book);
	return book_list;

if __name__ == '__main__':
	main();
	print popular_books(10)
