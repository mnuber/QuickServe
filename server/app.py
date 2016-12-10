from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash, send_from_directory
from contextlib import closing
from datetime import timedelta
import sqlite3 as sqlite
import csv, time, datetime, os, uuid, random, json, haversine
from flask.ext.jsonpify import jsonify
from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__)

config = {}

with open("config.ini") as config_file:
    for pair in config_file:
        (key, value) = pair.split("=")
        config[key.strip()] = value.strip()

app.config.update(
    DATABASE = config['DATABASE'],
    DEBUG = config['DEBUG'],
    SECRET_KEY = config['SECRET_KEY'],
    USERNAME = config['USERNAME'],
    PASSWORD = config['PASSWORD'],
    SESSION_COOKIE_HTTPONLY = config['SESSION_COOKIE_HTTPONLY'],
    
)

def connect_db():
    return sqlite.connect('data.db')

def log(suggestion):
    with closing(connect_db()) as db:
        db.text_factory = str
        db.cursor().execute("insert into suggestions values (?,?,?,?,?,?)", [None, suggestion['OrgName'], suggestion['Location'], suggestion['Phone'], suggestion['Email'],suggestion['Description']])
        db.commit()

def get_services(filter_dict):
    pass

def get_entries():
    rows = []
    with closing(connect_db()) as db:
        # db.text_factory = str
        
        curs = db.cursor().execute("select * from organizations order by name")
        table = []
        for rows in curs:
            table.append(rows)
    return table


def update_org(org_dict):
    with closing(connect_db()) as db:
        try:
            curs = db.cursor().execute("""update organizations 
                set
                name  = ?,
                address1  = ?,
                address2  = ?,
                city  = ?,
                state  = ?,
                zip  = ?,
                county  = ?,
                phone  = ?,
                fax  = ?,
                tty  = ?,
                toll_free  = ?,
                hotline  = ?,
                email  = ?,
                website  = ?,
                fb_name  = ?,
                fb_url  = ?,
                twitter  = ?,
                lat  = ?,
                lng = ? 
                where
                id = ?
        """, [
            org_dict['orgname'],
            org_dict['address1'],
            org_dict['address2'],
            org_dict['city'],
            org_dict['state'],
            org_dict['zip'],
            org_dict['county'],
            org_dict['tel'],
            org_dict['fax'],
            org_dict['tty'],
            org_dict['toll-free'],
            org_dict['hotline'],
            org_dict['email'],
            org_dict['website'],
            org_dict['fb_name'],
            org_dict['fb_url'],
            org_dict['twitter'],
            org_dict['lat'],
            org_dict['lng'],
            org_dict['id']])
            print 'commit'
            db.commit()
        except Exception as e:
            print e            


def add_org(org_dict):
    with closing(connect_db()) as db:
        try:
            curs = db.cursor().execute("""insert into organizations values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, [
            None,
            org_dict['orgname'],
            org_dict['address1'],
            org_dict['address2'],
            org_dict['city'],
            org_dict['state'],
            org_dict['zip'],
            org_dict['county'],
            org_dict['tel'],
            org_dict['fax'],
            org_dict['tty'],
            org_dict['toll-free'],
            org_dict['hotline'],
            org_dict['email'],
            org_dict['website'],
            org_dict['fb_name'],
            org_dict['fb_url'],
            org_dict['twitter'],
            org_dict['lat'],
            org_dict['lng']])
            print 'commit'
            db.commit()
        except Exception as e:
            print e


def delete_org(id):
    with closing(connect_db()) as db:
        print id
        try:
            curs = db.cursor().execute("""delete from organizations where
                id = ?
        """, [id,])
            
            db.commit()
        except Exception as e:
            print e

def get_entries():
    rows = []
    with closing(connect_db()) as db:
        # db. = ?_factory = str
        
        curs = db.cursor().execute("select * from organizations order by name")
        table = []
        for rows in curs:
            table.append(rows)
    return table

    
# main entry point into the app
# replace the return with render_template and the main entry point 
@app.route("/", methods = ['GET'])
def main_entry():
    return render_template('index.html')

# #renders a map
# @app.route("/map", methods = ['POST'])
# def map():
#     return request.form['userFilters']

@app.route("/", methods = ['POST'])
def entrance():
    return render_template("index.html") 

# @app.route("/lists", methods = ['POST'])
# def lists():
#     return jsonify(list = get_entries())

@app.route("/suggests", methods = ['POST', 'GET'])
def suggests():
    if request.method == 'GET':
        return render_template('suggests.html')
    else:
        log(request.form)
        return "Logged?"


# takes in a filters json object
# {
#  gender : "Male",
#  age : "Turn",
#  veteran : "False",
#  homeless : "False",
#  orientation : "Bisexaul"   
# }
@app.route("/api/v1/profile", methods = ['POST'])
def profile():
    content = json.loads(request.get_json())
    filters = content['filters']
    return ""



@app.route("/profile", methods = ['GET'])
def profile_view():
    
    return render_template("profile.html")




# takes in a location json object
# {
#  long: 135.11231,
#  lat : -99.0432432  
# }
@app.route("/api/v1/map", methods = ['POST'])
def map():
    content = json.loads(request.get_json())
    map = content['filters']
    return ""


# returns all services with filter by type
@app.route("/api/v1/lists", methods = ['GET'])
def lists():
    return jsonify(get_entries())


# takes in form input as a json object
# {
#    orgname,
#    location,
#    phone,
#    email,
#    desc
# }
@app.route("/api/v1/suggest", methods = ['POST'])
def suggest():
    content = json.loads(request.get_json())
    suggestion = content['suggestion']
    return ""


# takes in form input as a json object
# {
#    nanne,
#    location,
#    desc
# }
@app.route("/api/v1/report", methods = ['POST'])
def report():
    content = json.loads(request.get_json())
    report = content['report']
    return ""






@app.route("/admin", methods = ['GET'])
def admin():
    return render_template('admin.html')


@app.route("/orgs", methods = ['GET','POST'])
def orgs():
    return render_template('orgs.html', orgs = get_entries())



def get_entry(id):
    with closing(connect_db()) as db:
        # db.text_factory = str
        
        curs = db.cursor().execute("select * from organizations where id = ?", [id,])
        
        table = [x for x in curs]
    return table

@app.route("/edit/<id>", methods = ['GET','POST'])
def edit(id):
    if request.method == 'POST':
        print request.form['id']
        
        update_org(request.form)
        
        # print len (request.form.keys())
        # for i in request.form.keys():
        #     print i
        # return ""
        return render_template('orgs.html',orgs = get_entries())

    else:
        return render_template('edit.html', entry = get_entry(id))



@app.route("/delete/<id>", methods = ['GET'])
def delete(id):
    delete_org(id)
    return render_template('orgs.html', orgs = get_entries())



@app.route("/add", methods = ['POST','GET'])
def add():
    if request.method == 'POST':
        add_org(request.form)
        return render_template('orgs.html', orgs = get_entries())
    else:
        return render_template('add.html')


@app.route("/list", methods = ['get'])
def search():
    return render_template('list.html', list = get_entries())

@app.route("/search", methods = ['get'])
def list():
    return render_template('search.html', list = get_entries())




@app.route("/notifications", methods = ['POST'])
def notifications():
    return "notifications"

@app.route("/map", methods = ['GET'])
def maps():
    return render_template('map.html')


if __name__ == "__main__":
    app.run(port=80)

