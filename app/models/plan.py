from app import db
from datetime import datetime

class MembershipPlan(db.Model):
    __tablename__ = 'membership_plans'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    duration_months = db.Column(db.Integer, nullable=False)  # 1 for Monthly, 3 for Quarterly, 12 for Yearly
    price = db.Column(db.Numeric(10, 2), nullable=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    # Back-reference to all members subscribing to this plan. Prevent cascade delete issues.
    members = db.relationship('Member', back_populates='plan', lazy='dynamic')

    def __repr__(self):
        return f"<MembershipPlan {self.name} - ${self.price}>"
