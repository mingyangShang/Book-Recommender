# Author liuhaozhen
# -*- coding: utf-8 -*-
import csv;
import math;
from operator import itemgetter;

def ReadData(book_user,user_book,book_sim):
	print "ReadData";
	# 读取book_user文件
	with open("./Item_Based_CF/book_user.csv") as f:
		reader=csv.reader(f);
		for row in reader:
			if book_user.has_key(row[0])==False:
				book_user[row[0]]=[];
			book_user[row[0]].append(row[1]);

	# 读取user_book文件
	with open("./Item_Based_CF/user_book.csv") as f:
		reader=csv.reader(f);
		for row in reader:
			if user_book.has_key(row[0])==False:
				user_book[row[0]]=[];
			user_book[row[0]].append(row[1]);

	# 读取book_sim文件
	with open("./Item_Based_CF/book_sim.csv") as f:
		reader=csv.reader(f);
		for row in reader:
			if book_sim.has_key(row[0])==False:
				book_sim[row[0]]={};
			book_sim[row[0]][row[1]]=float(row[2]);
	return book_user,user_book,book_sim;

def GetRecommendation(books,N,book_sim,rank):
	# 针对每一本书都挑选前N个最相似的,再在他们的组合中选前N个
	all_list=[];
	for book in books:
		if book_sim.has_key(book)==False:
			continue;
		temp_list=sorted(book_sim[book].items(), key=itemgetter(1),reverse = True)[0:N];
		all_list.extend(temp_list);
	all_list=sorted(all_list, key=lambda x:x[1])[::-1];
	top_list=all_list[:N];
	for item in top_list:
		rank.append(item[0]);
	return rank;

def Precision(book_user,user_book,book_sim):
	# 选取10位用户,对每一位用户都随意选择一本书籍,根据该书籍生成推荐列表,判断推荐列表里的书籍和自己选购书籍的重合数
	user_number=10;# 用户数
	N=5;# 推荐书本数
	hit=0;# 命中数
	all_N=0;# 所有推荐书本数

	users=user_book.keys()[:10];
	for user in users:
		books=user_book[user];
		rank=[];
		rank=GetRecommendation(books,N,book_sim,rank);
		for item in rank:
			if item in user_book[user]:
				hit+=1;
		all_N+=N;
	print hit;
	print all_N;
	print hit/(1.0*all_N);

def main():
	book_user={};# 书籍用户映射
	user_book={}# 用户书籍映射
	book_sim={};# 书籍相似度映射

	book_user,user_book,book_sim=ReadData(book_user,user_book,book_sim);
	Precision(book_user,user_book,book_sim);

if __name__ == '__main__':
	main();