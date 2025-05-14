from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # For session-based flash messages

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    email = request.form['email']

    if name and email:
        # Insert data into the database here if needed
        flash('Form submitted successfully!', 'success')
        return redirect(url_for('home'))
    else:
        flash('Please fill out all fields!', 'error')
        return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
