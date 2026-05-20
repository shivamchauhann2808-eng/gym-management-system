from app import db
from datetime import datetime, date

class Member(db.Model):
    __tablename__ = 'members'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), unique=True, nullable=True)
    
    # Member Profile Fields
    full_name = db.Column(db.String(100), nullable=False)
    profile_photo = db.Column(db.String(200), nullable=True)  # Filename in static/uploads
    gender = db.Column(db.String(20), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    address = db.Column(db.Text, nullable=True)
    
    # Subscription Fields
    plan_id = db.Column(db.Integer, db.ForeignKey('membership_plans.id'), nullable=False)
    join_date = db.Column(db.Date, nullable=False, default=date.today)
    expiry_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='Active')  # 'Active', 'Expired', 'Pending'
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = db.relationship('User', back_populates='member_profile')
    plan = db.relationship('MembershipPlan', back_populates='members')

    @property
    def check_and_update_status(self):
        """
        Helper method to check if membership has expired relative to current date,
        updating the database status flag dynamically if necessary.
        """
        today = date.today()
        if today > self.expiry_date:
            if self.status != 'Expired':
                self.status = 'Expired'
                db.session.commit()
            return 'Expired'
        elif self.status == 'Expired' and today <= self.expiry_date:
            self.status = 'Active'
            db.session.commit()
            return 'Active'
        return self.status

    def __repr__(self):
        return f"<Member {self.full_name} ({self.status})>"
