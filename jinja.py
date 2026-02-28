"""Small Flask + Jinja2 examples showing:
- Building URLs dynamically with `url_for`
- Variable rule: route with `/<name>`

Run: `python jinja.py` then open http://127.0.0.1:5000/
"""

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


@app.route('/')
def index():
	# index.html demonstrates `url_for` usage in templates
	return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
	name = request.form.get('name')
	email = request.form.get('email')
	message = request.form.get('message')
	return render_template('result.html', name=name or 'Guest', email=email or '', message=message or '')


@app.route('/hello/<name>')
def hello(name):
	# Demonstrates a variable rule (URL parameter)
	return f"<h1>Hello, {name}!</h1><p>This response comes from the variable rule <code>/hello/{name}</code>.</p><p><a href='{url_for('index')}'>Back</a></p>"


if __name__ == '__main__':
	app.run(debug=True)

