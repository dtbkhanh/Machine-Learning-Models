# Semi-automatic Risk Analytics UI
An interactive UI is built so that users can engage with it. Each time, a pair of two companies is shown along with their information (company names, revenues, etc.), asking the user to choose which one is better. The human interaction on the UI is then captured and stored in a Database. 

## 🖥️ Python framework for Web application:
The application is built using Python frameworks of Dash and Flask. 

### 🛠️ Flask-SQLAlchemy
Flask-SQLAlchemy is used to connect Flask to a database (MySQL).
#### Declaring models:
```
class ActionCapture(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    button1_click = db.Column(db.Integer)
    button2_click = db.Column(db.Integer)
    timestamp= db.Column(db.DateTime, nullable=False)
```
* The class `Model` is a declarative base used to declare models.
* Use `Column` to define columns and assign them names.

#### Update MySQL data in Dash app:
* Whenever user clicks on the button, the action to store values into Database will be triggered:
```
db.session.add()
db.session.commit()
```
with `timestamp = datetime.datetime.now())`, the corresponding button-click column will get the value 1 and the other button-click columns will get 0. For example, button 1 is clicked, then `button1_click` = 1, the rest is 0.
* The class `ActionCapture` is used to define the table to be create in database. If such table already exists in the database, the records will be written inside. If not, the initial database is created using `db.create_all()`.
    * `SQLAlchemy.create_all()` and `SQLAlchemy.drop_all()` methods are used to create and drop tables according to the models.
* Accessing the data in database using `db.session.query().all()`


## ⚙️ Setting up a local MySQL Database:
0. Open Terminal
1. Start a MySQL server instance: with docker container name `Khanh_mysql`:
```
docker run --name Khanh_mysql  -p 3306:3306 -e MYSQL_ROOT_PASSWORD=helloworld -d mysql:8.0.19
```

2. Connect to MySQL Docker Container (start a MySQL client inside the container):
```
docker exec -it Khanh_mysql -uroot -p
```
or: `sudo mysql -uroot -p`

3. Create a new Database inside MySQL:
```
mysql> CREATE DATABASE KhanhDB;
mysql> SHOW CREATE DATABASE KhanhDB;
mysql> DESCRIBE KhanhDB;
mysql> USE KhanhDB;
```
Type `\q` or `exit` to quit MySQL.


## 🚀 Executing the App:
### How to run a Web app on development server using Visual Studio Code:

1. Create a virtual environment: `virtualenv -p python3 env`

2. Activate the virtual environment: `source env/bin/activate`

2.1. Run `pip install -r requirements.txt`

3. Run the Python  _*.py_ file: `python ~/.../testUI.py` 

4. Open the browser and go to `http://127.0.0.1:8050/` to see the result

### Viewing the records inside MySQL Database: 
```
mysql> SELECT * FROM KhanhDB.action_capture;

```

## 🛠️ Local Development
### Executing mysql database using docker-compose
```.env
docker-compose up mysql
```
