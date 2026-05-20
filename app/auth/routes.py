from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from app.models.user import User
from app.auth.forms import LoginForm
from urllib.parse import urlsplit

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    # If already logged in, send them to their dashboard/profile
    if current_user.is_authenticated:
        if current_user.role == 'admin':
            return redirect(url_for('dashboard.index'))
        else:
            return redirect(url_for('member_panel.profile'))
            
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower().strip()).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password.', 'danger')
            return render_template('auth/login.html', title='Sign In', form=form)
            
        login_user(user, remember=form.remember.data)
        flash(f'Welcome back, {user.email}!', 'success')
        
        # Redirection post-login to requested protected page if present
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            if user.role == 'admin':
                next_page = url_for('dashboard.index')
            else:
                next_page = url_for('member_panel.profile')
        return redirect(next_page)
        
    return render_template('auth/login.html', title='Sign In', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))
