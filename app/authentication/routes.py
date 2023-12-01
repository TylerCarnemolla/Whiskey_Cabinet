from forms import UserLoginForm

from models import User, db, check_password_hash

from flask import Blueprint, render_template, request, redirect, url_for, flash

from flask_login import login_user, logout_user, LoginManager, current_user, login_required

auth = Blueprint('auth', __name__, template_folder = 'auth_templates') 
@auth.route('/signup', methods = ['GET', 'POST']) 

def signup():
    form = UserLoginForm()   

    try:  
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            password = form.password.data 
            print(email, password)
            Collector = User(email, password = password)
            

            db.session.add(Collector) 
            db.session.commit()

            flash(f'You have successfully created a Collector account {email}', 'Collector-created')
            return redirect(url_for('site.home')) 
    except:
        raise Exception('Invalid form data: Please check your form.')
    return render_template('sign_up.html', form=form) 


@auth.route('/signin', methods = ['GET', 'POST'])

def signin():
    form = UserLoginForm()

    try:  
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            password = form.password.data 
            print(email, password)
            
            logged_user = User.query.filter(User.email == email).first() 
            if logged_user and check_password_hash(logged_user.password, password):
                
                login_user(logged_user)
                flash('You successfully signed in.')
                return redirect(url_for('site.profile'))
            else:
                flash(f"You have failed to get in, you must not be an employee.")
    except:
        raise Exception ('Somthing went wrong, please check your sign in information')
    return render_template('sign_in.html', form = form)
            

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('site.home'))