import os
import uuid
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required
from app import db
from app.models.member import Member
from app.models.user import User
from app.models.plan import MembershipPlan
from app.members.forms import MemberForm
from app.utils.decorators import admin_required
from datetime import date, timedelta
from werkzeug.utils import secure_filename

members_bp = Blueprint('members', __name__)

def add_months(start_date, months):
    """
    Safely adds calendar months to a start date, accounting for variable month
    durations and leap years. Pure Python implementation.
    """
    month = start_date.month - 1 + months
    year = start_date.year + month // 12
    month = month % 12 + 1
    # Max days per month
    month_days = [31, 29 if (year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)) else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    day = min(start_date.day, month_days[month - 1])
    return date(year, month, day)

def save_profile_photo(form_photo):
    """
    Saves a profile photo with a unique UUID filename to avoid name collisions,
    returning the safe filename relative to the upload folder.
    """
    if not form_photo:
        return None
        
    filename = secure_filename(form_photo.filename)
    # Generate unique UUID filename while preserving extension
    ext = os.path.splitext(filename)[1].lower()
    unique_filename = f"{uuid.uuid4().hex}{ext}"
    
    upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
    form_photo.save(upload_path)
    return unique_filename

def delete_profile_photo(filename):
    """
    Deletes an old profile photo file from disk if it exists.
    """
    if not filename:
        return
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
        except Exception as e:
            current_app.logger.error(f"Failed to delete old photo: {file_path}. Error: {str(e)}")

@members_bp.route('/', methods=['GET'])
@login_required
@admin_required
def index():
    # Sync member statuses
    for member in Member.query.all():
        member.check_and_update_status

    search_query = request.args.get('search', '').strip()
    page = request.args.get('page', 1, type=int)
    per_page = 10

    # Build base query
    query = Member.query

    if search_query:
        # Search by name, email, or phone
        query = query.filter(
            (Member.full_name.ilike(f'%{search_query}%')) |
            (Member.email.ilike(f'%{search_query}%')) |
            (Member.phone.ilike(f'%{search_query}%'))
        )

    # Paginate
    pagination = query.order_by(Member.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    members = pagination.items

    return render_template(
        'members/list.html',
        title='Members Directory',
        members=members,
        pagination=pagination,
        search_query=search_query
    )

@members_bp.route('/view/<int:id>', methods=['GET'])
@login_required
@admin_required
def view(id):
    member = Member.query.get_or_404(id)
    # Perform a dynamic sync check
    member.check_and_update_status
    return render_template('members/view.html', title=f"{member.full_name}'s Profile", member=member)

@members_bp.route('/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create():
    form = MemberForm()
    
    # Populate plans choice dynamically
    plans = MembershipPlan.query.all()
    form.plan_id.choices = [(p.id, f"{p.name} (${p.price:.2f})") for p in plans]
    
    if form.validate_on_submit():
        email = form.email.data.lower().strip()
        
        # Check if email is already taken in Users table
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash(f'An account with email {email} already exists.', 'danger')
            return render_template('members/create.html', title='Register New Member', form=form)
            
        # Get selected plan to compute expiry date
        plan = MembershipPlan.query.get(form.plan_id.data)
        if not plan:
            flash('Invalid plan selected.', 'danger')
            return render_template('members/create.html', title='Register New Member', form=form)
            
        # Automatically calculate Expiry Date based on duration
        expiry_date = add_months(form.join_date.data, plan.duration_months)
        
        # Setup the User credentials for Member panel login
        new_user = User(email=email, role='member')
        # Admin can provide a custom password or it defaults to member123
        member_password = form.password.data if form.password.data else "member123"
        new_user.set_password(member_password)
        
        db.session.add(new_user)
        db.session.flush() # Flush to get new_user.id
        
        # Save photo if uploaded
        photo_filename = None
        if form.profile_photo.data:
            photo_filename = save_profile_photo(form.profile_photo.data)
            
        # Save the Member profile
        new_member = Member(
            user_id=new_user.id,
            full_name=form.full_name.data.strip(),
            profile_photo=photo_filename,
            gender=form.gender.data,
            dob=form.dob.data,
            phone=form.phone.data.strip(),
            email=email,
            address=form.address.data.strip() if form.address.data else None,
            plan_id=plan.id,
            join_date=form.join_date.data,
            expiry_date=expiry_date,
            status=form.status.data
        )
        
        db.session.add(new_member)
        db.session.commit()
        
        flash(f"Member '{new_member.full_name}' has been successfully registered!", "success")
        return redirect(url_for('members.index'))
        
    return render_template('members/create.html', title='Register New Member', form=form)

@members_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit(id):
    member = Member.query.get_or_404(id)
    form = MemberForm()
    
    # Populate plan choices
    plans = MembershipPlan.query.all()
    form.plan_id.choices = [(p.id, f"{p.name} (${p.price:.2f})") for p in plans]
    
    if request.method == 'GET':
        # Prepopulate form with member values
        form.full_name.data = member.full_name
        form.gender.data = member.gender
        form.dob.data = member.dob
        form.phone.data = member.phone
        form.email.data = member.email
        form.address.data = member.address
        form.plan_id.data = member.plan_id
        form.join_date.data = member.join_date
        form.status.data = member.status
        
    if form.validate_on_submit():
        new_email = form.email.data.lower().strip()
        
        # Verify email uniqueness if email is changed
        if new_email != member.email:
            existing_user = User.query.filter_by(email=new_email).first()
            if existing_user and existing_user.id != member.user_id:
                flash(f'An account with email {new_email} already exists.', 'danger')
                return render_template('members/edit.html', title='Edit Member Profile', form=form, member=member)
        
        # Determine if plan has changed to recalculate expiry date
        plan_changed = (form.plan_id.data != member.plan_id) or (form.join_date.data != member.join_date)
        plan = MembershipPlan.query.get(form.plan_id.data)
        
        # Update credentials
        user = User.query.get(member.user_id)
        if user:
            user.email = new_email
            if form.password.data:
                user.set_password(form.password.data)
                
        # Update details
        member.full_name = form.full_name.data.strip()
        member.gender = form.gender.data
        member.dob = form.dob.data
        member.phone = form.phone.data.strip()
        member.email = new_email
        member.address = form.address.data.strip() if form.address.data else None
        member.plan_id = plan.id
        member.join_date = form.join_date.data
        member.status = form.status.data
        
        if plan_changed:
            member.expiry_date = add_months(form.join_date.data, plan.duration_months)
            
        # Handle profile image update
        if form.profile_photo.data:
            # Delete the old picture to prevent file bloating
            if member.profile_photo:
                delete_profile_photo(member.profile_photo)
            member.profile_photo = save_profile_photo(form.profile_photo.data)
            
        db.session.commit()
        flash(f"Profile for '{member.full_name}' was successfully updated!", "success")
        return redirect(url_for('members.view', id=member.id))
        
    return render_template('members/edit.html', title='Edit Member Profile', form=form, member=member)

@members_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
@admin_required
def delete(id):
    member = Member.query.get_or_404(id)
    name = member.full_name
    
    # 1. Delete associated profile photo file from system
    if member.profile_photo:
        delete_profile_photo(member.profile_photo)
        
    # 2. Grab the User account to delete it cleanly (will trigger cascade or handled manually)
    user = User.query.get(member.user_id)
    
    db.session.delete(member)
    if user:
        db.session.delete(user)
        
    db.session.commit()
    flash(f"Member '{name}' has been successfully deleted.", "success")
    return redirect(url_for('members.index'))
