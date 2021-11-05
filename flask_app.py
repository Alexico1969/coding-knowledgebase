from flask import Flask,redirect,url_for,render_template,request
import sqlite3
from sqlite3 import Error
from db import create_connection, create_tables, create_starter_data, get_domains, add_knowledge

app=Flask(__name__, static_url_path='/static')

create_connection(r"knowledge.db")
#create_tables()
#create_starter_data()  # run just once to get the first domains in the db
print(">> Checkpoint Alpha" )


@app.route('/',methods=['GET','POST'])
def home():
    domain_list = []
    domain_list = get_domains()
    return render_template('index.html', domain_list=domain_list)

@app.route('/new',methods=['GET','POST'])
def new():
    print("## New !")
    domain_list = []
    if request.method == "POST":
        domain = request.form.get("domain")
        topic = request.form.get("domain")
        problem = request.form.get("domain")
        solution = request.form.get("domain")
        print(domain)
        add_knowledge(domain, topic, problem, solution)
    else:
        
        domain_list = get_domains()
    
    return render_template('new.html', domain_list=domain_list)

if __name__ == '__main__':
    app.run(port=5000,debug=True)