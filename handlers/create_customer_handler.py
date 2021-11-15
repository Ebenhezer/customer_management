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


@app.route('/add', methods=['GET', 'POST'])
def create_customer():
    # Check if user is loggedin
    if 'loggedin' in session:

        if request.method == 'POST':
            if 'add_customer' in request.form and 'company_name' in request.form and 'customer_email' in request.form and 'contact_number' in request.form:
                customer_added = False;
                # Create variables for easy access
                company_name = request.form['company_name']
                customer_email = request.form['customer_email']
                contact_number = request.form['contact_number']

                if len(company_name) > 50 or len(company_name) <= 0:
                    return render_template('new_customer.html', 
                        failed_message='Company name length must be 1-50 char',
                        company_name= company_name,
                        customer_email= customer_email,
                        contact_number = contact_number)
                elif len(customer_email) > 50 or len(customer_email) <= 0:
                    return render_template('new_customer.html', 
                        failed_message='Customer email length must be 1-50 char',
                        company_name= company_name,
                        customer_email= customer_email,
                        contact_number = contact_number)
                elif len(contact_number) > 11 or len(contact_number) <= 0:
                    return render_template('new_customer.html', 
                        failed_message='Contact number length must be less than or equal to 11',
                        company_name= company_name,
                        customer_email= customer_email,
                        contact_number = contact_number)
                # Add a new customer
                try:
                    dbUtils.createCustomer(company_name, customer_email, contact_number)
                    customer_added = True
                except Exception as e:
                    message = "Failed to create user"
                    return render_template('error_page.html', message= message)

                if customer_added ==True:
                    return render_template('home.html', username=session['username'], success_message="Customer successfully saved")
            if 'back' in request.form :
                return redirect(url_for('login'))
        else:
            #Means Method is a GET, so render the new customer page
            return render_template('new_customer.html', msg='')

    # User is not loggedin redirect to login page
    return redirect(url_for('login'))