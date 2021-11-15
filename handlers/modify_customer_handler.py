from flask import Flask, render_template, request, redirect, url_for, session
import sqlalchemy
from werkzeug.exceptions import HTTPException, BadRequest
import psycopg2
from utilities.dbUtils import dbUtilities
from utilities.utils import Utilities
import time
import datetime
from datetime import date

from __main__ import app

utilities = Utilities()
dbUtils = dbUtilities()

@app.route('/modify', methods=['GET', 'POST'])
def modify_customer():
    # Check if user is loggedin
    if 'loggedin' in session:
        if request.method == 'POST' :
            if  'search' in request.form and 'customer_id' in request.form:
                customer_id = request.form['customer_id']
                customer = None
                
                try:
                    customer = dbUtils.getCustomerById(customer_id)
                    #If none, then customer information was not found
                    if customer == None:
                        return render_template('modify_customer.html', failed_message = "Customer not found")
                    
                    # Else all is good, so render the edit page with the information
                    customer_id = customer[0]
                    customer_name = customer[1]
                    customer_email = customer[2]
                    contact_number = customer[3]
                except:
                    return render_template('modify_customer.html', failed_message = "Failed to get customer information")
                
                return render_template('edit_customer.html',
                                        customer_id = customer_id,
                                        customer_name = customer_name,
                                        customer_email = customer_email,
                                        contact_number = contact_number)

            elif 'edit_customer' in request.form and 'customer_name' in request.form and 'customer_email' in request.form and 'customer_email' in request.form:
                customer_id = request.form['customer_id']
                customer_email = request.form['customer_email']
                customer_name = request.form['customer_name']
                contact_number = request.form['contact_number']
                # Update the customer
                try:
                    dbUtils.updateCustomer(customer_id, customer_name, customer_email, contact_number)
                    return render_template('home.html', success_message ="Successfully updated the customer info")
                except:
                    return render_template('modify_customer.html', failed_message ="Failed to update")
            elif 'delete' in request.form and 'customer_id' in request.form:
                customer_id = request.form['customer_id']
                try:
                    dbUtils.deleteCustomer(customer_id)
                    return render_template('home.html', success_message ="Successful deleted the customer")
                except:
                    return render_template('modify_customer.html', failed_message ="Failed to delete")
            elif 'back' in request.form :
                return render_template('modify_customer.html')
            elif 'back_home' in request.form :
                return redirect(url_for('home'))

        else:      
            return render_template('modify_customer.html',)

    # User is not loggedin redirect to login page
    return redirect(url_for('login'))