from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
from models import db, Supply, Counterparty, User
from forms import RegistrationForm, LoginForm
from flask_login import LoginManager, UserMixin, current_user, login_required, logout_user, login_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate

app = Flask(__name__)

# Настройки для базы данных
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '1111'

migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

db.init_app(app)

def create_tables():
    db.create_all()  # Создание таблиц

# Главная страница
@app.route('/')
def home():
    return render_template('home.html', active_page='home')

# Страница Supplies
@app.route('/supplies')
def supplies():
    return render_template('supplies.html', active_page='supplies')

# Страница Counterparties
@app.route('/counterparties')
def counterparties():
    return render_template('counterparty.html', active_page='counterparties')

@app.route('/reports')
def reports():
    return render_template('reports.html', actice_page='repoerts')


# --- CRUD для модели Supply ---
# 1. Create (создать запись)
@app.route('/supplies', methods=['POST'])
def create_supply():
    data = request.json  # Получаем данные из тела запроса
    new_supply = Supply(
        ID_data_about_order=data['ID_data_about_order'],
        ID_rank_catalogue=data['ID_rank_catalogue'],
        ID_counterparty=data['ID_counterparty'],
        Date_receiving_actual=data['Date_receiving_actual'],
        Amount_receiving_actual=data['Amount_receiving_actual'],
        Refund_amount=data.get('Refund_amount')  # Необязательное поле
    )
    db.session.add(new_supply)
    db.session.commit()
    return jsonify({'message': 'Supply created successfully'}), 201

# 2. Read (получить все записи)
@app.route('/supplies', methods=['GET'])
def get_supplies():
    supplies = Supply.query.all()
    supplies_list = [
        {
            'ID_supply': s.ID_supply,
            'ID_data_about_order': s.ID_data_about_order,
            'ID_rank_catalogue': s.ID_rank_catalogue,
            'ID_counterparty': s.ID_counterparty,
            'Date_receiving_actual': s.Date_receiving_actual,
            'Amount_receiving_actual': s.Amount_receiving_actual,
            'Refund_amount': s.Refund_amount
        } for s in supplies
    ]
    return jsonify(supplies_list)

# 3. Update (обновить запись)
@app.route('/supplies/<int:supply_id>', methods=['PUT'])
def update_supply(supply_id):
    data = request.json
    supply = Supply.query.get(supply_id)
    if not supply:
        return jsonify({'message': 'Supply not found'}), 404

    # Обновляем данные
    supply.ID_data_about_order = data['ID_data_about_order']
    supply.ID_rank_catalogue = data['ID_rank_catalogue']
    supply.ID_counterparty = data['ID_counterparty']
    supply.Date_receiving_actual = data['Date_receiving_actual']
    supply.Amount_receiving_actual = data['Amount_receiving_actual']
    supply.Refund_amount = data.get('Refund_amount')

    db.session.commit()
    return jsonify({'message': 'Supply updated successfully'})

# 4. Delete (удалить запись)
@app.route('/supplies/<int:supply_id>', methods=['DELETE'])
def delete_supply(supply_id):
    supply = Supply.query.get(supply_id)
    if not supply:
        return jsonify({'message': 'Supply not found'}), 404

    db.session.delete(supply)
    db.session.commit()
    return jsonify({'message': 'Supply deleted successfully'})

# --- Аналогично можно реализовать CRUD для других моделей ---
# Например, Counterparty
@app.route('/counterparties', methods=['POST'])
def create_counterparty():
    data = request.json
    new_counterparty = Counterparty(
        Name=data['Name'],
        Lisensis=data['Lisensis'],
        ID_country=data['ID_country'],
        Phone=data['Phone'],
        E_mail=data['E_mail'],
        BR_assessment=data['BR_assessment'],
        IM_assessment=data['IM_assessment']
    )
    db.session.add(new_counterparty)
    db.session.commit()
    return jsonify({'message': 'Counterparty created successfully'}), 201

# Регистрация\авторизация
@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Аккаунт создан для {form.username.data}!', 'success')
        new_user = User(username=form.username.data, email=form.email.data,
                password=generate_password_hash(form.password.data))
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    user = User.query.filter_by(email=form.email.data).first()
    if user and check_password_hash(user.password, form.password.data):
        login_user(user)
        flash('Вход выполнен!', 'success')
        return redirect(url_for('home'))
    else:
        flash('Неверный email или пароль', 'danger')

@app.route("/logout")
def logout():
    logout_user()
    flash('Вы вышли из системы!', 'info')
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
