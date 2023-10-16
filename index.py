from flask import Flask
from flask import render_template, url_for, request, redirect
import sqlite3 as db
import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/')
def index():

    con = db.connect('inventory.db')
    c = con.cursor()
    c.execute(
        'CREATE TABLE IF NOT EXISTS product (product_id INTEGER PRIMARY KEY AUTOINCREMENT, product_name TEXT, product_quantity INTEGER, product_date TEXT)')
    con.commit()
    result = c.execute('select * from product')
    con.commit()
    rows = result.fetchall()
    con.close()
    return render_template('products.html', rows=rows,title='Home')


@app.route('/newproductform')
def new():
    return render_template('newproductform.html')


@app.route('/newproductdata', methods=['POST', 'GET'])
def newproduct():
    if request.method == 'POST':
        productname = request.form['product_name']
        productquantity = request.form['product_quantity']
        con = db.connect('inventory.db')
        c = con.cursor()
        c.execute("insert into product (product_name, product_quantity, product_date) values(?,?,?)", (productname, productquantity, datetime.date.today()))
        con.commit()
        con.close()
        return redirect(url_for('index'))


@app.route('/updateproductdata', methods=['POST', 'GET'])
def updateproduct():
    if request.method == 'POST':
        product_name = request.form['product_name']
        product_quantity=request.form['product_quantity']
        product_id = request.form['product_id']
        con = db.connect('inventory.db')
        c = con.cursor()
        c.execute("update product set product_name=?, product_quantity=?, product_date=? where product_id=?",(product_name, product_quantity, datetime.date.today(), product_id))
        con.commit()
        con.close()
        return redirect(url_for('admin'))


@app.route('/admin')
def admin():
    # return render_template('login.html')
    con = db.connect('inventory.db')
    c = con.cursor()
    c.execute(
        'CREATE TABLE IF NOT EXISTS product (product_id INTEGER PRIMARY KEY AUTOINCREMENT, product_name TEXT, product_date TEXT)')
    con.commit()
    result = c.execute('select * from product')
    con.commit()
    rows = result.fetchall()
    con.close()
    return render_template('admin.html', rows=rows)


@app.route('/adminform', methods=['POST'])
def adminform():
    id = request.form['id']
    action=request.form['action']
    con = db.connect('inventory.db')
    c = con.cursor()

    if action=='Edit':
        result = c.execute('select * from product where product_id=?', (id,))
        con.commit()
        rows = result.fetchall()
        con.close()
        return render_template('editform.html', rows=rows)

    if action=='Delete':
        c.execute('delete from product where product_id=?', (id,))
        con.commit()
        con.close()
        return redirect(url_for('admin'))



if __name__ == '__main__':
    app.run(debug=True)
