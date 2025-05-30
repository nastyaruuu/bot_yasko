from flask import Flask, render_template, url_for, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    speciality = db.Column(db.String, nullable=False)
    adress = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"Volunteer(id={self.id}, name='{self.name}', email='{self.email}', specialty='{self.specialty}')"

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']
        surname = request.form['surname']
        name = request.form['name']
        age = request.form['age']
        speciality = request.form['speciality']
        adress = request.form['adress']
        user = Users(login=login, password=password, surname=surname, name=name, age=age, speciality=speciality, adress=adress)
        try:
            db.session.add(user)
            db.session.commit()
            return redirect('/')
        except:
            return 'Произошла ошибка'
    else: 
        return render_template("index.html")
    
# Получение всех волонтеров
@app.route('/api/volunteers', methods=['GET'])
def get_volunteers():
    volunteers = Users.query.all()
    result = []
    for volunteer in volunteers:
        result.append({
            'id': volunteer.id,
            'email': volunteer.login,
            'surname': volunteer.surname,
            'name': volunteer.name,
            'age': volunteer.age, 
            'speciality': volunteer.speciality,
            'adress': volunteer.adress
        })
    return jsonify(result)

# Получение одного волонтера по ID
@app.route('/api/volunteers/<int:volunteer_id>', methods=['GET'])
def get_volunteer(volunteer_id):
    volunteer = Users.query.get(volunteer_id)
    if volunteer:
        return jsonify({
            'id': volunteer.id,
            'email': volunteer.login,
            'surname': volunteer.surname,
            'name': volunteer.name,
            'age': volunteer.age, 
            'speciality': volunteer.speciality,
            'adress': volunteer.adress
        })
    return jsonify({'message': 'Volunteer not found'})

# Добавление нового волонтера
@app.route('/api/volunteers/add', methods=['GET'])
def add_volunteer():
    data = request.json
    volunteer = Users(
        name=data['name'],
        login=data['login'],
        speciality=data['speciality'],
        password=data['password'],
        age=data['age'],
        adress=data['adress'], 
        surname=data['surname'],
    )
    db.session.add(volunteer)
    db.session.commit()
    return jsonify({'message': 'Volunteer added successfully'})

# Редактирование волонтера
@app.route('/api/volunteers/edit<int:volunteer_id>', methods=['PUT'])
def edit_volunteer(volunteer_id):
    volunteer = Users.query.get(volunteer_id)
    if volunteer:
        data = request.json
        volunteer.name = data['name']
        volunteer.login = data['login']
        volunteer.speciality = data['speciality']
        volunteer.password = data['password']
        volunteer.adress = data['adress']
        volunteer.age = data['age']
        volunteer.surname = data['surname']
        db.session.commit()
        return jsonify({'message': 'Volunteer updated successfully'})
    return jsonify({'message': 'Volunteer not found'})

# Удаление волонтера
@app.route('/api/volunteers/delete/<int:volunteer_id>', methods=['GET'])
def delete_volunteer(volunteer_id):
    volunteer = Users.query.get(volunteer_id)
    if volunteer:
        db.session.delete(volunteer)
        db.session.commit()
        return jsonify({'message': 'Volunteer deleted successfully'})
    return jsonify({'message': 'Volunteer not found'})

@app.route('/all')
def all():
    return render_template("all.html")

@app.route('/user-id')
def user():
    return render_template("user_id.html")

@app.route('/add-user')
def add_user():
    return render_template("add_user.html")

@app.route('/edit-user')
def edit_user():
    return render_template("edit_user.html")

@app.route('/delete-user')
def delete_user():
    return render_template("delete_user.html")

with app.app_context():
        db.create_all()
        app.run(debug=True, host='0.0.0.0', port=5005)