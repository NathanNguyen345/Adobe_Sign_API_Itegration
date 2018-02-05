import os
from flask import Flask, render_template, request, url_for, redirect
from werkzeug.utils import secure_filename
import requests
import authorization
import agreements

# Set upload path and allowed extensions
UPLOAD_FOLDER = '/pdf/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'jpg', 'png', 'doc', 'docx', 'gif', 'rtf'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Global Decration
auth_url = authorization.authorization()
header = ''
transcientID = ''
email = ''

# Route to the authorization page
@app.route('/', methods=['GET', 'POST'])
def oauth():

    global header

    # If user clicks get token button
    if request.method == "POST":

        # Grab the authorization url from the input field
        auth_responses = request.form['auth_url']

        # Fetch the access token information
        token = authorization.get_token(auth_responses)

        header = {'Access-Token': '{}'.format(token['access_token'])}
        base_uris = requests.get('https://api.na2.echosign.com//api/rest/v5/base_uris', headers=header)

        # Redirect to the user to the send document page if token is valid
        if token:
            return redirect(url_for('upload_doc'))

    return render_template('oauth.html', auth_url = auth_url, header=header)



def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



# Route to the upload document page
@app.route('/upload_doc', methods=['GET', 'POST'])
def upload_doc():

    global transcientID
    global email

    if request.method == "POST":

        # Extract recipients email address
        email = request.form['email']
        email = email.split(' ')

        # Extract the pdf file that the user and secure save it to the file system
        f = request.files['file']
        f.save(secure_filename(f.filename))

        # Form data for api call
        data = {
            'Mine-Type': 'application/pdf',
            'File-Name' : 'PDF File'
        }

        # File data for api call
        # pdf_file = {'File': open('test_doc.pdf', 'rb')}
        pdf_file = {'File': open('test.rtf', 'rb')}

        # Post transientDocument and get document ID
        transcientID = requests.post('https://api.na2.echosign.com/api/rest/v5/transientDocuments',
                                     headers=header,
                                     data=data,
                                     files=pdf_file).json().get('transientDocumentId')

        if transcientID:
            return redirect((url_for('send_doc')))


    return render_template('upload_doc.html')



# Route to the send document page
@app.route('/send_doc')
def send_doc():

    agreementID_records = {}

    # Iterate through email list and request a post call to send out documents
    for recipient in email:
        agreement = agreements.create_agreement(transcientID, recipient)
        agreementID = requests.post('https://api.na2.echosign.com:443/api/rest/v5/agreements',
                                    headers=header,
                                    json=agreement).json().get('agreementId')

        # Store all reciept's email address along with their agreement ID's
        agreementID_records[recipient] = agreementID

    return render_template('send_doc.html')

if __name__ == '__main__':
    app.run(debug=True)