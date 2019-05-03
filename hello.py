from flask import Flask,request, render_template, url_for, session, redirect
from flask_pymongo import PyMongo
import csv
import review_rating_cal as rc
import search_domain as sd
import basic_clean as fd
import datetime
from flask_cors import CORS 
import pymongo
from flask_restful import Resource, Api


app = Flask(__name__)
#app.config['MONGO_DBNAME'] = 'mongologin'
#app.config['MONGO_URI'] = 'mongodb://Abhijeet123:90119822@cluster0-shard-00-00-qe0x2.mongodb.net:27017,cluster0-shard-00-01-qe0x2.mongodb.net:27017,cluster0-shard-00-02-qe0x2.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true'
#mongo = PyMongo(app)


myclient =pymongo.MongoClient("mongodb://localhost:27017/")
mydb=myclient["Library"]	

api=Api(app)
CORS(app)




@app.route("/")
def hello():
	if 'username' in session:
		#users = mongo.db.registration
		users=mydb['user']
		info = users.find_one({'username':session['username']})
		if session['username'] == "admin":
			return render_template("homepage_admin.html",information=info)
		else:
			return render_template("homepage.html",information=info)
	return render_template('login.html')

@app.route("/login",methods=['POST','GET'])
def login():
	#users=mongo.db.registration
	users=mydb['user']

	if 'username' in session:
		user_login=users.find_one({'username':session['username']})

		return render_template('homepage.html',information=user_login)
	

	username1 = request.form['username']
	user_login = users.find_one({'username':username1})

	if user_login:
		if user_login['pass'] == request.form['pass']:
			
			if request.form['username'] == 'admin' and request.form['pass'] == 'admin':
				session['username'] = request.form['username']
				return render_template('homepage_admin.html',information=user_login)
			else:
				session['username'] = request.form['username']
				return render_template('homepage.html',information=user_login)
					
	return "invalid Credential"

@app.route("/logout")
def logout():
	session.clear()
	return render_template('login.html')

@app.route("/home")
def home():
	#users = mongo.db.registration
	users=mydb['user']
	info = users.find_one({'username':session['username']})
	if info:
		if session['username'] == "admin":
			return render_template("homepage_admin.html",information = info)
		else:
			return render_template("homepage.html",information = info)


@app.route("/profile")
def profile():
	#users = mongo.db.registration
	users=mydb['user']
	info = users.find_one({'username':session['username']})
	if info:
		return render_template('profile.html',information = info)

@app.route("/edit_page")
def edit_page():
	#users = mongo.db.registration
	users=mydb['user']
	info = users.find_one({'username':session['username']})
	return render_template("edit_info.html",information = info)


@app.route("/Edit_info",methods=['POST','GET']) 
def Edit_info():
	#users = mongo.db.registration
	users=mydb['user']
	users.find_one_and_update({"username":session['username']}, {"$set":{"fname":request.form['fname'] , "lname":request.form['lname'],'email':request.form['email'] ,"contact_no":request.form['contact_no'],"age":request.form['age'],"branch":request.form['branch'],"year":request.form['year'],}})

	return render_template("output_strings.html",string = "Successfully Saved")


@app.route("/registration" , methods=['POST', 'GET'])
def registration():
	if request.method == 'POST': 
		#users=mongo.db.registration
		users=mydb['user']
		if users.find_one({'username':request.form['username']}):
			#session['username'] = request.form['username']
			return "already register username! try different"
		else:
			users.insert_one({'username':request.form['username'] , 'fname':request.form['fname'] , 'lname':request.form['lname'] , 'pass':request.form['pass'] , 'contact_no':request.form['contact_no'] , 'email':request.form['email']})
			return render_template('login.html')
	return render_template('registration.html')


@app.route("/books" , methods=['POST', 'GET'])
def books():
	#users = mongo.db.books_lists
	users=mydb['books_lists']
	data=list(users.find({}))
	print(len(data))
	if len(data)!=0:
		#return "if part"
		data=list(data)
		return render_template("books.html",books_info=data)
	else:
		print("else part")	
		with open('Book_dataset.csv', 'r') as csvFile:
			#print("in with part")
			reader=csv.reader(csvFile)
			line=list(reader)
		for i in range(len(line)):
			users.insert_one({'author':line[i][0],'title':line[i][1],'branch':line[i][2],'domain':line[i][3],'publisher':line[i][4]})
	return render_template("books.html",books_info=data)
	#users.insert_one({'author':line[1][0],'title':line[1][1],'branch':line[1][2],'domain':line[1][3],'publisher':line[1][4]})
	return "error"

@app.route("/issued_books" , methods=['POST','GET'])
def issued_books():
	if request.method == 'POST':
		#users = mongo.db.books_lists
		users=mydb['books_lists']
		data = users.find_one({'title':request.form['title_name']})
		if data:
			#user=mongo.db.registration
			user=mydb['user']
			data_profile=user.find_one({'username':session['username']})

			issued_books=[request.form['title_name']]

			list_old_books=data_profile.get('issued_books')
			if list_old_books:
				if request.form['title_name'] in list_old_books:
					return render_template("output_strings.html",string = "Book already issued")
				else:
					list_old_books.append(request.form['title_name'])
					user.find_one_and_update({'username':session['username']},{"$set":{"issued_books":list_old_books}})
		#issued_books.append(data_profile.get('issued_books'))
			else:
				user.find_one_and_update({'username':session['username']},{"$set":{"issued_books":[request.form['title_name']]}})
			return render_template("output_strings.html",string = "Book issued successfully")
		else:
			return render_template("output_strings.html",string = "Not available")
	#this else is for button issued books in navigation
	else:
		#users = mongo.db.registration
		users=mydb['user']
		data = users.find_one({'username':session['username']})
		
		list_of_books=data.get("issued_books")
		if list_of_books:
			return render_template("issued_books.html",information=list_of_books)
		else:
			string='no books issued !! First issue books'
			return render_template("issued_books.html",string=string)


@app.route("/single_book",methods=['POST','GET'])
def single_book():
	#users = mongo.db.books_lists
	users=mydb['books_lists']
	#title=request.form['title_name']
	book = users.find_one({'title':request.form['title_name']})
	if book:
		return render_template("selected_book.html",information=book)
	else:
		return render_template("output_strings.html",string = "No book available")

#submit a review 
@app.route("/before_submit_review",methods=['POST','GET'])
def before_submit_review():

	book_name=request.form['book_name']
	return render_template('before_submit.html',information=book_name)


@app.route("/submit_review",methods=['POST','GET'])
def submit_review():
	if request.method == 'POST':
		#users=mongo.db.reviews
		users=mydb['reviews']
		review=request.form['review']
		book_name=request.form['book_name']

		result=rc.review_(review)

		if users.find_one({'book_name':book_name}):
			if users.find_one({'comments.username':session['username']}):
				return render_template("output_strings.html",string = "Already submitted Review")
		else:	
			users.insert_one({'book_name':request.form['book_name'],'comments':{'username':session['username'],'review':review}})
		#review_count.insert_one({"book_name":request.form['book_name'],""})
		#users = mongo.db.total_review_count
		#return "review submitted"

		#users = mongo.db.total_review_count
		users=mydb['total_review_count']
		if users.find_one({'book_name':book_name}):
			if users.find_one({'book_name':book_name,'username':session['username']}):
				#updating review function

				return render_template("output_strings.html",string = "Already submitted Review")
			else:
				if result=='pos':
					users.find_one_and_update({'book_name':book_name},{"$inc":{"positive_counter":1 , "total_count" :1}})
				else:
					users.find_one_and_update({'book_name':book_name},{"$inc":{"negative_counter":1 , "total_count" :1}})
		else:
			if result=="pos":
				users.insert_one({'book_name':book_name,'username':session['username'],'positive_counter':1,'negative_counter':0,'total_count':1})
			else:
				users.insert_one({'book_name':book_name,'username':session['username'],'positive_counter':0,'negative_counter':1,'total_count':1})
	return render_template("output_strings.html",string = "submitted Review")    	

@app.route("/add_book")
def add_book():
	#users = mongo.db.book
	return render_template("add_book_after.html")

@app.route("/add_book_after1",methods=['POST','GET'])
def add_book_after1():
	users=mydb['books_lists']
	#users = mongo.db.books_lists
	users.insert_one({'author':request.form['author_name'],'title':request.form['title_name'],'branch':request.form['branch_name'],'domain':request.form['domain_name'],'publisher':request.form['publiser_name']})
	string="Book successfully Added"
	return render_template("add_book_after.html",string=string)


@app.route("/delete_book")
def delete_book():
	#users = mongo.db.books_lists
	users=mydb['books_lists']
	data=users.find({})
	if data:
		data = list(data)
		return render_template("delete_book.html",information=data)

@app.route("/delete_book_after",methods=['POST','GET'])
def delete_book_after():
	#users = mongo.db.books_lists
	users=mydb['books_lists']
	tit = users.find_one({'title':request.form['title_name']})

	users.delete_one(tit)
	string="Book Removed"
	return render_template("delete_book.html",string=string)


@app.route("/search_book", methods=['POST','GET'])
def search_book():
	if request.method=='POST':
		users=mydb['books_lists']
		#users=mongo.db.books_lists
		title1 = []
		dict1 = {}
#here we need to put domain finder
		input_text = request.form['domain']
		result=sd.find_domain(input_text)
		#print(result)
		title1.clear()
		dict1.clear()
		print(len(title1)) 
		
		data = list(users.find({'domain':result}))
		

		for i in range(len(data)):
			dict1 = data[i]
			title1.append(dict1.get('title'))
		print(len(title1)) 
		dict2={}
		list_of_review1=[]
		reviews1=[]
		dict2.clear()
		list_of_review1.clear()
		#user=mongo.db.total_review_count
		user=mydb['total_review_count']
		#user_review=mongo.db.reviews
		user_review=mydb['reviews']
		for i in range(len(title1)):
			data_dict = user.find_one({'book_name':title1[i]})
			if data_dict:
				list_of_review1.append([title1[i],data_dict.get('positive_counter'),data_dict.get('negative_counter'),data_dict.get('total_count')])
				data_review=user_review.find_one({"book_name":title1[i]})
				reviews1.append([title1[i],data_review.get("comments")])

			else:
				list_of_review1.append([title1[i],0,0,0])	
				#dict2={'book_name':title[i],'positive':data_dict.get('positive_counter'),'negative':data_dict.get('negative_counter'),'total_review':data_dict.get('total_count')}
		return render_template("endresult.html",information=list_of_review1,info=reviews1)
			
@app.route("/contact")
def contact():
	return render_template("contact_us.html")

@app.route("/events")
def events():
	return render_template("events.html")

@app.route("/event_after",methods=['POST','GET'])
def event_after():
	list2=['next','previous','class']
	#users = mongo.db.timetable
	users=mydb['timetable']
	#users=mydb['timetable'] need to add timetable manually in mongodb
	query=request.form['query']
	filtered_token=fd.basic_cleanning(query)
	print(filtered_token)

	for i in filtered_token:
		if i in list2:		
			now=datetime.datetime.now()
			hour=now.hour
			if hour < 16 and hour > 8:

				hour=str(hour+1)
				
				#add extra zero to front if it's not there
				hour=hour+'00'
				data=users.find_one({'time':hour})
				lecture_name=str(data.get('subject'))
				return render_template("output_strings.html",string = lecture_name)
			else:
				return render_template("output_strings.html",string = "No lecture for this time")
	return "Ans is :"+response


if __name__=="__main__":
	app.secret_key = 'mysecret'
	app.run(debug=True)