import os
from flask import Flask, render_template, request, url_for, redirect
import requests
import authorization
import json

app = Flask(__name__)

# Global Decration
auth_url = authorization.authorization()
header = ''

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
            return redirect(url_for('send_doc'))



    return render_template('oauth.html', auth_url = auth_url, header=header)

# Route to the send document page
@app.route('/send_doc', methods=['GET', 'POST'])
def send_doc():


    if request.method == "POST":
        email = request.form['email']
        pdf_file = request.form['pdf_file']

        print(pdf_file)


        payload = {'File-Name' : 'test',
                'File' : ''
        }

        # Upload the document
        r = requests.post('https://api.na2.echosign.com/api/rest/v5/transientDocuments',
                          headers=header,
                          data=json.dumps(payload))
        r = r.text
        print(r)

    return render_template('send_doc.html')

if __name__ == '__main__':
    app.run(debug=True)