from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def test():
    return render_template('home.html')

@app.route('/customers')
def show_customer():
    return render_template('customers.html')

if __name__ == '__main__':
    app.run(debug=True)