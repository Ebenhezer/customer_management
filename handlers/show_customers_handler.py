from flask import Flask, render_template, request, redirect, url_for, session
import sqlalchemy
from werkzeug.exceptions import HTTPException, BadRequest
from utilities.utils import Utilities
from utilities.dbUtils import dbUtilities
import time
import datetime
from datetime import date

from __main__ import app

utilities = Utilities()
dbUtils = dbUtilities()


@app.route('/show', methods=['GET', 'POST'])
def show_customers():
    # Check if user is loggedin
    if 'loggedin' in session:
        
        if "back" in request.form:
            return redirect(url_for('home'))

        try:
            customers = dbUtils.getAllCustomers()

        except Exception:
            message = "Failed to get customer list"
            return render_template('error_page.html', message= message)

        return render_template('show_customers.html',customers=customers, msg='')

    # User is not loggedin redirect to login page
    return redirect(url_for('login'))