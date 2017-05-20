# Author liuhaozhen
# -*- coding: utf-8 -*-
import csv;
import math;

def ReadData(file,size):
	print "ReadData";
	data=[];
	with open(file) as f:
		reader=csv.reader(f);
		for row in reader:
			if "User-ID" in row:
				continue;
			row[1]=row[1].split('"')[1];
			row[2]=float(row[2].split('"')[1]);# 将字符变成float
			data.append(row);
			if len(data)==size:
				break;
	return data;

def GenerateMap(all_data,book_user,user_book,user_book_rating,book_avg):
	print "生成映射";
	# 遍历all_data
	for user,book,rating in all_data:
		# 生成[user,book]->rating的映射
		temp_list=[];
		temp_list.append(user);
		temp_list.append(book);
		temp_tuple=tuple(temp_list);
		user_book_rating[temp_tuple]=rating;

		# 生成book->user的映射
		if book_user.has_key(book)==False:
			book_user[book]=[];
		book_user[book].append(user);

		# 生成user->book的映射
		if user_book.has_key(user)==False:
			user_book[user]=[];
		user_book[user].append(book);

	# 计算每个book的平均分
	for book in book_user.keys():
		summary=0.0;
		for user in book_user[book]:
			temp_list=[];
			temp_list.append(user);
			temp_list.append(book);
			temp_tuple=tuple(temp_list);
			summary+=user_book_rating[temp_tuple];
		avg=summary/len(book_user[book]);
		book_avg[book]=avg;
	return book_user,user_book,user_book_rating,book_avg;

def ItemSimilarity(book_user,book_sim):
	print "Calculate Similarity";
	books=book_user.keys();
	count=0;
	for i in books:
		for j in books:
			if i==j:
				continue;
			numerator=0.0;# 分子
			denominator_1=0.0;# 分母1
			denominator_2=0.0;# 分母2
			users=list(set(book_user[i]).intersection(set(book_user[j])));# 获取同时给书籍i、j评分的用户集合
			numerator+=len(users);
			denominator_1=len(book_user[i]);
			denominator_2=len(book_user[j]);

			temp=[];
			temp.append(i);
			temp.append(j);
			result=denominator_1*denominator_2;
			if result==0:
				book_sim[tuple(temp)]=0;
			else:
				book_sim[tuple(temp)]=numerator/result;

	return book_sim;

def SaveData(book_user,user_book,user_book_rating,book_avg,book_sim):
	print "保存数据"
	# 保存book_user数据
	data=[];
	for book in book_user.keys():
		for user in book_user[book]:
			temp=[];
			temp.append(book);
			temp.append(user);
			data.append(temp);

	with open("./Item_Based_CF/book_user.csv","wb") as f:
		writer=csv.writer(f);
		for row in data:
			writer.writerow(row);

	# 保存user_book数据
	data=[];
	for user in user_book.keys():
		for book in user_book[user]:
			temp=[];
			temp.append(user);
			temp.append(book);
			data.append(temp);

	with open("./Item_Based_CF/user_book.csv","wb") as f:
		writer=csv.writer(f);
		for row in data:
			writer.writerow(row);

	# 保存book_avg数据
	data=[];
	for book in book_avg.keys():
		temp=[];
		temp.append(book);
		temp.append(book_avg[book]);
		data.append(temp);

	with open("./Item_Based_CF/book_avg.csv","wb") as f:
		writer=csv.writer(f);
		for row in data:
			writer.writerow(row);

	# 保存user_book_rating数据
	data=[];
	for key,value in user_book_rating.items():
		temp=[];
		temp.extend(list(key));
		temp.append(value);
		data.append(temp);

	with open("./Item_Based_CF/user_book_rating.csv","wb") as f:
		writer=csv.writer(f);
		for row in data:
			writer.writerow(row);

	# 保存book_sim数据
	data=[];
	for key,value in book_sim.items():
		temp=[];
		temp.extend(list(key));
		temp.append(value);
		data.append(temp);

	with open("./Item_Based_CF/book_sim.csv","wb") as f:
		writer=csv.writer(f);
		for row in data:
			writer.writerow(row);


def main():
	datasize=2000;# 数据集大小
	book_user={};# 书籍用户映射
	user_book={};# 用户书籍映射
	user_book_rating={};# 用户书籍评分映射
	book_avg={};# 书籍平均分映射
	book_sim={};# 书籍相似度映射

	file="./BX-CSV-Dump/BX-Book-Ratings_processed.csv";
	all_data=[];
	all_data=ReadData(file,datasize);
	book_user,user_book,user_book_rating,book_avg=GenerateMap(all_data,book_user,user_book,user_book_rating,book_avg);
	book_sim=ItemSimilarity(book_user,book_sim);
	SaveData(book_user,user_book,user_book_rating,book_avg,book_sim);

if __name__ == '__main__':
	main();