from flask import Flask, jsonify, render_template
import pymysql

app = Flask(__name__)

# define a flask function to get database connection using pymsql method
def get_db_connection():
    connection = pymysql.connect(host='mydb.cqz7h2q6z5qg.us-west-1.rds.amazonaws.com',
                                 user='dbuser',
                                 password='dbpassword',
                                 db='devprojdb',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor),
    return connection


@app.route('/health') # To show that the application is up and running
def health():
    return jsonify({"status": "UP"})


@app.route('/create_table')
def create_table():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE users (id INT, name VARCHAR(255))")
    connection.commit()
    connection.close()
    return jsonify({"status": "Table Created"})


@app.route('/insert_record', methods=['POST'])
def insert_record():
    name = request.json['name']
    connection = get_db_connection()
    cursor = connection.cursor()
    insert_query = "INSERT INTO example_table (name) VALUES ('{}')".format(
        name)
    cursor.execute(insert_query, (name,))
    connection.commit()
    connection.close()
    return jsonify({"status": "Record Inserted"})


@app.route('/data')
def data():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM example_table")
    records = cursor.fetchall()
    connection.close()
    return jsonify(records)

# UI route


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
