from flask import Flask
from flask import render_template, url_for, request, redirect
import sqlite3 as db
import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    # return render_template('login.html')
    
    con = db.connect('jokes.db')
    c = con.cursor()
    c.execute(
        'CREATE TABLE IF NOT EXISTS inventory (inventory_id INTEGER PRIMARY KEY AUTOINCREMENT, inventory_name TEXT, inventory_qtty INTEGER, inventory_date TEXT)')
    con.commit()
    result = c.execute('select * from inventory')
    con.commit()
    rows = result.fetchall()
    con.close()
    return render_template('products.html', rows=rows,title='Home')


@app.route('/newjokeform')
def new():
    return render_template('newjokeform.html')

@app.route('/blog')
def blog():
    status={'home':'','blog':'active'}
    return render_template('blog.html',title='Blog',status=status)

@app.route('/dataform')
def dataform():
    return render_template('dataform.html')


@app.route('/newjokedata', methods=['POST', 'GET'])
def newjoke():
    if request.method == 'POST':
        username = request.form['joke_name']
        con = db.connect('jokes.db')
        c = con.cursor()
        c.execute("insert into joke (joke_name,joke_date) values(?,?)", (username, datetime.date.today()))
        con.commit()
        con.close()
        return redirect(url_for('index'))


@app.route('/updatejokedata', methods=['POST', 'GET'])
def updatejoke():
    if request.method == 'POST':
        joke_name = request.form['joke_name']
        joke_id = request.form['joke_id']
        con = db.connect('jokes.db')
        c = con.cursor()
        c.execute("update joke set joke_name=?, joke_date=? where joke_id=?",(joke_name, datetime.date.today(), joke_id))
        con.commit()
        con.close()
        return redirect(url_for('admin'))


@app.route('/admin')
def admin():
    # return render_template('login.html')
    con = db.connect('jokes.db')
    c = con.cursor()
    c.execute(
        'CREATE TABLE IF NOT EXISTS joke (joke_id INTEGER PRIMARY KEY AUTOINCREMENT, joke_name TEXT, joke_date TEXT)')
    con.commit()
    result = c.execute('select * from joke')
    con.commit()
    rows = result.fetchall()
    con.close()
    status = {'home': 'active', 'blog': ''}
    return render_template('admin.html', rows=rows,status=status)


@app.route('/adminform', methods=['POST'])
def adminform():
    id = request.form['id']
    action=request.form['action']
    con = db.connect('jokes.db')
    c = con.cursor()

    if action=='Edit':
        result = c.execute('select * from joke where joke_id=?', (id,))
        con.commit()
        rows = result.fetchall()
        con.close()
        return render_template('editform.html', rows=rows)

    if action=='Delete':
        c.execute('delete from joke where joke_id=?', (id,))
        con.commit()
        con.close()
        return redirect(url_for('admin'))



if __name__ == '__main__':
    app.run(debug=True)
