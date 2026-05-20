from flask import Blueprint, render_template, jsonify
from flask_login import login_required
from app.models.member import Member
from app.models.plan import MembershipPlan
from app.utils.decorators import admin_required
from datetime import datetime, timedelta, date
from collections import OrderedDict
from sqlalchemy import func

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
@login_required
@admin_required
def index():
    # Sync and verify expired member statuses dynamically upon dashboard load
    all_members = Member.query.all()
    for member in all_members:
        member.check_and_update_status

    # Recalculate stats after dynamic update
    total_members = Member.query.count()
    active_members = Member.query.filter_by(status='Active').count()
    expired_members = Member.query.filter_by(status='Expired').count()
    pending_members = Member.query.filter_by(status='Pending').count()
    
    # Calculate Monthly Revenue (sum of normalized monthly revenue of all active memberships)
    # e.g., Plan Price / Plan Duration (Months) for active members
    active_subscriptions = Member.query.filter_by(status='Active').all()
    monthly_revenue = 0.0
    for sub in active_subscriptions:
        plan = sub.plan
        duration = plan.duration_months if plan.duration_months > 0 else 1
        monthly_revenue += float(plan.price) / duration
        
    # Get 5 recent member registrations
    recent_registrations = Member.query.order_by(Member.join_date.desc(), Member.created_at.desc()).limit(5).all()

    # Prepopulate monthly registration counts over the last 6 months for chart display
    today = date.today()
    months_labels = []
    reg_counts = []
    
    # Generate last 6 months
    for i in range(5, -1, -1):
        # Calculate month date boundaries
        # Go back 'i' months
        year = today.year
        month = today.month - i
        if month <= 0:
            month += 12
            year -= 1
        
        month_start = date(year, month, 1)
        if month == 12:
            month_end = date(year + 1, 1, 1) - timedelta(days=1)
        else:
            month_end = date(year, month + 1, 1) - timedelta(days=1)
            
        month_label = month_start.strftime("%b %Y")
        count = Member.query.filter(Member.join_date >= month_start, Member.join_date <= month_end).count()
        
        months_labels.append(month_label)
        reg_counts.append(count)

    # Membership plans distribution stats for plans breakdown
    plans_distribution = {}
    plans = MembershipPlan.query.all()
    for p in plans:
        plans_distribution[p.name] = Member.query.filter_by(plan_id=p.id, status='Active').count()

    return render_template(
        'dashboard/index.html',
        title='Admin Dashboard',
        total_members=total_members,
        active_members=active_members,
        expired_members=expired_members,
        pending_members=pending_members,
        monthly_revenue=round(monthly_revenue, 2),
        recent_registrations=recent_registrations,
        months_labels=months_labels,
        reg_counts=reg_counts,
        plans_distribution=plans_distribution
    )
