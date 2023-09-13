from flask import Flask, request, render_template
import mysql.connector

app = Flask(__name__)

# Function to insert form data into the MySQL database
def insert_user_data(passenger_name, passenger_age, email, password):
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='password',
        database='tickets'
    )
    cursor = connection.cursor()
    sql = 'INSERT INTO users (passenger_name, passenger_age, email, password) VALUES (%s, %s, %s, %s)'
    data = (passenger_name, passenger_age, email, password)
    cursor.execute(sql, data)
    connection.commit()
    connection.close()

# Function to validate user credentials against the database
def validate_user_credentials(email, password):
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='password',
        database='tickets'
    )
    cursor = connection.cursor()
    sql = 'SELECT * FROM users WHERE email = %s AND password = %s'
    data = (email, password)
    cursor.execute(sql, data)
    user = cursor.fetchone()
    connection.close()
    return user

@app.route('/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        passenger_name = request.form['passenger_name']
        passenger_age = request.form['passenger_age']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Add form validation here to check if passwords match, email is valid, etc.
        if password == confirm_password:
            insert_user_data(passenger_name, passenger_age, email, password)
            return render_template('signin.html')
        else:
            return 'Passwords do not match. Please try again.'

    return render_template('login.html')

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = validate_user_credentials(email, password)
        if user:
            # User is authenticated, you can manage user session here if needed
        
            return render_template('app.html')
        else:
            return 'Invalid email or password. Please try again.'

    return render_template('signin.html')


#******************************************************************************************************


# Function to insert form data into the MySQL database
def insert_tickets_data(origin, destination, date_of_travel, number_of_passengers, amount):
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='password',
        database='tickets'
    )
    cursor = connection.cursor()
    sql = 'INSERT INTO booking (origin, destination, date_of_travel, number_of_passengers, amount) VALUES (%s, %s, %s, %s, %s)'
    data = (origin, destination, date_of_travel, number_of_passengers, amount)
    cursor.execute(sql, data)
    connection.commit()
    connection.close()


@app.route('/app', methods=['GET', 'POST'])
def tickets():
    if request.method == 'POST':
        origin = request.form['origin']
        destination = request.form['destination']
        date_of_travel = request.form['date_of_travel']
        number_of_passengers = request.form['number_of_passengers']
        amount = request.form.get('amount')
        insert_tickets_data(origin, destination, date_of_travel, number_of_passengers, amount)
        return render_template('thanks.html')
    
    return render_template('app.html')
    
if __name__ == '__main__':
    app.run(debug=True)
