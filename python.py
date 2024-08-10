from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import pymysql


app = Flask(__name__)



def fetch_data(query, args):
    try:
        # Database connection parameters
        host = '127.0.0.1'
        user = 'root'
        password = '1234'
        database = 'criminaldb'

        # Establish the database connection
        db = pymysql.connect(host=host, user=user, password=password, db=database)

        # Create a cursor object
        cursor = db.cursor()

        # Execute the query to fetch data
        cursor.execute(query, args)

        # Fetch all rows from the executed query
        data = cursor.fetchall()

        if data:
            # Create a DataFrame from the fetched data
            df = pd.DataFrame(data, columns=[col[0] for col in cursor.description])
            return df
        else:
            # Return an empty DataFrame
            return pd.DataFrame()

    except pymysql.MySQLError as err:
        print(f"Error connecting to MySQL: {err}")
        return pd.DataFrame()

    finally:
        # Ensure the connection is closed even if an error occurs
        if 'db' in locals() and db.open:
            db.close()
            
            
            
            



# def get_db_connection():
#     app.config['MYSQL_HOST'] = '127.0.0.1'
#     app.config['MYSQL_USER'] = 'root'
#     app.config['MYSQL_PASSWORD'] = '1234'
#     app.config['MYSQL_DB'] = 'criminaldb'
#     return pymysql.connect(host=app.config['MYSQL_HOST'],
#                            user=app.config['MYSQL_USER'],
#                            password=app.config['MYSQL_PASSWORD'],
#                            db=app.config['MYSQL_DB'])

# @app.route('/')
# def home():
#     return render_template('login.html')

# @app.route('/register', methods=['POST'])
# def register_user():
#     firstname = request.form['firstname']
#     lastname = request.form['lastname']
#     email = request.form['email']
#     password = request.form['password']

#     conn = get_db_connection()
#     try:
#         cur = conn.cursor()
#         cur.execute("INSERT INTO user_info(firstname, lastname, email, password) VALUES (%s, %s, %s, %s)",
#                     (firstname, lastname, email, password))
#         conn.commit()
#     except Exception as e:
#         print(f"Error: {e}")
#     finally:
#         cur.close()
#         conn.close()

#     return redirect(url_for('home'))

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         email = request.form['email']
#         password = request.form['password']

#         conn = get_db_connection()
#         try:
#             cur = conn.cursor()
#             cur.execute("SELECT * FROM user_info WHERE email=%s AND password=%s", (email, password))
#             result = cur.fetchone()
#         except Exception as e:
#             print(f"Error: {e}")
#             result = None
#         finally:
#             cur.close()
#             conn.close()

#         if result:
#             return render_template('index.html',result=result,fname = result[1])
#         else:
#             return 'Invalid email or password'

#     return render_template('login.html')






# @app.route('/', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         email = request.form['email']
#         password = request.form['password']

#         try:
#             # Database connection parameters
#             host = '127.0.0.1'
#             user = 'root'
#             password_db = '1234'
#             database = 'criminaldb'

#             # Establish the database connection
#             db = pymysql.connect(host=host, user=user, password=password_db, db=database)

#             # Create a cursor object
#             cursor = db.cursor()

#             # Execute the query to fetch user data
#             cursor.execute("SELECT * FROM user_info WHERE email=%s AND password=%s", (email, password))
#             result = cursor.fetchone()

#         except pymysql.MySQLError as err:
#             print(f"Error connecting to MySQL: {err}")
#             result = None

#         finally:
#             # Ensure the connection is closed
#             if 'db' in locals() and db.open:
#                 db.close()

#         if result:
#             return render_template('index.html', result=result, fname=result[1])
#         else:
#             return 'Invalid email or password'

#     return render_template('login.html')


# @app.route('/register', methods=['POST'])
# def register_user():
#     firstname = request.form['firstname']
#     lastname = request.form['lastname']
#     email = request.form['email']
#     password = request.form['password']

#     try:
#         # Database connection parameters
#         host = '127.0.0.1'
#         user = 'root'
#         password_db = '1234'
#         database = 'criminaldb'

#         # Establish the database connection
#         db = pymysql.connect(host=host, user=user, password=password_db, db=database)

#         # Create a cursor object
#         cursor = db.cursor()

#         # Execute the query to insert data
#         cursor.execute("INSERT INTO user_info (firstname, lastname, email, password) VALUES (%s, %s, %s, %s)",
#                        (firstname, lastname, email, password))
#         db.commit()

#     except pymysql.MySQLError as err:
#         print(f"Error inserting data into MySQL: {err}")
#         db.rollback()

#     finally:
#         # Ensure the connection is closed
#         if 'db' in locals() and db.open:
#             db.close()

#     return redirect(url_for('login'))













@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        search_type = request.form.get('search_type', 'default_search_type')
        if search_type == 'crime.html':
            return redirect(url_for('crime'))
        elif search_type == 'criminal.html':
            return redirect(url_for('criminal'))
        elif search_type == 'crime_occurrence.html':
            return redirect(url_for('crime_occurrence'))
        elif search_type == 'location.html':
            return redirect(url_for('location'))
        elif search_type == 'suspect.html':
            return redirect(url_for('suspect'))
    else:
        return render_template('index.html')
    
    
    
@app.route('/home')
def home():
    return render_template('index.html')
    
    
@app.route('/crime', methods=['GET', 'POST'])
def crime():
    if request.method == 'POST':
        id = request.form.get('id')
        name = request.form.get('name')
        category = request.form.get('category')
        
        # Prepare the SQL query with placeholders
        query = "SELECT * FROM crime WHERE id = %s OR name = %s OR category = %s"
        
        # Ensure the arguments are passed as a tuple
        args = (id, name, category)
        
        # Fetch data using the updated function
        df = fetch_data(query, args)
        
        if df.empty:
            html_table = ""
        else:
            html_table = df.to_html(classes='table table-striped')
        
        return render_template('result.html', data=html_table)
    else:
        return render_template('crime.html')
    
    
@app.route('/criminal', methods=['GET', 'POST'])
def criminal():
    if request.method == 'POST':
        id = request.form.get('id')
        name = request.form.get('name')
        crime = request.form.get('crime')

        query = "SELECT * FROM criminal WHERE id = %s OR name = %s OR crime = %s"
        args = (id, name, crime)

        df = fetch_data(query, args)
        if df.empty:
            html_table = ""
        else:
            html_table = df.to_html(classes='table table-striped')
        
        return render_template('result.html', data=html_table)
    else:
        return render_template('criminal.html')





@app.route('/crime_occurrence', methods=['GET', 'POST'])
def crime_occurrence():
    if request.method == 'POST':
        crime_id = request.form.get('crime_id')
        location_id = request.form.get("location_id")
        date_of_crime = request.form.get('date_of_crime')

        query = "SELECT * FROM crime_occurrence WHERE crime_id = %s OR location_id = %s OR date_of_crime = %s"
        args = (crime_id, location_id, date_of_crime)

        df = fetch_data(query, args)
        if df.empty:
            html_table = ""
        else:
            html_table = df.to_html(classes='table table-striped')
        
        return render_template('result.html', data=html_table)
    else:
        return render_template('crime_occurrence.html')

@app.route('/location', methods=['GET', 'POST'])
def location():
    if request.method == 'POST':
        city = request.form.get('city')
        state = request.form.get('state')
        zip = request.form.get('zip')

        query = "SELECT * FROM location WHERE city = %s OR state = %s OR zip = %s"
        args = (city, state, zip)

        df = fetch_data(query, args)
        if df.empty:
            html_table = ""
        else:
            html_table = df.to_html(classes='table table-striped')
        
        return render_template('result.html', data=html_table)
    else:
        return render_template('location.html')

@app.route('/suspect', methods=['GET', 'POST'])
def suspect():
    if request.method == 'POST':
        id = request.form.get('id')
        name = request.form.get('name')
        gender = request.form.get('gender')
        height = request.form.get('height')

        query = "SELECT * FROM suspect WHERE id = %s OR name = %s OR gender = %s OR height = %s"
        args = (id, name, gender, height)

        df = fetch_data(query, args)
        html_table = df.to_html(classes='table table-striped') if not df.empty else "No data found"
        
        return render_template('result.html', data=html_table)
    else:
        return render_template('suspect.html')
    
    
    
@app.route('/insert_crime', methods=['POST'])
def insert_crime():
    id = request.form.get('id')
    name = request.form.get('name')
    category = request.form.get('category')

    query = "INSERT INTO crime (id, name, category) VALUES (%s, %s, %s)"
    args = (id, name, category)

    try:
        # Database connection parameters
        host = '127.0.0.1'
        user = 'root'
        password = '1234'
        database = 'criminaldb'

        # Establish the database connection
        db = pymysql.connect(host=host, user=user, password=password, db=database)

        # Create a cursor object
        cursor = db.cursor()

        # Execute the query to insert data
        cursor.execute(query, args)

        # Commit the transaction
        db.commit()
        donein = f"Insertion Done"
        return render_template('crime.html', donein=donein)

    except pymysql.MySQLError as err:
        print(f"Error inserting data into MySQL: {err}")
        db.rollback()
        return "Error inserting data into MySQL"

    finally:
        # Ensure the connection is closed
        if 'db' in locals() and db.open:
            db.close()
            
            
            
            
@app.route('/insert_criminal', methods=['POST'])
def insert_criminal():
    id = request.form.get('id')
    name = request.form.get('name')
    crime = request.form.get('crime')
    crime_location = request.form.get('crime_location')
    date_of_crime = request.form.get('date_of_crime')
    status = request.form.get('status')
    notes = request.form.get('notes')

    query = "INSERT INTO criminal (id, name, crime, crime_location, date_of_crime, status, notes) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    args = (id, name, crime, crime_location, date_of_crime, status, notes)

    try:
        # Database connection parameters
        host = '127.0.0.1'
        user = 'root'
        password = '1234'
        database = 'criminaldb'

        # Establish the database connection
        db = pymysql.connect(host=host, user=user, password=password, db=database)

        # Create a cursor object
        cursor = db.cursor()

        # Print the query and arguments for debugging
        print("Executing query:", query)
        print("With arguments:", args)

        # Execute the query to insert data
        cursor.execute(query, args)

        # Commit the transaction
        db.commit()

        donein = f"Insertion Done"
        return render_template('criminal.html', donein=donein)

    except pymysql.MySQLError as err:
        # Print the exact error message for debugging
        print(f"Error inserting data into MySQL: {err}")
        db.rollback()
        return f"Error inserting data into MySQL: {err}"

    finally:
        # Ensure the connection is closed
        if 'db' in locals() and db.open:
            db.close()
            
            
@app.route('/insert_crime_occurrence', methods=['POST'])
def insert_crime_occurrence():
    
    suspect_id = request.form.get('suspect_id')
    crime_id = request.form.get('crime_id')
    location_id = request.form.get('location_id')
    date_of_crime = request.form.get('date_of_crime')
    status = request.form.get('status')
    notes = request.form.get('notes')
    
    name = request.form.get('name')
    category = request.form.get('category')

    query = "INSERT INTO crime_occurrence(suspect_id, crime_id, location_id, date_of_crime, status, notes) VALUES (%s, %s, %s, %s, %s, %s)"
    args = (suspect_id, crime_id, location_id, date_of_crime,status, notes)

    try:
        # Database connection parameters
        host = '127.0.0.1'
        user = 'root'
        password = '1234'
        database = 'criminaldb'

        # Establish the database connection
        db = pymysql.connect(host=host, user=user, password=password, db=database)

        # Create a cursor object
        cursor = db.cursor()

        # Execute the query to insert data
        cursor.execute(query, args)

        # Commit the transaction
        db.commit()

        donein = f"Insertion Done"
        return render_template('crime_occurrence.html', donein=donein)

    except pymysql.MySQLError as err:
        print(f"Error inserting data into MySQL: {err}")
        db.rollback()
        return f"Error inserting data into MySQL: {err}"
        

    finally:
        # Ensure the connection is closed
        if 'db' in locals() and db.open:
            db.close()
            
            
@app.route('/insert_suspect', methods=['POST'])
def insert_suspect():
    
    id = request.form.get('id')
    name = request.form.get('name')
    birthdate = request.form.get('birthdate')
    gender = request.form.get('gender')
    weight = request.form.get('weight')
    height = request.form.get('height')
    notes = request.form.get('notes')
    
    name = request.form.get('name')
    category = request.form.get('category')

    query = "INSERT INTO suspect(id, name, birthdate, gender, height, weight, notes) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    args = (id, name, birthdate, gender, height, weight, notes)

    try:
        # Database connection parameters
        host = '127.0.0.1'
        user = 'root'
        password = '1234'
        database = 'criminaldb'

        # Establish the database connection
        db = pymysql.connect(host=host, user=user, password=password, db=database)

        # Create a cursor object
        cursor = db.cursor()

        # Execute the query to insert data
        cursor.execute(query, args)

        # Commit the transaction
        db.commit()

        donein = f"Insertion Done"
        return render_template('suspect.html', donein=donein)

    except pymysql.MySQLError as err:
        print(f"Error inserting data into MySQL: {err}")
        db.rollback()
        return f"Error inserting data into MySQL: {err}"
        

    finally:
        # Ensure the connection is closed
        if 'db' in locals() and db.open:
            db.close()
            
            
@app.route('/insert_location', methods=['POST'])
def insert_location():
    
    id = request.form.get('id')
    address = request.form.get('address')
    city = request.form.get('city')
    state = request.form.get('state')
    zip = request.form.get('zip')
    
    notes = request.form.get('notes')
    
    name = request.form.get('name')
    category = request.form.get('category')

    query = "INSERT INTO location(id, address, city, state, zip, notes) VALUES (%s, %s, %s, %s, %s, %s)"
    args = (id, address, city, state, zip, notes)

    try:
        # Database connection parameters
        host = '127.0.0.1'
        user = 'root'
        password = '1234'
        database = 'criminaldb'

        # Establish the database connection
        db = pymysql.connect(host=host, user=user, password=password, db=database)

        # Create a cursor object
        cursor = db.cursor()

        # Execute the query to insert data
        cursor.execute(query, args)

        # Commit the transaction
        db.commit()

        donein = f"Insertion Done"
        return render_template('location.html', donein=donein)

    except pymysql.MySQLError as err:
        print(f"Error inserting data into MySQL: {err}")
        db.rollback()
        return f"Error inserting data into MySQL: {err}"
        

    finally:
        # Ensure the connection is closed
        if 'db' in locals() and db.open:
            db.close()
            
@app.route('/delete_crime', methods=['POST'])
def delete_crime():
    id = request.form.get('id')

    # Query to check if the record exists
    check_query = "SELECT * FROM crime WHERE id = %s"
    delete_query = "DELETE FROM crime WHERE id = %s"
    args = (id,)

    try:
        # Database connection parameters
        host = '127.0.0.1'
        user = 'root'
        password = '1234'
        database = 'criminaldb'

        # Establish the database connection
        db = pymysql.connect(host=host, user=user, password=password, db=database)

        # Create a cursor object
        cursor = db.cursor()

        # Check if the record exists
        cursor.execute(check_query, args)
        record = cursor.fetchone()

        if record:
            # Record exists, proceed to delete
            cursor.execute(delete_query, args)
            db.commit()
            done = f"Deletion Done"
            return render_template('crime.html', done=done)
        else:
            # Record not found, show error message
            error = f"No record found with ID: {id}"
            return render_template('crime.html', error=error)

    except pymysql.MySQLError as err:
        print(f"Error deleting data from MySQL: {err}")
        db.rollback()
        error = f"Error deleting data from MySQL: {err}"
        return render_template('crime.html', error=error)

    finally:
        # Ensure the connection is closed
        if 'db' in locals() and db.open:
            db.close()

            
@app.route('/delete_criminal', methods=['POST'])
def delete_criminal():
    id = request.form.get('id')

    # Query to check if the record exists
    check_query = "SELECT * FROM criminal WHERE id = %s"
    delete_query = "DELETE FROM criminal WHERE id = %s"
    args = (id)

    try:
        # Database connection parameters
        host = '127.0.0.1'
        user = 'root'
        password = '1234'
        database = 'criminaldb'

        # Establish the database connection
        db = pymysql.connect(host=host, user=user, password=password, db=database)

        # Create a cursor object
        cursor = db.cursor()

        # Check if the record exists
        cursor.execute(check_query, args)
        record = cursor.fetchone()

        if record:
            # Record exists, proceed to delete
            cursor.execute(delete_query, args)
            db.commit()
            done = f"Deletion Done"
            return render_template('criminal.html', done=done)
        else:
            # Record not found, show error message
            error = f"No record found with ID: {id}"
            return render_template('criminal.html', error=error)

    except pymysql.MySQLError as err:
        print(f"Error deleting data from MySQL: {err}")
        db.rollback()
        error = f"Error deleting data from MySQL: {err}"
        return render_template('criminal.html', error=error)

    finally:
        # Ensure the connection is closed
        if 'db' in locals() and db.open:
            db.close()
            
            
@app.route('/delete_crime_occurrence', methods=['POST'])
def delete_crime_occurrence():
    id = request.form.get('crime_id')

    # Query to check if the record exists
    check_query = "SELECT * FROM crime_occurrence WHERE crime_id = %s"
    delete_query = "DELETE FROM crime_occurrence WHERE crime_id = %s"
    args = (id)

    try:
        # Database connection parameters
        host = '127.0.0.1'
        user = 'root'
        password = '1234'
        database = 'criminaldb'

        # Establish the database connection
        db = pymysql.connect(host=host, user=user, password=password, db=database)

        # Create a cursor object
        cursor = db.cursor()

        # Check if the record exists
        cursor.execute(check_query, args)
        record = cursor.fetchone()

        if record:
            # Record exists, proceed to delete
            cursor.execute(delete_query, args)
            db.commit()
            done = f"Deletion Done"
            return render_template('crime_occurrence.html', done=done)
        else:
            # Record not found, show error message
            error = f"No record found with ID: {id}"
            return render_template('crime_occurrence.html', error=error)

    except pymysql.MySQLError as err:
        print(f"Error deleting data from MySQL: {err}")
        db.rollback()
        error = f"Error deleting data from MySQL: {err}"
        return render_template('crime_occurrence.html', error=error)

    finally:
        # Ensure the connection is closed
        if 'db' in locals() and db.open:
            db.close()
            
            
@app.route('/delete_location', methods=['POST'])
def delete_location():
    id = request.form.get('id')

    # Query to check if the record exists
    check_query = "SELECT * FROM location WHERE id = %s"
    delete_query = "DELETE FROM location WHERE id = %s"
    args = (id)

    try:
        # Database connection parameters
        host = '127.0.0.1'
        user = 'root'
        password = '1234'
        database = 'criminaldb'

        # Establish the database connection
        db = pymysql.connect(host=host, user=user, password=password, db=database)

        # Create a cursor object
        cursor = db.cursor()

        # Check if the record exists
        cursor.execute(check_query, args)
        record = cursor.fetchone()

        if record:
            # Record exists, proceed to delete
            cursor.execute(delete_query, args)
            db.commit()
            done = f"Deletion Done"
            return render_template('location.html', done=done)
        else:
            # Record not found, show error message
            error = f"No record found with ID: {id}"
            return render_template('location.html', error=error)

    except pymysql.MySQLError as err:
        print(f"Error deleting data from MySQL: {err}")
        db.rollback()
        error = f"Error deleting data from MySQL: {err}"
        return render_template('location.html', error=error)

    finally:
        # Ensure the connection is closed
        if 'db' in locals() and db.open:
            db.close()
            
            
            
@app.route('/delete_suspect', methods=['POST'])
def delete_suspect():
    id = request.form.get('id')

    # Query to check if the record exists
    check_query = "SELECT * FROM suspect WHERE id = %s"
    delete_query = "DELETE FROM suspect WHERE id = %s"
    args = (id)

    try:
        # Database connection parameters
        host = '127.0.0.1'
        user = 'root'
        password = '1234'
        database = 'criminaldb'

        # Establish the database connection
        db = pymysql.connect(host=host, user=user, password=password, db=database)

        # Create a cursor object
        cursor = db.cursor()

        # Check if the record exists
        cursor.execute(check_query, args)
        record = cursor.fetchone()

        if record:
            # Record exists, proceed to delete
            cursor.execute(delete_query, args)
            db.commit()
            done = f"Deletion Done"
            return render_template('suspect.html', done=done)
        else:
            # Record not found, show error message
            error = f"No record found with ID: {id}"
            return render_template('suspect.html', error=error)

    except pymysql.MySQLError as err:
        print(f"Error deleting data from MySQL: {err}")
        db.rollback()
        error = f"Error deleting data from MySQL: {err}"
        return render_template('suspect', error=error)

    finally:
        # Ensure the connection is closed
        if 'db' in locals() and db.open:
            db.close()
            
            
            

            




if __name__ == '__main__':
    app.run(debug=True)