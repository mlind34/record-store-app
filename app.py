from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/')
def test():
    return render_template('home.html')

@app.route('/customers', methods=['GET', 'POST'])
def show_customer():
    if request.method == "POST":
        return request
    return render_template('customers.html')

if __name__ == '__main__':
    app.run(debug=True)