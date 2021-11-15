from flask import Flask, render_template, request, redirect, url_for, session
import requests
from werkzeug.exceptions import HTTPException, BadRequest
from utilities.utils import Utilities
from utilities.dbUtils import dbUtilities

app = Flask(__name__)
app.secret_key = 'TedMe1000#'

utilities = Utilities()
dbUtils = dbUtilities()

#import the handlers
from handlers import modify_customer_handler
from handlers import show_customers_handler
from handlers import create_customer_handler
from handlers import signup_handler
from handlers import login_handler


@app.route('/', methods=['GET', 'POST'])
def root():
    if 'loggedin' in session:
        return redirect(url_for('home'))

    # Just return the login page(login.html)
    return render_template('login.html', msg='')

    
@app.route('/home', methods=['GET', 'POST'])
def home():
    if 'loggedin' in session:

        if request.form.get("create"):
            return redirect(url_for('create_customer'))
        elif request.form.get("modify"):
            return redirect(url_for('modify_customer'))
        elif request.form.get("show"):
            return redirect(url_for('show_customers'))

        return render_template('home.html', username=session['username'])

    return render_template('login.html', msg='Not logged in')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('loggedin', None)
    # Then redirect to the login page
    msg= 'Logged out'
    return render_template('login.html', login_message=msg)

# ========================================================================= #

# Handle bad requests

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    message = "Error 404"
    return render_template('error_page.html', message= message), 404

@app.errorhandler(400)
def page_not_found(e):
    # note that we set the 400 status explicitly
    message = "Error 400"
    return render_template('error_page.html', message= message), 400

# handle indexError


if __name__ == "__main__":
    # create the table if it does not exists
    print("Server running on https://127.0.0.1:8000")
    app.run(host='127.0.0.1', port=8000, debug=True)
