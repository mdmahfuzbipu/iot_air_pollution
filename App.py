from flask import Flask, render_template,request,redirect,url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'air pollution monitoring system'

mysql = MySQL(app)

@app.route('/')
def Index():
    return render_template('index.html')


@app.route('/insert', methods = ['POST'])
def insert():

    if request.method == "POST":
        date_time = request.form['date_time']
        location = request.form['location']
        temperature = request.form['temperature']
        relative_humidity = request.form['relative_humidity']
        atmospheric_pressure = request.form['atmospheric_pressure']
        altitude = request.form['altitude']
        co_concentration = request.form['co_concentration']
        ch4_concentration = request.form['ch4_concentration']
        smoke_concentration = request.form['smoke_concentration']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO air_pollution_data(date_time,location,temperature,relative_humidity,atmospheric_pressure,altitude,co_concentration,ch4_concentration,smoke_concentration) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)",(date_time,location,temperature,relative_humidity,atmospheric_pressure,altitude,co_concentration,ch4_concentration,smoke_concentration))
        mysql.connection.commit()
        cur.execute("SELECT LAST_INSERT_ID()")
        row_id = cur.fetchone()[0]
        return redirect(url_for('show', id=row_id))

    
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    cur = mysql.connection.cursor()

    # Handle form submission
    if request.method == 'POST':
        date_time = request.form['date_time']
        location = request.form['location']
        temperature = request.form['temperature']
        relative_humidity = request.form['relative_humidity']
        atmospheric_pressure = request.form['atmospheric_pressure']
        altitude = request.form['altitude']
        co_concentration = request.form['co_concentration']
        ch4_concentration = request.form['ch4_concentration']
        smoke_concentration = request.form['smoke_concentration']

        cur.execute("UPDATE air_pollution_data SET date_time=%s, location=%s, temperature=%s, relative_humidity=%s, atmospheric_pressure=%s, altitude=%s, co_concentration=%s, ch4_concentration=%s, smoke_concentration=%s WHERE id=%s", (date_time, location, temperature, relative_humidity, atmospheric_pressure, altitude, co_concentration, ch4_concentration, smoke_concentration, id))
        mysql.connection.commit()

        return redirect(url_for('show', id=id))

    cur.execute("SELECT * FROM air_pollution_data WHERE id=%s", [id])
    data = cur.fetchone()
    return render_template('edit.html', data=data)

   

@app.route('/delete/<string:id>', methods = ['GET'])
def delete(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM air_pollution_data WHERE id = %s", [id])
    mysql.connection.commit()
    return redirect(url_for('Index'))

@app.route('/show/<int:id>')
def show(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM air_pollution_data WHERE id = %s", [id])
    data = cur.fetchone()
    return render_template('show.html', data=data)

if __name__ == "__main__":
    app.run(debug=True)
