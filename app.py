from flask import Flask
from flask import render_template, url_for, request, redirect, session, flash
from markupsafe import escape
from flask_wtf import CSRFProtect
from Flask_Seminar_2.user_model import User, db

from Flask_Seminar_2.login_form import LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = b'9baca58065dd677db6910def5ee0940550d80c249d54d72ee42e9aa653dca417'
csrf = CSRFProtect(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user_data_base.db'
db.init_app(app)

context_user_dict = {}


@app.route(escape('/'))
def home():  # put application's code here
    return render_template('base.html')


@app.route('/hello/<name>')
def redirect_hello(name):
    return render_template('button_exit.html', name=name)


@app.route(escape('/outerwear/'))
def outerwear():
    jackets = {'Black': 'Size 48: black jackets', 'Blue': 'Size 50: blue jackets', 'Yellow': 'Size 52: yellow jackets',
               'White': 'Size 54: white jackets'}
    return render_template('outerwear.html', jackets=jackets)


@app.route(escape('/Summer/'))
def summer():
    clothing = {'Black': 'Size 48: black T-shirt', 'Blue': 'Size 50: blue T-shirt', 'Yellow': 'Size 52: yellow shorts',
                'White': 'Size 54: white shorts'}
    return render_template('Summer.html', clothing=clothing)


@app.route(escape('/dresses/'))
def dresses():
    dres = {'Black': 'Size 48: black dresses', 'Blue': 'Size 50: blue dresses', 'Yellow': 'Size 52: yellow dresses',
            'White': 'Size 54: white dresses'}
    return render_template('dresses.html', dres=dres)


@app.route(escape("/user_form/"), methods=['GET', 'POST'])
def user_form():
    form = LoginForm()
    if request.method == 'POST':
        name = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        if name not in context_user_dict:
            context_user_dict[name] = email
            print(context_user_dict)

            session['user_data'] = request.form.get('user', 'email')
            user = User(username=name, email=email, password=hash(password))
            db.create_all()
            db.session.add(user)
            db.session.commit()

            flash('Вы  уже успешно вошли!', 'success')  # если уже есть авторизация
            # response = make_response('Успешная авторизация')#Так не устанавливаются
            # response.set_cookie('name', 'email' )
            return redirect(url_for('redirect_hello', name=name))  # сюда вернуть response=response через запятую
        else:
            return render_template('form.html', form=form)
    return render_template('form.html', form=form)


@app.route(escape('/exit/'))
def cookie_exit():
    # session.pop('name', None) #так не удаляются из браузера
    # session.pop('email', None)
    # session.pop('user_name', None)
    session.clear()
    return redirect(url_for('user_form'))


@app.errorhandler(404)
def page_not_found(e):
    app.logger.warning(e)
    context = {
        'url': request.base_url
    }
    return render_template('404.html', context=context)


if __name__ == '__main__':
    app.run(debug=True)
