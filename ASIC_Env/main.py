"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    This is a flask micro-framework that will integrate the client side web application to integrate with adobe
    echo sign backend server with their api. 
    Written By: Nathan Nguyen
    Date: 2/2/2018
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
import os
from flask import Flask, render_template, request, url_for, redirect
from werkzeug.utils import secure_filename
import requests
import authorization
import agreements

# Flask config set up
app = Flask(__name__)
APP_ROOT = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, '/instance')
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'jpg', 'png', 'doc', 'docx', 'gif', 'rtf'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Global authorization declaration
auth_url = authorization.authorization()

# Global variable that will store all of our cookies during the session
session = {}

# Route to the authorization page
@app.route('/', methods=['GET', 'POST'])
def oauth():

    global session

    # If user clicks get token button
    if request.method == "POST":

        # Grab the authorization url from the input field
        auth_responses = request.form['auth_url']

        # Fetch the access token information
        token = authorization.get_token(auth_responses)

        session['header'] = {'Access-Token': '{}'.format(token['access_token'])}

        # Redirect to the user to the send document page if token is valid
        if token:
            return redirect(url_for('upload_doc', session=session))

    return render_template('oauth.html', auth_url = auth_url, session=session)


# Route to the upload document page
@app.route('/upload_doc', methods=['GET', 'POST'])
def upload_doc():

    global app

    # If the user clicks submit button
    if request.method == "POST":

        # Extract recipients email address
        email = request.form['email']
        session['email'] = email.split(' ')

        # Extract the pdf file that the user and secure save it to the file system
        f = request.files['file']
        f.save(secure_filename(f.filename))

        # Form data for api call
        data = {
            'Mine-Type': 'application/rtf',
            'File-Name': 'RTF File'
        }

        # File data for api call
        doc_file = {'File': open(f.filename, 'rb')}

        # Post transientDocument and get document ID
        session['transientID'] = requests.post('https://api.na2.echosign.com/api/rest/v5/transientDocuments',
                                               headers=session['header'],
                                               data=data,
                                               files=doc_file).json().get('transientDocumentId')

        if session['transientID']:
            return redirect((url_for('send_doc', session=session)))

    return render_template('upload_doc.html')



# Route to the send document page
@app.route('/send_doc')
def send_doc():

    agreementID_records = {}

    # Iterate through email list and request a post call to send out documents
    for recipient in session['email']:
        agreement = agreements.create_agreement(session['transientID'], recipient)
        agreementID = requests.post('https://api.na2.echosign.com:443/api/rest/v5/agreements',
                                    headers=session['header'],
                                    json=agreement).json().get('agreementId')

        # Store all recipient's email address along with their agreement ID's
        agreementID_records[recipient] = agreementID

    return render_template('send_doc.html')

if __name__ == '__main__':
    app.run(debug=True)