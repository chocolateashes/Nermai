#Hello.py is the python file that has the functions that render templates and push out SQL queries
from __future__ import print_function # In python 2.7
import sys 
from flask import Flask, render_template
from flask import request, redirect
from flask import g
import sqlite3

app = Flask(__name__)

#connecting to the database which includes both opening it in before_request and closing it in teardown_request
@app.before_request
def before_request():
    g.db = sqlite3.connect("tnofficials.db")

@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()

#begins the application by rendering the index.html template
@app.route("/")
def begin():
    return render_template("index.html")

#called when "reportofficials" is called in the HTML
@app.route('/reportofficials')
def reportofficials():
    return render_template('reportofficials.html')

#called when "about" is called in the HTML
@app.route('/about')
def about():
    return render_template('about.html')

#called when "report" is called in the HTML
#this is the result of submitting a form which is why the POST method is used
#pulls data drom the form and then uses an Insert statement to push into the database
@app.route('/report', methods = ['POST'])
def report():
    name = request.form['name']
    department = request.form['department']
    county = request.form['county']
    star = request.form['star']
    date = request.form['date']
    message = request.form['message']

   
    g.db.execute("INSERT INTO tamilofficials(name, department, county, star, date, message) VALUES (?,?,?,?,?,?)", [name,department,county,star,date,message])
    g.db.commit()

    return redirect('/')

#called when "officials" is called in the HTML
#populates the HTML with data from the database
#performs a SELECT query in order to retrieve all the names from the database
@app.route('/officials.html')
def officials():
    tamilofficials = g.db.execute("SELECT name from tamilofficials").fetchall()
    return render_template('officials.html', tamilofficials = tamilofficials)

#called when "toprated" is called in the HTML
#populates the HTML with data from the database
#performs a SELECT query in order to retrieve all the names from the database where the star rating is greater than 3
@app.route('/toprated.html')
def toprated():
    topofficials = g.db.execute("SELECT name from tamilofficials where star > 3").fetchall()
    return render_template('toprated.html', topofficials = topofficials)

#called when "details" is called in the HTML
#has a card pop up with the details from the database
#perfotms multiple select queries and outputs to the HTML
#takes in the name as an input in order to use in the queries
@app.route('/details/<name>')
def details(name):
    officialname = g.db.execute("SELECT name from tamilofficials where name = ?", (name,)).fetchall()
    officialdepartment = g.db.execute("SELECT department from tamilofficials where name = ?", (name,)).fetchall()
    officialcounty = g.db.execute("SELECT county from tamilofficials where name = ?", (name,)).fetchall()
    officialrating = g.db.execute("SELECT star from tamilofficials where name = ?", (name,)).fetchall()
    officialmessage = g.db.execute("SELECT message from tamilofficials where name = ?", (name,)).fetchall()
    
    return render_template('details.html', officialname = officialname, officialdepartment = officialdepartment, officialcounty=officialcounty, officialrating=officialrating, officialmessage = officialmessage)
 

if __name__ == "__main__":
    app.run()