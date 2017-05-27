# Author liuhaozhen
# -*- coding: utf-8 -*-
import csv;
import math;

def ReadData(user_book,book_user):
	print "ReadData";
	# 读取user_book文件
	with open("../Item_Based algorithm/Item_Based_CF/user_book.csv") as f:
		reader=csv.reader(f);
		for row in reader:
			if user_book.has_key(row[0])==False:
				user_book[row[0]]=[];
			user_book[row[0]].append(row[1]);

	# 读取book_user文件
	with open("../Item_Based algorithm/Item_Based_CF/book_user.csv") as f:
		reader=csv.reader(f);
		for row in reader:
			if book_user.has_key(row[0])==False:
				book_user[row[0]]=[];
			book_user[row[0]].append(row[1]);
	return user_book,book_user;

def UserSimilarity(user_book,book_user,user_sim):
	print "Calculate Similarity";
	users=user_book.keys();
	for i in users:
		for j in users:
			if i==j:
				continue;
			books=list(set(user_book[i]).intersection(set(user_book[j])));#
			# numerator=len(books);# 分子
			numerator=0.0;
			for book in books:
				numerator+=1.0/(1+math.log(len(book_user[book])));
			# if numerator==0:
			# 	continue;
			denominator_1=len(user_book[i]);# 分母1
			denominator_2=len(user_book[j]);# 分母2

			temp=[];
			temp.append(i);
			temp.append(j);
			result=math.sqrt(denominator_1*denominator_2);
			if result==0:
				user_sim[tuple(temp)]=0;
			else:
				user_sim[tuple(temp)]=numerator*1.0/result;
	return user_sim;

def SaveData(user_sim):
	print "save data"
	# 保存book_sim数据
	data=[];
	for key,value in user_sim.items():
		temp=[];
		temp.extend(list(key));
		temp.append(value);
		data.append(temp);

	with open("./User_Based_CF/user_sim.csv","wb") as f:
		writer=csv.writer(f);
		for row in data:
			writer.writerow(row);


def main():
	user_book={};# 用户书籍映射
	user_sim={};# 书籍相似度映射
	book_user={};# 书籍用户映射

	user_book,book_user=ReadData(user_book,book_user);
	user_sim=UserSimilarity(user_book,book_user,user_sim);
	SaveData(user_sim);

if __name__ == '__main__':
	main();