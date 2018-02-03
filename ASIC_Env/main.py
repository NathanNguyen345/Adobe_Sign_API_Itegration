from flask import Flask, render_template

app = Flask(__name__)

# Creating a route
@app.route('/')
def oauth():
    return render_template('oauth.html')

@app.route('/index')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)