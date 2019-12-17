#!/usr/bin/python3
from flask import Flask, Response, redirect, request, session, url_for
from datetime import timedelta
import os, operator, random

class Flask(Flask):
    def process_response(self, response):
        # Every response will be processed here first
        super(Flask, self).process_response(response)
        response.headers['Server'] = 'Microsoft-IIS/10.0'
        del response.headers['Vary']
        return(response)


app = Flask(__name__)
app.config['SECRET_KEY'] =  os.urandom(32)
app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(seconds=60)


# Error Handler
@app.errorhandler(401)
def access_denied_error(error):
    return('Try Harder!!!', 200)

@app.errorhandler(404)
def not_found_error(error):
    return('Try Harder!!!', 200)
    
@app.errorhandler(405)
def invalid_method_error(error):
    return('Try Harder!!!', 200)

@app.errorhandler(500)
def internal_error(error):
    return('Try Harder!!!', 200)


# Challenge
def randomCalc():
    ops = {'+':operator.add,
           '-':operator.sub,
           '*':operator.mul,
           '/':operator.truediv}
    n1 = round(random.uniform(1.00,999.00), 2)
    n2 = round(random.uniform(1.00,999.00), 2)
    op = random.choice(list(ops.keys()))
    ans = "{0:.2f}".format(float(ops.get(op)(n1,n2)))
    return(n1,op,n2,ans)

@app.route('/', methods = ['GET'])
def index():
    return redirect(url_for('flag'))

@app.route('/reset', methods = ['GET'])
def reset():
    session.pop('attempts', None)
    return("Session has been reset. You can now try again!")

@app.route('/flag', methods = ['GET', 'POST'])
def flag():
    # Challenge should be performed with HTTP POST request
    if request.method == 'POST':
        answer = str(request.form.get('answer'))
        if ('attempts' in session):
            if (session['attempts'] == 10) and (answer == 'YES_I_CAN!'):
                return("Flag is: FLAG{I_c4n_h4z_c0d3z_n_crypt0_yisssss!!!}")
            elif (answer == session['ans']):
                session['attempts'] = session.get('attempts') + 1
                if session['attempts'] == 10:
                    return("Total POST attempts: {0}<br>Can you decode this? TFJGX1ZfUE5BIQ==".format(session.get('attempts')))
                else:
                    num1,optr,num2,ans = randomCalc()
                    session['num1'] = str(num1)
                    session['optr'] = str(optr)
                    session['num2'] = str(num2)
                    session['ans'] = str(ans)
                    return("Total POST attempts: {0}<br>Problem: {1} {2} {3} <br>".format(session.get('attempts'),session['num1'],session['optr'],session['num2']))
            else:
                session.pop('attempts', None)
                return("Answer invalid - Try Harder!!!")
                
        else:
            # First visit
            num1,optr,num2,ans = randomCalc()
            session['num1'] = str(num1)
            session['optr'] = str(optr)
            session['num2'] = str(num2)
            session['ans'] = str(ans)
            session['attempts'] = 1
            return('Total POST attempts: {0}, send a POST request with parameter "answer" in the body.<br>Problem:<br>{1} {2} {3} <br>'.format(session.get('attempts'),session['num1'],session['optr'],session['num2']))
            
    # Print instructions for HTTP GET request
    else:
        session.pop('attempts', None)
        return('''Challenge: C4n I h4z c0d3 n crypt0?<br>
        How to get the Flag:<br>
        1. Submit a POST request to /flag<br>
        2. Evaluate the received data<br>
        3. Submit the evaluated data to /flag<br>
        4. Repeat 2 and 3, 10 times<br>
        4. ???<br>
        5. PROFIT!!!<br>
        <br>
        NOTE: Each data submission attempt will expire in 3 seconds if left unattended
        HINT: String
        ''')
    
if __name__ == "__main__":
    app.run(debug = False, host = '0.0.0.0', port = 80)

