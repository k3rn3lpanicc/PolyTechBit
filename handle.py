import sqlite3
import json
import time


db_name = "usersdb.db"

class User:
    def __init__(self,name , is_admin , stdcode) -> None:
        self.name = name
        self.is_admin = is_admin
        self.stdcode = stdcode
    def set_chat_id(self , chat_id):
        self.chat_id = chat_id
    def get_info(self) -> str :
        return f"{self.name}:{self.stdcode}"


class Question:
    def __init__(self , question , answer , date , adder) -> None:
        self.question = question
        self.answer = answer
        self.date = date
        self.adder = adder
    def get_info(self):
        return f"{self.question}:{self.answer}"

class Tutorial:
    def __init__(self , name , message_id , adder , date):
        self.name = name
        self.message_id = message_id
        self.adder = adder
        self.date = date
    def get_info(self):
        return f"{self.name}:{self.message_id}"


def insert_user(chat_id , name , std_code):
    conn = sqlite3.connect(db_name)
    conn.execute("insert into users(name,tcode,is_admin,stdcode) values(?,?,?,?)",[name , str(chat_id) , "0" , str(std_code)]) 
    conn.commit()

def remove_user(chat_id):
    conn = sqlite3.connect(db_name)
    conn.execute("DELETE from users where tcode = ?" , [str(chat_id)])
    conn.execute("DELETE from users2 where tid = ?" , [str(chat_id)])    
    conn.commit()
def pre_insert(chat_id):
    conn = sqlite3.connect(db_name)
    conn.execute("insert into users2(tid,state,data) values(?,?,?)" , [str(chat_id) , "" , ""])
    conn.commit()

def set_state(telegram_id, state):
    conn = sqlite3.connect(db_name)
    conn.execute("update users2 set state = ? where tid =?" , [str(state),str(telegram_id)])
    conn.commit()

def get_state(chat_id):
    conn = sqlite3.connect(db_name)
    curs = conn.execute('select state from users2 where tid = ?',[str(chat_id)])
    state = ""
    for row in curs:
        state = row[0]
    if(state == '' or state == None):
        return False
    return state

def get_user(chat_id) -> User:
    conn = sqlite3.connect(db_name)
    curs = conn.execute("SELECT * FROM users WHERE tcode = ?" , [str(chat_id)])
    rr = None
    for row in curs:
        rr = User(row[1] , row[3] , row[4])
        return rr
    return False

def set_column(table_name , column_name , telegram_id,value):
    conn = sqlite3.connect(db_name)
    va = "tid"
    if(table_name == 'users'):
        va = 'tcode'
    if(table_name == "students"):
        va = "stdcode"
    query = "UPDATE "+table_name +" SET "+column_name +" = ? WHERE "+va+" = ?"
    print(query)
    conn.execute(query , [str(value) , str(telegram_id)])
    conn.commit()

def get_value(tablename , telegram_id , column_name):
    va = "tcode" if tablename == 'users' else "tid"
    conn = sqlite3.connect(db_name)
    query = "SELECT "+column_name+" FROM " + tablename + " WHERE "+va+" = ?"
    curs = conn.execute(query , [str(telegram_id)])
    for row in curs:
        return str(row[0])
    return ""

def save_data(chat_id , keyname , value):
    current_data = get_value('users2',chat_id,'data')
    if(current_data==""):
        set_column('users2',"data",chat_id,"{}")
        save_data(chat_id , keyname , value)
    else:
        data = json.loads(current_data)
        data[keyname] = value
        set_column('users2' , 'data',chat_id , json.dumps(data))

def load_data(chat_id , keyname):
    data = json.loads(get_value('users2' ,chat_id,'data'))
    if(keyname in data):
        return data[keyname]
    else:
        return False

def get_std_by_code(stdcode):
    conn = sqlite3.connect(db_name)
    curs = conn.execute("SELECT * FROM students WHERE stdcode = ?" , [str(stdcode)])
    rr = dict()
    for row in curs:
        rr['name'] = row[0]
        rr['code'] = row[1]
        rr['user_name'] = row[2]
        return rr
    return False

def get_parent(stdcode):
    if stdcode.startswith('400310') or stdcode.startswith('401310'):
        tail = stdcode[3:]
        head = str(int(stdcode[:3])-1)
        if head.startswith('3'):
            head = head[1:]
        moadel = head+tail
        return get_std_by_code(moadel)
    else:
        tail = stdcode[2:]
        head = str(int(stdcode[:2])-1)
        moadel = head+tail
        return get_std_by_code(moadel)




def insert_question(question , answer,chat_id):
    try:
        conn = sqlite3.connect(db_name)
        conn.execute("insert into questions(question,answer,date,adder) values(?,?,?,?)",[question , answer,time.time() , str(chat_id)]) 
        conn.commit()
        return True
    except:
        return False
def get_users() -> list :
    conn = sqlite3.connect(db_name)
    curs = conn.execute("SELECT * FROM users")
    rr = []
    for row in curs:
        rr.append(User(row[1] , row[3] , row[4]))
        rr[-1].set_chat_id(row[2])
    return rr

def get_questions() -> list :
    conn = sqlite3.connect(db_name)
    curs = conn.execute("SELECT * FROM questions")
    rr = []
    for row in curs:
        rr.append(Question(row[0] , row[1] , row[2] , row[3]))
    return rr

def get_question(date) -> Question:
    conn = sqlite3.connect(db_name)
    curs = conn.execute("SELECT * FROM questions WHERE date = ?" , [str(date)])
    for row in curs:
        return Question(row[0] , row[1] , row[2] , row[3])
    return False


def insert_tutorial(name , message_id , adder) :
    conn = sqlite3.connect(db_name)
    conn.execute("insert into tutorials(name,message_id,adder,date) values(?,?,?,?)",[name , message_id , adder,str(time.time())])
    conn.commit()

def get_tutorials() -> list :
    conn = sqlite3.connect(db_name)
    curs = conn.execute("SELECT * FROM tutorials")
    rr = []
    for row in curs:
        rr.append(Tutorial(row[0] , row[1] , row[2] , row[3]))
    return rr

def get_tutorial(date) -> Tutorial:
    conn = sqlite3.connect(db_name)
    curs = conn.execute("SELECT * FROM tutorials WHERE date = ?" , [str(date)])
    for row in curs:
        return Tutorial(row[0] , row[1] , row[2] , row[3])
    return False

def delete_tutorial(date):
    conn = sqlite3.connect(db_name)
    conn.execute("DELETE FROM tutorials WHERE date = ?" , [str(date)])
    conn.commit()

def delete_question(date):
    conn = sqlite3.connect(db_name)
    conn.execute("DELETE FROM questions WHERE date = ?" , [str(date)])
    conn.commit()

class Student:
    def __init__(self , name , code , user_name):
        self.name = name
        self.code = code
        self.user_name = user_name
    

def get_student(stdcode) :
    conn = sqlite3.connect(db_name)
    curs = conn.execute("SELECT * FROM students WHERE stdcode = ?" , [str(stdcode)])
    for row in curs:
        return Student(str(row[0]) , str(row[1]) , str(row[2]))
    return False
