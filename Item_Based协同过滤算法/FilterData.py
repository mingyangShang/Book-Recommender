# Author liuhaozhen
# -*- coding: utf-8 -*-
import csv;
import math;

def ReadData(book_user,user_book,FilterBooks,FilterUsers):
	# 读取book_user数据
	with open("./Item_Based_CF/book_user.csv") as f:
		reader=csv.reader(f);
		for row in reader:
			book_user[row[0]]=1;

	# 读取user_book文件
	with open("./Item_Based_CF/user_book.csv") as f:
		reader=csv.reader(f);
		for row in reader:
			user_book[row[0]]=1;


	# 读取Books数据
	with open("./BX-CSV-Dump/BX-Books_processed.csv") as f:
		reader=csv.reader(f);
		for row in reader:
			if book_user.has_key(row[0]):
				FilterBooks.append(row);

	# 读取Users数据
	with open("./BX-CSV-Dump/BX-Users_processed.csv") as f:
		reader=csv.reader(f);
		for row in reader:
			if user_book.has_key(row[0]):
				FilterUsers.append(row);

	return FilterBooks,FilterUsers;


def SaveData(FilterBooks,FilterUsers):
	# 保存Books数据
	with open("./Item_Based_CF/filterbooks.csv","wb") as f:
		writer=csv.writer(f);
		for row in FilterBooks:
			writer.writerow(row);

	# 保存Users数据
	with open("./Item_Based_CF/filterusers.csv","wb") as f:
		writer=csv.writer(f);
		for row in FilterUsers:
			writer.writerow(row);

def main():
	FilterBooks=[];
	FilterUsers=[];
	book_user={};
	user_book={};

	FilterBooks,FilterUsers=ReadData(book_user,user_book,FilterBooks,FilterUsers);
	SaveData(FilterBooks,FilterUsers);

if __name__ == '__main__':
	main();