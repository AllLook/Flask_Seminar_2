from flask import Flask
from flask import render_template, url_for, request, redirect, make_response, session, flash
from key_session_flash import key_flash
from markupsafe import escape

app = Flask(__name__)
app.secret_key = b'9baca58065dd677db6910def5ee0940550d80c249d54d72ee42e9aa653dca417'


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
    if request.method == 'POST':
        name = request.form.get('name')
        # email = request.form.get('email')
        session['user_data'] = request.form.get('user', 'email')

        flash('Вы  уже успешно вошли!', 'success')  # если уже есть авторизация
        # response = make_response('Успешная авторизация')#Так не устанавливаются
        # response.set_cookie('name', 'email' )
        return redirect(url_for('redirect_hello', name=name))  # сюда вернуть response=response через запятую
    return render_template('form.html')


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
