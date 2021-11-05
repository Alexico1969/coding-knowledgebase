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

def create_tables():
    print(">> Checkpoint Beta" )
    database = "knowledge.db"
    conn = connect_to_db(database)

    c = conn.cursor()

    '''query = "drop table users"
    c.execute(query)
    query = "drop table domains"
    c.execute(query)
    '''

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

    query = "clear table domains"
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

def add_knowledge(domain, topic, problem, solution):
    database = "knowledge.db"
    conn = connect_to_db(database)
    c = conn.cursor()
    query = '''select domain_id from domains where name=?'''
    c.execute(query, (domain,))
    data = c.fetchall()
    domain_id = data[0][0]

    query = '''insert into topics (name) values (?)'''
    c.execute(query, (topic,))
    conn.commit()

    query = '''select topic_id from topics where name=?'''
    c.execute(query, (topic,))
    data = c.fetchall()
    topic_id = data[0][0]
    
    query = '''insert into knowledge (domain, topic ,problem, solution) values (?,?,?,?)'''
    c.execute(query, (domain_id, topic_id, problem, solution))
    conn.commit()
    print("!! new knowledge added !")