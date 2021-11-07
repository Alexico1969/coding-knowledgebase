from flask import Flask,redirect,url_for,render_template,request, make_response
import sqlite3
from sqlite3 import Error
from db import create_connection, create_tables, create_starter_data, get_domains, get_topics, get_knowledge, get_knowledge_all
from db import add_knowledge, clear_table_knowledge, clear_table_topics, drop_tables, get_1_topic, topics_filtered, fix

app=Flask(__name__, static_url_path='/static')

create_connection(r"knowledge.db")
#drop_tables()
#create_tables()
#create_starter_data()  # run just once to get the first domains in the db
#clear_table_knowledge()  # if you want to empty table knowledge
#clear_table_topics()  # if you want to empty table topics
fix()

@app.route('/',methods=['GET','POST'])
def home():
    domain_list = []  
    domain_list = get_domains()
    topic_list = []
    problem = ""
    solution = ""
    
    if request.method == "POST":
        action = request.form["action"]
        if action == "s_topic": #als de $.ajax gebruikt is (een van de topics geklikt)
            topic = request.form["topic"]
            topic_dict = get_1_topic(topic)
            problem = topic_dict["problem"].replace("\054","<br>").replace("\012","<br>")
            solution = topic_dict["solution"].replace("\054","<br>").replace("\012","<br>")
            resp = make_response(render_template('index.html', domain_list=domain_list, topic_list=topic_list, problem=problem, solution=solution))
            resp.set_cookie('problem', problem)
            resp.set_cookie('solution',solution)
        else: #als een van de domain buttons geklikt is.
            domain = request.form["action"]
            topic_list = topics_filtered(domain)
            resp = make_response(render_template('index.html', domain_list=domain_list, topic_list=topic_list, problem=problem, solution=solution))
            
    else:
        topic_list = get_topics()
        resp = make_response(render_template('index.html', domain_list=domain_list, topic_list=topic_list, problem=problem, solution=solution))


    return resp

@app.route('/new',methods=['GET','POST'])
def new():
    domain_list = []
    if request.method == "POST":
        domain = request.form["domain"]
        topic = request.form["topic"]
        problem = request.form["problem"]
        solution = request.form["solution"]
        add_knowledge(domain, topic, problem, solution)
    else:
        
        domain_list = get_domains()
    
    return render_template('new.html', domain_list=domain_list)

@app.route('/dump',methods=['GET','POST'])
def dump():
    domain_list = []  
    domain_list = get_domains()
    topic_list = []
    topic_list = get_topics()
    knowledge_list = []
    knowledge_list = get_knowledge_all()

    if request.method == "POST":
        print("todo")
        
    return render_template('dump.html', domain_list=domain_list, topic_list=topic_list, knowledge_list=knowledge_list)

if __name__ == '__main__':
    app.run(port=5000,debug=True)