from __future__ import print_function # In python 2.7
import sys 
from flask import Flask, render_template
from flask import request, redirect
from flask import g
import sqlite3
app = Flask(__name__)

officials = {}

@app.before_request
def before_request():
    g.db = sqlite3.connect("tnofficials.db")

@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()

@app.route("/")
def begin():
    return render_template("index.html")

@app.route('/reportofficials')
def reportofficials():
    """ Displays the index page accessible at '/'
    """
    return render_template('reportofficials.html')
@app.route('/about')
def about():
    return render_template('about.html')

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

    
    #if name in officials:
    #    officials[name] = officials[name] + int(star)
    #else:
    #    officials[name] = int(star)

    #print("Name: " + name)
    #print("Department: " + department)
    #print("County: " + county)
    #print("Date: " + date)
    #print("Rating: " + star)

    return redirect('/')

@app.route('/officials.html')
def officials():
    tamilofficials = g.db.execute("SELECT name from tamilofficials").fetchall()
    return render_template('officials.html', tamilofficials = tamilofficials)

@app.route('/details/<name>')
def details(name):
    #name = str(name[0])
 
    print(name, file=sys.stderr)
    officialname = g.db.execute("SELECT name from tamilofficials where name = ?", (name,)).fetchall()
    #return render_template('details.html', officialname = officialname)
    officialdepartment = g.db.execute("SELECT department from tamilofficials where name = ?", (name,)).fetchall()
    officialcounty = g.db.execute("SELECT county from tamilofficials where name = ?", (name,)).fetchall()
    officialrating = g.db.execute("SELECT star from tamilofficials where name = ?", (name,)).fetchall()
    officialmessage = g.db.execute("SELECT message from tamilofficials where name = ?", (name,)).fetchall()
#print(officialname)
    return render_template('details.html', officialname = officialname, officialdepartment = officialdepartment, officialcounty=officialcounty, officialrating=officialrating, officialmessage = officialmessage)
 

if __name__ == "__main__":
    app.run()