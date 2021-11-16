import sqlite3
from sqlite3 import Error
from sqlalchemy import Table, Column, Integer, String, create_engine, MetaData, Text
from sqlalchemy.sql.expression import false

engine = create_engine('sqlite:///customer.sql', echo = False)

#Using ORM
connection = engine.connect()
metadata_obj = MetaData()

user = Table('t_user_info', metadata_obj,
    Column('user_id', Integer, primary_key=True),
    Column('username', String(30), nullable=False),
    Column('email', String(50), key='email'),
    Column('password', String(50), nullable=False),
    Column('cellphone', Integer)
)

customer = Table('t_customer', metadata_obj,
    Column('customer_id', Integer, primary_key=True),
    Column('company_name', String(50), nullable=False),
    Column('customer_email', String(50), key='email'),
    Column('contact_number', Integer)
)

metadata_obj.create_all(engine)

#create a connection to the database

class dbUtilities:

    def createUser(self, username, email, password, cellphone):  
        insert = user.insert().values(username = username, email = email, password=password, cellphone=cellphone)
        connection = engine.connect()
        result = connection.execute(insert)
        return True

    def createCustomer(self, company_name, customer_email, contact_number):  
        insert_query = """INSERT INTO t_customer (company_name, customer_email, contact_number) VALUES (:company_name,:customer_email,:contact_number);"""
        connection = engine.connect()
        results = connection.execute(insert_query, {"company_name":company_name, "customer_email":customer_email, "contact_number":contact_number})
        return True

    def login(self, email, password): 
        query = user.select().where(user.c.email == email).where(user.c.password == password)
        connection = engine.connect()
        account = connection.execute(query) 
        row = account.fetchone()
        return row; 

    def loginByUsername(self, username, password):     
        query = user.select().where(user.c.username == username).where(user.c.password == password)
        connection = engine.connect()
        account = connection.execute(query) 
        row = account.fetchone()
        return row;  
    
    def getUserByEmail(self, email):  
        query = user.select().where(user.c.email == email)
        connection = engine.connect()
        account = connection.execute(query) 
        row = account.fetchone()
        return row; 

    def getAllUsers(self):  
        sql_query = user.select()
        connection = engine.connect()
        result = connection.execute(sql_query)
        users = result.fetchall()  
        return users;

    def getAllCustomers(self):  
        sql_query = customer.select()
        connection = engine.connect()
        result = connection.execute(sql_query)
        account = result.fetchall()  
        return account; 
        #return user 
    
    def getCustomerById(self, customer_id):   
        query = customer.select().where(customer.c.customer_id == customer_id)
        connection = engine.connect()
        account = connection.execute(query) 
        row = account.fetchone()
        return row;

    def updateCustomer(self, customer_id, company_name, customer_email, contact_number):  
        print(customer_id,customer_email,contact_number)
        update_statement = "UPDATE t_customer SET company_name = :company_name, customer_email = :customer_email, \
                                contact_number = :contact_number WHERE customer_id = :customer_id"
        connection = engine.connect()
        results = connection.execute(update_statement, {"company_name":company_name, "customer_email":customer_email, \
                                    "contact_number":contact_number, "customer_id":customer_id })

        # query = customer.update().where(customer.c.customer_id == customer_id).values(company_name=company_name, customer_email=customer_email, contact_number=contact_number)
        # connection = engine.connect()
        # connection.execute(query) 
        return True

    def deleteCustomer(self, customer_id):  

        query = customer.delete().where(customer.c.customer_id == customer_id)
        connection = engine.connect()
        connection.execute(query) 
        return True 
