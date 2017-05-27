# Author liuhaozhen
# -*- coding: utf-8 -*-
import csv;

def main():

	# 对BX-Users.csv进行预处理
	data_users=[];
	with open("./BX-CSV-Dump/BX-Users.csv") as f:
		reader=csv.reader(f);
		for row in reader:
			if len(row)==1:
				string=row[0];
				data_users.append(string.split(";"));
			else:
				string="";
				for x in row:
					string=string+x;
				if "\n" in string:
					temp=string.split("\n");
					data_users.append(temp[0].split(";"));
					temp=temp[1].split(";");
					temp[0]=temp[0].strip('""');
					data_users.append(temp);
				else:
					data_users.append(string.split(";"));

	with open("./BX-CSV-Dump/BX-Users_processed.csv","wb") as f:
		writer=csv.writer(f);
		for row in data_users:
			writer.writerow(row);

	# 对BX-Books.csv进行预处理
	data_books=[];
	with open("./BX-CSV-Dump/BX-Books.csv") as f:
		reader=csv.reader(f);
		for row in reader:
			if len(row)==1:
				string=row[0];
				data_books.append(string.split(";"));
			else:
				string="";
				for x in row:
					string=string+x;
				data_books.append(string.split(";"));

	with open("./BX-CSV-Dump/BX-Books_processed.csv","wb") as f:
		writer=csv.writer(f);
		for row in data_books:
			writer.writerow(row);


	# 对BX-Book-Ratings.csv进行预处理
	data_book_ratings=[];
	with open("./BX-CSV-Dump/BX-Book-Ratings.csv") as f:
		reader=csv.reader(f);
		for row in reader:
			if len(row)==1:
				string=row[0];
				if "/" in string:
					continue;
				data_book_ratings.append(string.split(";"));
			else:
				string="";
				for x in row:
					string=string+x;
				if "/" in string:
					continue;
				data_book_ratings.append(string.split(";"));

	with open("./BX-CSV-Dump/BX-Book-Ratings_processed.csv","wb") as f:
		writer=csv.writer(f);
		for row in data_book_ratings:
			writer.writerow(row);
			

if __name__ == '__main__':
	main();