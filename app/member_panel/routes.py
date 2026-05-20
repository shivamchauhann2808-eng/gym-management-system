from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.utils.decorators import member_required

member_panel_bp = Blueprint('member_panel', __name__)

@member_panel_bp.route('/profile')
@login_required
@member_required
def profile():
    # Grab the linked Member profile for the current logged-in member
    member = current_user.member_profile
    if not member:
        flash("Profile not found. Please contact the Gym Administrator.", "danger")
        return redirect(url_for('auth.logout'))
        
    # Sync and verify expired member status dynamically upon profile load
    member.check_and_update_status
    
    return render_template(
        'member_panel/profile.html',
        title='My Gym Membership',
        member=member
    )
