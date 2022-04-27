from flask import Flask, render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
# from functionz import insert_user
from functionz import *

# from functionz import top_users,delete_product,update_product_price,login_attempt,query_order,insert_address,insert_order,insert_product,
# top_stores,product_price, query_products
import psycopg2

app = Flask(__name__)

# Configurations for connecting to the database using sqlalchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:postgres@localhost/sweetshop'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


@app.route('/process_login', methods =['POST'])
def processLoginSignUp():
    user_name = request.form.get('userid')
    f_name = request.form.get('fname')
    l_name = request.form.get('lname')
    e_mail= request.form.get('email')
    re_email = request.form.get('email2')
    pass_word = request.form.get('password')

    name = f_name + " " + l_name

    insert_user(user_name, name, pass_word, e_mail)


    return redirect("http://127.0.0.1:5000/")

# query_products(2)

# Route decorator tells Flask what url to use to trigger a function
@app.route('/')
def index():
    # fetches all the records in the Favquotes table and stores them in the result variable
    # result = Favquotes.query.all()
    return render_template('doodoobase.html')

@app.route('/add-products', methods=['POST'])
def addTingzToCart():
    global nameParam
    userid = request.form.get('userid')
    productid = int(request.form.get('productid'))
    quantity = int(request.form.get('quantitty'))
    totalcost = int(request.form.get('price_item'))
    street = request.form.get('userstreet')
    city = request.form.get('usercity')
    insert_order(userid, productid, quantity, totalcost, street, city)
    return redirect(url_for('prodicks'))


# These are endpoints
# What the applications will be responding with if they go to the
# /about or /quotes sections
@app.route('/about_us')
def quotes():
    return render_template('about_us.html')

@app.route('/cart')
def cart():
    return render_template('cart.html')

@app.route('/contact_us')
def contact():
    return render_template('contact_us.html')

@app.route('/login_signup')
def login():
    return render_template('login_signup.html')

@app.route('/prodicks')
def ma():
    ##### replace these with actual database call: ##############
    # itemInfo = db.getItems(storeid)

    product_list = query_products(1)
    # product_tags = ("chocolate_chip_cockies", 1234, 20) #display name, tag name, productid, price
    # itemInfo = db.getItems(storeid) # get list of all items in db
    return render_template('prodicks.html', product_list=product_list)

@app.route('/product')
def product():
    return render_template('product_page.html')

@app.route('/error')
def error():
    return render_template('sumting_wrong.html')




# cur.close()
# conn.close()
