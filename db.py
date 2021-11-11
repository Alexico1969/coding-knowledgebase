import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print("** SQLite DB active, version:",sqlite3.version)
    except Error as e:
        print("** ERROR **", e)
    finally:
        if conn:
            conn.close()

def connect_to_db(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print("** Connection established")
        return conn
    except Error as e:
        print(e)

    return conn

def drop_tables():
    database = "knowledge.db"
    conn = connect_to_db(database)

    c = conn.cursor()

    query = "drop table users"
    c.execute(query)
    query = "drop table domains"
    c.execute(query)
    query = "drop table domains"
    c.execute(query)
    query = "drop table domains"
    c.execute(query)
    
    conn.commit()
    c = conn.cursor()

def create_tables():
    database = "knowledge.db"
    conn = connect_to_db(database)

    c = conn.cursor()

    query = """ CREATE TABLE IF NOT EXISTS users (
                                        user_id_id integer PRIMARY KEY,
                                        name text NOT NULL,
                                        username text NOT NULL,
                                        password text NOT NULL,
                                        role text NOT NULL
                                    ); """
    c.execute(query)

    query = """ CREATE TABLE IF NOT EXISTS domains (
                                        domain_id integer PRIMARY KEY,
                                        name text NOT NULL                                    
                                    ); """
    c.execute(query)
    
    query = """ CREATE TABLE IF NOT EXISTS topics (
                                        topic_id integer PRIMARY KEY,
                                        name text NOT NULL,
                                        domain int,
                                        foreign key(domain) references domains(domain_id)
                                    ); """
    c.execute(query)
    
    query = """ CREATE TABLE IF NOT EXISTS knowledge (
                                        know_id integer PRIMARY KEY,
                                        domain int,
                                        topic int,
                                        problem text NOT NUll,
                                        solution text NOT NULL,
                                        foreign key(domain) references domains(domain_id),
                                        foreign key(domain) references domains(domain_id)
                                    ); """
    c.execute(query)

    print("** Tables created")

def create_starter_data():
    database = "knowledge.db"
    conn = connect_to_db(database)
    c = conn.cursor()

    query = "delete from domains"
    c.execute(query)
    
    query = '''INSERT INTO domains (name)
                VALUES( "HTML"), ("CSS"), ("JS"), ("HTML/CSS/JS"), ("JQuery"), ("SQL"), ("Python"), ("Flask"), ("Misc");'''
    c.execute(query)
    conn.commit()

def get_domains():
    database = "knowledge.db"
    conn = connect_to_db(database)
    c = conn.cursor()
    query = '''select name from domains'''
    c.execute(query)
    data = c.fetchall()
    output = []
    for d in data:
        output.append(d[0])
    return output

def get_topics():
    database = "knowledge.db"
    conn = connect_to_db(database)
    c = conn.cursor()
    query = '''select name, domain from topics'''
    c.execute(query)
    data = c.fetchall()
    output = []
    for d in data:
        output.append(d[0])
    return output

def get_knowledge(id):
    print("todo")

def get_knowledge_all():
    database = "knowledge.db"
    conn = connect_to_db(database)
    c = conn.cursor()
    query = '''select domain, topic, problem, solution from knowledge'''
    c.execute(query)
    data = c.fetchall()
    output = []
    for d in data:
        output.append(d[2])
    query = '''select name, domain from topics'''
    c.execute(query)
    data = c.fetchall()
    query = '''select * from knowledge'''
    c.execute(query)
    data = c.fetchall()
    print("------ > * from knowledge: ", data)
    query = '''select * from topics'''
    c.execute(query)
    data = c.fetchall()
    print("------ > * from topics: ", data)
    
    return output

def add_knowledge(domain, topic, problem, solution):
    database = "knowledge.db"
    conn = connect_to_db(database)
    c = conn.cursor()
    query = '''select domain_id from domains where name=?'''
    c.execute(query, (domain,))
    data = c.fetchall()
    try:
        domain_id = data[0][0]
    except:
        print("error with data, data = ", data)
        print("error with data, name to be found = ", domain)
    query = '''insert into topics (name, domain) values (?,?)'''
    c.execute(query, (topic,domain))
    conn.commit()

    query = '''select topic_id from topics where name=?'''
    c.execute(query, (topic,))
    data = c.fetchall()
    topic_id = data[0][0]
    
    query = '''insert into knowledge (domain, topic , problem, solution) values (?,?,?,?)'''
    c.execute(query, (domain_id, topic_id, problem, solution))
    conn.commit()
    print("!! new knowledge added !")

def change_knowledge(domain, topic, problem, solution):
    database = "knowledge.db"
    conn = connect_to_db(database)
    c = conn.cursor()
    query = '''select domain_id from domains where name=?'''
    c.execute(query, (domain,))
    data = c.fetchall()
    try:
        domain_id = data[0][0]
    except:
        print("error with data, data = ", data)
        print("error with data, name to be found = ", domain)

    query = '''select topic_id from topics where name=?'''
    c.execute(query, (topic,))
    data = c.fetchall()
    topic_id = data[0][0]
    
    query= '''update topics set domain=? where topic_id=?'''
    c.execute(query, (domain, topic_id))
    conn.commit()
    
    
    query= '''update knowledge set domain=?, problem=?, solution =? where topic=?'''
    c.execute(query, (domain_id, problem, solution, topic_id))
    conn.commit()
    print("!! Knowledge updated !")

def clear_table_knowledge():
    database = "knowledge.db"
    conn = connect_to_db(database)
    c = conn.cursor()
    query = '''delete from knowledge;'''
    c.execute(query)
    conn.commit()
    print("** Table knowledge CLEARED **")

def clear_table_topics():
    database = "knowledge.db"
    conn = connect_to_db(database)
    c = conn.cursor()
    query = '''delete from topics where topic_id>=0;'''
    c.execute(query)
    conn.commit()
    print("** Table topics CLEARED **")

def get_1_topic(topic):
    output = {}
    output["topic"] = topic
    output["problem"] = "temp_problem"
    output["solution"] = "temp_solution"
    database = "knowledge.db"
    conn = connect_to_db(database)
    c = conn.cursor()
    query = "select topic_id from topics where name=?"
    c.execute(query,(topic,))
    data = c.fetchone()
    topic_id = data[0]
    query = "select domain, problem, solution from knowledge where topic=?"
    c.execute(query,(topic_id,))
    data = c.fetchone()
    domain_id = data[0]
    query = "select name from domains where domain_id=?"
    c.execute(query,(domain_id,))
    data2 = c.fetchone()
    output["domain"] = data2[0]
    output["problem"] = data[1]
    output["solution"] = data[2]
    print("*>", output)
    return output

def topics_filtered(domain):
    output = []
    database = "knowledge.db"
    conn = connect_to_db(database)
    c = conn.cursor()
    print("***** domain:", domain)
    if domain:
        query = "select name from topics where domain=?"
        c.execute(query,(domain,))
        data = c.fetchall()
        print("*5", data)
    else:
        query = "select name from topics"
        c.execute(query)
        data = c.fetchall()
    if data:
        for d in data:
            output.append(d[0])
        print("output:",output)
    print("*3", output)
    return output

def topics_searched(search_str):
    output = []
    database = "knowledge.db"
    conn = connect_to_db(database)
    c = conn.cursor()
    query = "select name from topics"
    c.execute(query)
    data = c.fetchall()
    if data:
        for d in data:
            topic = d[0]

            if search_str.casefold() in topic.casefold():
                output.append(topic)
        print("output:",output)

    return output

def fix():
    database = "knowledge.db"
    conn = connect_to_db(database)
    c = conn.cursor()
    
    query = "select * from topics"
    c.execute(query)
    data = c.fetchall()
    for d in data:
        print(d[0], " - ", d[1], " - ", d[2])

    #query = '''delete from topics where name="SQL Query not working"'''
    #c.execute(query)
    #conn.commit()
    #query = '''delete from knowledge where topic=2'''
    #c.execute(query)
    #query = '''delete from knowledge where topic=5'''
    #c.execute(query)
    #query = '''delete from knowledge where topic=7'''
    #c.execute(query)
    #conn.commit()