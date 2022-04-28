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

store_id = 0

@app.route('/process-signup', methods =['POST'])
def processSignup():
    # variables that stores information from signup page
    name = request.form.get('name')
    email = request.form.get('email')
    username = request.form.get('uname')
    password = request.form.get('password')
    insert_user(username, name, password, email)
    return redirect("signup.html") 

############ FUNCTION TO PROCESS WHETHER OR NOT LOGIN IS VALID #############
# @app.route('/process-login', methods =['POST'])
# def processLogin():
#     # variables that stores information from signup page
#     global flag, nameParam
#     username = request.form.get('userid')
#     password = request.form.get('password')
#     validateLogin = db.login(username, password)
#     if validateLogin == True:
#         flag = 1
#         nameParam = username
#         return redirect(url_for('index'))
#     else:
#         flag = 0
#         return render_template("login.html")

######## OLD LOGIN ###########
# @app.route('/process_login', methods =['POST'])
# def processLoginSignUp():
#     user_name = request.form.get('userid')
#     f_name = request.form.get('fname')
#     l_name = request.form.get('lname')
#     e_mail= request.form.get('email')
#     re_email = request.form.get('email2')
#     pass_word = request.form.get('password')

#     name = f_name + " " + l_name

#     # checks if the information entered is valid
#     if user_name == "" or f_name == "" or l_name == "" or e_mail == "" or re_email == "" or pass_word == "" or e_mail != re_email:
#         return redirect("http://127.0.0.1:5000/error")

#     insert_user(user_name, name, pass_word, e_mail)

#     return redirect("http://127.0.0.1:5000/")

# query_products(2)

# Route decorator tells Flask what url to use to trigger a function
@app.route('/')
def index():
    # fetches all the records in the Favquotes table and stores them in the result variable
    # result = Favquotes.query.all()

    return render_template('doodoobase.html')
@app.route('/store_find',methods=['POST','GET'])
def store_find():
    global store_id
    stoopidstore =int(request.form.get('storeid'))
    
    if stoopidstore != 0:
        store_id = stoopidstore

    if stoopidstore == 0:
        product_list = query_products(store_id)
    product_list = query_products(stoopidstore)
    return render_template('prodicks.html',product_list=product_list, stoopidstore=stoopidstore)

@app.route('/add-products', methods=['POST'])
def addTingzToCart():
    global nameParam
    userid = request.form.get('userid')
    productid = int(request.form.get('productid'))
    quantity = int(request.form.get('quantitty'))
    totalcost = float(request.form.get('price_item'))
    street = request.form.get('userstreet')
    city = request.form.get('usercity')

    # storeid = 1
    storeid = int(request.form.get('storeid'))
    # product_list = query_products(storeid)
    insert_order(userid, productid, quantity, totalcost, street, city) 

    return render_template('doodoobase.html')
    # return render_template("prodicks.html",storeid=storeid)

@app.route('/delete-products' , methods=['GET', 'POST'])
def removeTingsFromCart():
    orderid = int(request.form.get('orderid'))
    delete_order(orderid)
    return redirect("/cart")
    # return render_template("http://127.0.0.1:5000/cart")
# delete_product(2)

@app.route('/checkout',methods=['POST','GET'])
def ():
    userid = "bond007"
    checkout_items = query_order(userid)
    user_info = query_user(userid)
    paymentid = request.form.get('paymentid')
    payment_shit = query_payment(paymentid)
    total_cost = get_total(userid)
    #make new page that says checkout is successful
    return render_template('doodoobase.html')

# These are endpoints
# What the applications will be responding with if they go to the
# /about or /quotes sections
@app.route('/about_us')
def quotes():
    return render_template('about_us.html')

@app.route('/menu')
def menu():
    return render_template('store_menu.html')

@app.route('/cart')
def cart():
    username = "bond007"
    cart_items = query_order(username) #TESTING
    print(cart_items)
    return render_template('cart.html', cart_items=cart_items)

@app.route('/contact_us')
def contact():
    return render_template('contact_us.html')

@app.route('/login_signup')
def login():

    return render_template('login_signup.html')

@app.route('/prodicks', methods=['GET', 'POST'])
def ma():
    ##### replace these with actual database call: ##############
    # itemInfo = db.getItems(storeid)
    # storeid = int(request.form.get('storeid'))
    # product_list = query_products(storeid)
    # product_tags = ("chocolate_chip_cockies", 1234, 20) #display name, tag name, productid, price
    # itemInfo = db.getItems(storeid) # get list of all items in db
    return render_template('prodicks.html')

@app.route('/product')
def product():
    return render_template('product_page.html')

@app.route('/error')
def error():
    return render_template('sumting_wrong.html')




# cur.close()
# conn.close()
