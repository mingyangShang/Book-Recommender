# Author liuhaozhen
# -*- coding: utf-8 -*-
import csv;
import math;
from operator import itemgetter;

def ReadData(book_user,user_book,user_sim):
	print "ReadData";
	# 读取book_user文件
	with open("../Item_Based algorithm/Item_Based_CF/book_user.csv") as f:
		reader=csv.reader(f);
		for row in reader:
			if book_user.has_key(row[0])==False:
				book_user[row[0]]=[];
			book_user[row[0]].append(row[1]);

	# 读取user_book文件
	with open("../Item_Based algorithm/Item_Based_CF/user_book.csv") as f:
		reader=csv.reader(f);
		for row in reader:
			if user_book.has_key(row[0])==False:
				user_book[row[0]]=[];
			user_book[row[0]].append(row[1]);

	# 读取user_sim文件
	with open("./User_Based_CF/user_sim.csv") as f:
		reader=csv.reader(f);
		for row in reader:
			if user_sim.has_key(row[0])==False:
				user_sim[row[0]]={};
			user_sim[row[0]][row[1]]=float(row[2]);
	return book_user,user_book,user_sim;

def GetRecommendation(user,N,user_sim,rank,K,book_user,user_book):
	# 针对每一个用户都挑选前K个最相似的.
	all_recommend={};
	K_list=[];
	temp_list=sorted(user_sim[user].items(), key=itemgetter(1),reverse = True)[0:K];
	for item in temp_list:
		K_list.append(item[0]);

	# 得到K个用户的阅读书目
	books_K=[];
	for user_k in K_list:
		books_K.extend(user_book[user_k]);

	# 计算user与book之间的关系
	for book in books_K:
		user_int_list=list(set(K_list).intersection(set(book_user[book])));
		similarity=0.0;
		for user_int in user_int_list:
			similarity+=user_sim[user][user_int];
		all_recommend[book]=similarity;
	top_list=sorted(all_recommend.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)[:N];
	for item in top_list:
		rank.append(item[0]);
	return rank;

def Precision(book_user,user_book,user_sim):
	# 选取10位用户,对每一位用户都随意选择一本书籍,根据该书籍生成推荐列表,判断推荐列表里的书籍和自己选购书籍的重合数
	user_number=10;# 用户数
	K=5;# 与user最相近的5个用户
	N=5;# 推荐书本数
	hit=0;# 命中数
	all_N=0;# 所有推荐书本数
	users=user_book.keys()[:user_number];
	for user in users:
		rank=[];
		rank=GetRecommendation(user,N,user_sim,rank,K,book_user,user_book);
		hit+=len(list(set(rank).intersection(set(user_book[user]))));
		all_N+=N;
	print hit;
	print all_N;
	print hit/(1.0*all_N);

def main():
	book_user={};# 书籍用户映射
	user_book={}# 用户书籍映射
	user_sim={};# 书籍相似度映射

	book_user,user_book,user_sim=ReadData(book_user,user_book,user_sim);
	Precision(book_user,user_book,user_sim);

if __name__ == '__main__':
	main();