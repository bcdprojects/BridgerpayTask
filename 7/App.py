from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL


# initializations
app = Flask(__name__)

server_url = 'http://quickstart-kb-http:9200'
service_name = 'BridgerpayFlask'
environment = 'dev'

apm = ElasticAPM(app, server_url=server_url, service_name=service_name, environment=environment)

# Mysql Connection
app.config['MYSQL_HOST'] = 'localhost' 
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'CDcd1212121'
app.config['MYSQL_DB'] = 'bcdexedbbcd'
mysql = MySQL(app)

# initialize using environment variables
from elasticapm.contrib.flask import ElasticAPM
app = Flask(__name__)
apm = ElasticAPM(app)



apm = ElasticAPM(app)

# routes
@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM bridgerpaytable')
    data = cur.fetchall()
    cur.close()
    return render_template('index.html', bridgerpaytable = data)

@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        current_datetime = request.form['current_datetime']
        email = request.form['email']
        comment = request.form['comment']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO bridgerpaytable (current_datetime, email,comment) VALUES (%s,%s,%s)", (current_datetime, email,comment))
        mysql.connection.commit()
        flash('Contact Added successfully')
        return redirect(url_for('Index'))

@app.route('/delete/<ind:id>', methods = ['POST','GET'])
def delete_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM bridgerpaytable WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Contact Removed Successfully')
    return redirect(url_for('Index'))

# starting the app
if __name__ == "__main__":
    app.run(port=3000, debug=True)
