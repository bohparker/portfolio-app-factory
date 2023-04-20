from flask import Flask, render_template, url_for, abort

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/education')
def education():
    return render_template('education.html')

@app.route('/portfolio')
def portfolio():
    return render_template('portfolio.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run()