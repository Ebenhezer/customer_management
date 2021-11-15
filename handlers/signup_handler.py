from sqlite3.dbapi2 import paramstyle
from flask import Flask, render_template, request, redirect, url_for, session
import sqlalchemy
import requests
from werkzeug.exceptions import HTTPException, BadRequest
from utilities.utils import Utilities
from utilities.dbUtils import dbUtilities
import time
import json

from __main__ import app

utilities = Utilities()
dbUtils = dbUtilities()

@app.route('/signup', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist inside user submitted form
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        registered = False;
        # Create variables for easy access
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        cellphone = request.form['cellphone']

        #First check if email account already exist
        try:
            user = dbUtils.getUserByEmail(email)
            if user != None:
                msg = 'User already exists'
                return render_template('login.html', register_message=msg)
        except Exception as e:
            message = "Failed to create user"
            return render_template('error_page.html', register_message= message)
            

        #Hash the password
        hashed_password = utilities.hash_password(password)
    
        try:
            dbUtils.createUser(username, email, hashed_password, cellphone)
            registered = True
        except Exception as e:
            message = "Failed to create user"
            return render_template('error_page.html', register_message= message)

        if registered == True:
            # If user registered then attempt to login automatically
            try:
                account = dbUtils.login(email, hashed_password)
                # Check that the user exists, if not, then return the login page
                if (account == None):
                    msg = 'Auto login failed'
                    return render_template('login.html', register_message=msg)

                #Else if the user exists, set the session information then show the home page
                session['loggedin'] = True
                session['username'] = account[1]
                session['email'] = account[2]
                return render_template('home.html', register_message=msg, username=session['username'])

            except Exception as e:
                message = "Failed to automatically login"
                return render_template('error_page.html', register_message= message)
    
    #Otherwise just render the login form
    return render_template('login.html', register_message=msg)
