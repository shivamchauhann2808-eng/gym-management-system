from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from app import db
from app.models.plan import MembershipPlan
from app.plans.forms import PlanForm
from app.utils.decorators import admin_required

plans_bp = Blueprint('plans', __name__)

@plans_bp.route('/', methods=['GET'])
@login_required
@admin_required
def index():
    plans = MembershipPlan.query.order_by(MembershipPlan.price.asc()).all()
    return render_template('plans/list.html', title='Membership Plans', plans=plans)

@plans_bp.route('/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create():
    form = PlanForm()
    if form.validate_on_submit():
        new_plan = MembershipPlan(
            name=form.name.data.strip(),
            duration_months=form.duration_months.data,
            price=form.price.data
        )
        db.session.add(new_plan)
        db.session.commit()
        flash(f"Membership plan '{new_plan.name}' has been created successfully!", "success")
        return redirect(url_for('plans.index'))
    return render_template('plans/form.html', title='Create Plan', form=form)

@plans_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit(id):
    plan = MembershipPlan.query.get_or_404(id)
    form = PlanForm()
    
    if request.method == 'GET':
        form.name.data = plan.name
        form.duration_months.data = plan.duration_months
        form.price.data = plan.price
        
    if form.validate_on_submit():
        plan.name = form.name.data.strip()
        plan.duration_months = form.duration_months.data
        plan.price = form.price.data
        db.session.commit()
        flash(f"Membership plan '{plan.name}' has been successfully updated!", "success")
        return redirect(url_for('plans.index'))
        
    return render_template('plans/form.html', title=f"Edit {plan.name}", form=form, plan=plan)

@plans_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
@admin_required
def delete(id):
    plan = MembershipPlan.query.get_or_404(id)
    
    # Integrity check: Ensure no members are currently active or pending under this plan
    active_member_count = plan.members.count()
    if active_member_count > 0:
        flash(f"Cannot delete plan '{plan.name}' because {active_member_count} member(s) are currently subscribed to it. Please re-assign those members to other plans first.", "danger")
        return redirect(url_for('plans.index'))
        
    name = plan.name
    db.session.delete(plan)
    db.session.commit()
    flash(f"Membership plan '{name}' has been deleted successfully.", "success")
    return redirect(url_for('plans.index'))
