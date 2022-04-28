from flask import Flask, render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
import psycopg2

hostname = 'localhost'
database = 'sweetshop'
username = 'postgres'
pwd = 'postgres'
port_id = 5432


def query_products(storeid):
    """ query products based on storeid
        See console for printed info
    """
    conn = None
    try:
        conn = psycopg2.connect(host = hostname,
        dbname = database,
        user= username,
        password = pwd,
        port = port_id)

        cur = conn.cursor()

        sql = f"SELECT productid, name, foodtype, price, description FROM Products WHERE storeid = {storeid}"
        cur.execute(sql)
        products = cur.fetchall()
        # print("---The Requested Store Menu Is---\n")
        # for row in products:
        #     print(row)
        cur.close()
        return products
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def insert_user(userid,name,password,email):
    """ Inserts user into DB, if it does not already exist.
        Check console to see the SQL statement sent.
        Return Type: Boolean. IF TRUE: Success, do nothing | IF FALSE: Error, do nothing, we assume address exists if error.
    """
    conn = None
    try:
        conn = psycopg2.connect(host = hostname,
        dbname = database,
        user= username,
        password = pwd,
        port = port_id)

        cur = conn.cursor()
        print()
        sql = f"INSERT INTO Users(userid,paymentid,name,pass,email) VALUES('{userid}',NULL,'{name}', '{password}','{email}')"
        print("Insert user statement:\t" + sql)
        cur.execute(sql)
        #Commits official changes to DB SweetTooth
        conn.commit()
        #Close Connection
        cur.close()
        return True; #SUCCESS
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return False; #Exists, or worse...
    finally:
        if conn is not None:
            conn.close()

def top_stores():
    """ Returns tuples of top stores, by money earned in orders.
        Check console for log of info.
        Return Type: List of Tuples.
        Tuple format: (STORENAME, TOTALREVENUE)
    """

    conn = None
    stores = None
    try:
        conn = psycopg2.connect(host = hostname,
        dbname = database,
        user= username,
        password = pwd,
        port = port_id)

        cur = conn.cursor()
        sql = "SELECT stores.name, sum(totalcost) as totalrevenue FROM Stores JOIN (SELECT products.productid, products.storeid, totalcost FROM Products JOIN Orders on products.productid = orders.productid)tb ON stores.storeid = tb.storeid GROUP by stores.name ORDER BY totalrevenue DESC"
        print("Top stores statement:\t" + sql)
        cur.execute(sql)
        stores = cur.fetchall()
        print("Output for the SQL statement:\n")
        for row in stores:
          print(row)
        #Close Connection
        cur.close()
        return stores
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return None
    finally:
        if conn is not None:
            conn.close()

def query_payment(paymentid):
    """ query payments based on paymentid
        See console for printed info
    """
    conn = None
    try:
        conn = psycopg2.connect(host = hostname,
        dbname = database,
        user= username,
        password = pwd,
        port = port_id)

        cur = conn.cursor()

        sql = f"SELECT * FROM Payments WHERE paymentid = {paymentid}"
        cur.execute(sql)
        payments = cur.fetchall()
        # print("---The Requested Store Menu Is---\n")
        # for row in products:
        #     print(row)
        cur.close()
        return payments
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def get_total(userid):
    """ query payments based on paymentid
        See console for printed info
    """
    conn = None
    try:
        conn = psycopg2.connect(host = hostname,
        dbname = database,
        user= username,
        password = pwd,
        port = port_id)

        cur = conn.cursor()

        sql = f"SELECT sum(totalcost) FROM orders WHERE userid = {userid}"
        cur.execute(sql)
        payments = cur.fetchall()
        # print("---The Requested Store Menu Is---\n")
        # for row in products:
        #     print(row)
        cur.close()
        return payments
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def query_user(userid):
    """ query payments based on paymentid
        See console for printed info
    """
    conn = None
    try:
        conn = psycopg2.connect(host = hostname,
        dbname = database,
        user= username,
        password = pwd,
        port = port_id)

        cur = conn.cursor()

        sql = f"SELECT * FROM users WHERE userid = {userid}"
        cur.execute(sql)
        users = cur.fetchall()
        # print("---The Requested Store Menu Is---\n")
        # for row in products:
        #     print(row)
        cur.close()
        return users
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def top_users():
    """ Returns tuples of top users, by money spent.
        Check console for log of info.
        Return Type: List of Tuples.
        Tuple format: (NAME, EMAIL, TOTALSPENT)
    """

    conn = None
    users = None
    try:
        conn = psycopg2.connect(host = hostname,
        dbname = database,
        user= username,
        password = pwd,
        port = port_id)

        cur = conn.cursor()
        sql = "SELECT users.name, email, sum(totalcost) as totalspent FROM Users JOIN Orders ON users.userid = orders.userid GROUP by users.name, users.email ORDER BY totalspent DESC"
        print("Top customers statement:\t" + sql)
        cur.execute(sql)
        users = cur.fetchall()
        print("Output for the SQL statement:\n")
        for row in users:
          print(row)
        #Close Connection
        cur.close()
        return users
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return None
    finally:
        if conn is not None:
            conn.close()

def login_attempt(user, password):
    """ query parts from the parts table """
    conn = None
    try:
        conn = psycopg2.connect(host = hostname,
        dbname = database,
        user= username,
        password = pwd,
        port = port_id)

        cur = conn.cursor()
        sql = f"SELECT * FROM users WHERE userid = '{user}' AND pass = '{password}'"
        cur.execute(sql, (user, password))

        # fetchall function gets all the records for the query
        # this will return a list of tuples like this [(0,1,2)], every set of () is an individual record
        rows = cur.fetchall()
        print("The number of users: ", cur.rowcount)
        count = cur.rowcount
        for row in rows:
            print(row)
        cur.close()
        return count #Count of 1 means the user input is a match in the DB, 0 means it's not.
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def query_order(userid):
    """ query orders based on orderid
        We could also do this based off userid instead... might be better.
    """
    conn = None
    try:
        conn = psycopg2.connect(host = hostname,
        dbname = database,
        user= username,
        password = pwd,
        port = port_id)

        cur = conn.cursor()

        sql = f"SELECT * FROM orders WHERE userid = '{userid}'"
        cur.execute(sql)
        rows = cur.fetchall()
        # print("---The Requested Order Is---\n")
        # for row in rows:
        #     print(row)
        cur.close()
        return rows
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        print("doodooo query shit not working")
    finally:
        if conn is not None:
            conn.close()

def insert_address(street, city, state, zipcode):
    """ Inserts address into DB, if it does not already exist.
        Check console to see the SQL statement sent.
        Return Type: Boolean. IF TRUE: Success, do nothing | IF FALSE: Error, do nothing, we assume address exists if error.
    """
    conn = None
    try:
        conn = psycopg2.connect(host = hostname,
        dbname = database,
        user= username,
        password = pwd,
        port = port_id)

        cur = conn.cursor()
        print()
        sql = f"INSERT INTO addresses(street,city,state,zipcode) VALUES ('{street}','{city}','{state}','{zipcode}')"
        print("Insert address statement:\t" + sql)
        cur.execute(sql)
        #Commits official changes to DB SweetTooth
        conn.commit()
        #Close Connection
        cur.close()
        return True; #SUCCESS
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        print("Possible Address Already Exists")
        return False; #Exists, or worse...
    finally:
        if conn is not None:
            conn.close()

def insert_order(userid, productid, quantity, totalcost, street, city):
    """ Inserts order into DB.
        NOTE: address pk(street,city) has to be existent in DB. To get around this use insert_addresses() first.
        NOTE: No need to add orderid. The DB was made to use orderid as a serial number, so it iterates when new orders are added.
        Check console for log of info.
        Return Type: Boolean. IF TRUE: Success, order-success.html(if we make one) or do nothing | IF FALSE: Error, give user something-wrong.html.
    """

    conn = None
    try:
        conn = psycopg2.connect(host = hostname,
        dbname = database,
        user= username,
        password = pwd,
        port = port_id)

        cur = conn.cursor()
        sql = f"INSERT INTO orders(userid, productid, quantity, totalcost, street, city) VALUES ('{userid}',{productid},{quantity},{totalcost},'{street}','{city}')"
        print("Insert order statement:\t" + sql)
        cur.execute(sql)
        #Commits official changes to DB SweetTooth
        conn.commit()
        #Close Connection
        cur.close()
        return True; #SUCCESS
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return False; #FAILURE
    finally:
        if conn is not None:
            conn.close()

def insert_product(productid, storeid, name, foodtype, price, description):
    """ Inserts product into DB.
        NOTE: storeid has to be existent in DB..
        Check console for log of info.
        Return Type: Boolean. IF TRUE: Success, do nothing | IF FALSE: Error, give something-wrong.html.
    """

    conn = None
    try:
        conn = psycopg2.connect(host = hostname,
        dbname = database,
        user= username,
        password = pwd,
        port = port_id)

        cur = conn.cursor()
        sql = f"INSERT INTO products(productid, storeid, name, foodtype, price, description) VALUES ({productid},{storeid},'{name}','{foodtype}',{price},'{description}')"
        print("Insert product statement:\t" + sql)
        cur.execute(sql)
        #Commits official changes to DB SweetTooth
        conn.commit()
        #Close Connection
        cur.close()
        return True; #SUCCESS
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return False; #FAILURE
    finally:
        if conn is not None:
            conn.close()

def update_product_price(productid, new_price):
    """ UPDATES product price in DB.
        NOTE: productid must be within the DB.
        Check console for log of info.
        Return Type: Boolean. IF TRUE: Success, do nothing | IF FALSE: Error, give something-wrong.html.
    """

    conn = None
    try:
        conn = psycopg2.connect(host = hostname,
        dbname = database,
        user= username,
        password = pwd,
        port = port_id)

        cur = conn.cursor()
        sql = f"UPDATE products SET price = {new_price} WHERE productid = {productid}"
        print("Update product price statement:\t" + sql)
        cur.execute(sql)
        #Commits official changes to DB SweetTooth
        conn.commit()
        #Close Connection
        cur.close()
        return True; #SUCCESS
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return False; #FAILURE
    finally:
        if conn is not None:
            conn.close()

def delete_order(orderid):
    """ Deletes product from DB based on productid.
        Check console for log of info.
        Return Type: Boolean. IF TRUE: Success, do nothing | IF FALSE: Error, give something-wrong.html.
    """

    conn = None
    try:
        conn = psycopg2.connect(host = hostname,
        dbname = database,
        user= username,
        password = pwd,
        port = port_id)

        cur = conn.cursor()
        sql = f"DELETE FROM orders CASCADE WHERE orderid = {orderid}"
        print("Delete product statement:\t" + sql)
        cur.execute(sql)
        #Commits official changes to DB SweetTooth
        conn.commit()
        #Close Connection
        cur.close()
        return True; #SUCCESS
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return False; #FAILURE
    finally:
        if conn is not None:
            conn.close()
          

def product_price(productid):
    """ Returns float value of a price for a product, since we need this to compute for insert_order().
        Check console for log of info.
        Return Type: Float.
    """

    conn = None
    price = None
    try:
        conn = psycopg2.connect(host = hostname,
        dbname = database,
        user= username,
        password = pwd,
        port = port_id)

        cur = conn.cursor()
        sql = f"SELECT price FROM Products WHERE productid = {productid}"
        print("Product price statement:\t" + sql)
        cur.execute(sql)
        price = float(cur.fetchone()[0])
        print("Output for the SQL statement:\n")
        print("Price is : " + str(price))
        #Close Connection
        cur.close()
        return price
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return price
    finally:
        if conn is not None:
            conn.close()
