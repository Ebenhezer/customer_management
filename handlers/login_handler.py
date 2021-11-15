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

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''

    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
       # Output message if something goes wrong...
        msg = ''

        username = request.form['username']
        password = request.form['password']

        # Hash the password
        hashed_password = utilities.hash_password(password)
 
        # If user registered then attempt to login automatically
        try:
            account = dbUtils.login(username, hashed_password)
            # Check that the user exists, if not, then return the login page
            if (account == None):
                try:
                    account = dbUtils.loginByUsername(username, hashed_password)
                    if (account == None):
                        msg = 'Incorrect username/password'
                        return render_template('login.html', login_message=msg)
                except:
                    msg = '(B) Login failed'
                    return render_template('login.html', login_message=msg)

            #Else if the user exists, set the session information then show the home page
            session['loggedin'] = True
            session['username'] = account[1]
            session['email'] = account[2]

            return redirect(url_for('home'))
        except Exception as e:
                #return e
                msg = "(C)Failed to login"
                return render_template('login.html', login_message=msg)
    else:
        #Method is a GET so firs check if logged in
        if "loggedin" in session:
            return redirect(url_for('home'))
        else:
            msg = "Please log in"
            return render_template('login.html', login_message=msg)
    # Then redirect to the login page
    return render_template('login.html')
