from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Train Reservation System</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                text-align: center;
                padding-top: 50px;
            }
            .message-box {
                background-color: #fff;
                border-radius: 8px;
                padding: 30px;
                max-width: 400px;
                margin: auto;
                box-shadow: 0 0 10px rgba(0,0,0,0.1);
            }
            h1 {
                color: green;
            }
        </style>
    </head>
    <body>
        <div class="message-box">
            <h1>Booking Successful!</h1>
            <p>Your train reservation was completed successfully.</p>
        </div>
    </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(debug=True)
