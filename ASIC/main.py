from flask import Flask, render_template, request, url_for, redirect, flash
import authorization

app = Flask(__name__)

auth_url = authorization.authorization()


# Creating a route
@app.route('/', methods=['GET', 'POST'])
def oauth():

    if request.method == "POST":
        auth_responses = request.form['auth_url']
        token = authorization.get_token(auth_responses)

        if token:
            return redirect(url_for('index'))


    return render_template('oauth.html', auth_url = auth_url)

@app.route('/index')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)