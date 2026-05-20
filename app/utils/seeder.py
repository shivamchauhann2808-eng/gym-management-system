import os
from datetime import date, timedelta
from app.models.user import User
from app.models.plan import MembershipPlan
from app.models.member import Member

def seed_database_if_empty(db):
    # Check if we already have users or plans
    try:
        if User.query.first() is not None or MembershipPlan.query.first() is not None:
            print("Database already seeded. Skipping auto-seeding.")
            return # Database is already populated
    except Exception as e:
        print(f"Checking tables failed: {e}. Attempting table creation...")

    print("Running db.create_all() to ensure all tables exist...")
    db.create_all()

    # Re-verify if data exists now that tables are created
    try:
        if User.query.first() is not None or MembershipPlan.query.first() is not None:
            print("Database already has records. Skipping seeding.")
            return
    except Exception as e:
        print(f"Error checking tables after creation: {e}")
        return

    print("Database is empty. Running auto-seeding...")
    
    # 1. Seed Membership Plans
    monthly = MembershipPlan(name="Monthly Standard", duration_months=1, price=49.99)
    quarterly = MembershipPlan(name="Quarterly Fit", duration_months=3, price=129.99)
    yearly = MembershipPlan(name="Yearly Iron Pro", duration_months=12, price=449.99)
    
    db.session.add_all([monthly, quarterly, yearly])
    db.session.commit()
    print("Membership plans seeded successfully.")
    
    # 2. Seed Default Super Admin
    admin = User(email="admin@gym.com", role="admin")
    admin.set_password("admin123")
    db.session.add(admin)
    db.session.commit()
    print("Default Super Admin account created: admin@gym.com / admin123")
    
    # 3. Seed Mock Gym Members (10 profiles)
    today = date.today()
    
    # Helper to calculate expiry date safely
    def calc_expiry(start_date, duration_months):
        month = start_date.month - 1 + duration_months
        year = start_date.year + month // 12
        month = month % 12 + 1
        month_days = [31, 29 if (year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)) else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        day = min(start_date.day, month_days[month - 1])
        return date(year, month, day)

    # Diverse array of mock members
    members_data = [
        {
            "full_name": "Marcus Aurelius",
            "email": "marcus@gym.com",
            "gender": "Male",
            "dob": date(1990, 4, 26),
            "phone": "+1 (555) 012-3456",
            "address": "12 Imperial Way, Rome, NY",
            "plan": monthly,
            "months_ago": 0, # Joined today, active
            "status": "Active"
        },
        {
            "full_name": "Serena Williams",
            "email": "serena@gym.com",
            "gender": "Female",
            "dob": date(1981, 9, 26),
            "phone": "+1 (555) 019-8765",
            "address": "45 Court Side Drive, Florida, FL",
            "plan": yearly,
            "months_ago": 2, # Joined 2 months ago, active
            "status": "Active"
        },
        {
            "full_name": "Arnold Schwarzenegger",
            "email": "arnold@gym.com",
            "gender": "Male",
            "dob": date(1947, 7, 30),
            "phone": "+1 (555) 013-8822",
            "address": "88 Muscle Beach Way, Venice, CA",
            "plan": yearly,
            "months_ago": 11, # Joined 11 months ago (expires in 1 mo), active
            "status": "Active"
        },
        {
            "full_name": "Jane Fonda",
            "email": "jane@gym.com",
            "gender": "Female",
            "dob": date(1937, 12, 21),
            "phone": "+1 (555) 015-7733",
            "address": "55 Aerobics Lane, Los Angeles, CA",
            "plan": monthly,
            "months_ago": 3, # Joined 3 months ago (expired since 1-mo plan), expired
            "status": "Expired"
        },
        {
            "full_name": "Usain Bolt",
            "email": "usain@gym.com",
            "gender": "Male",
            "dob": date(1986, 8, 21),
            "phone": "+1 (555) 019-9999",
            "address": "958 Lightning Lane, Kingston, NY",
            "plan": quarterly,
            "months_ago": 1, # Joined 1 month ago, active
            "status": "Active"
        },
        {
            "full_name": "Michael Phelps",
            "email": "michael@gym.com",
            "gender": "Male",
            "dob": date(1985, 6, 30),
            "phone": "+1 (555) 018-8888",
            "address": "28 Gold Medal Dr, Baltimore, MD",
            "plan": quarterly,
            "months_ago": 4, # Joined 4 months ago (expired since 3-mo plan), expired
            "status": "Expired"
        },
        {
            "full_name": "Clara Oswald",
            "email": "clara@gym.com",
            "gender": "Female",
            "dob": date(1992, 11, 23),
            "phone": "+1 (555) 011-2233",
            "address": "77 TARDIS Lane, London, OH",
            "plan": monthly,
            "months_ago": 0, # Joined today, pending/upcoming
            "status": "Pending"
        },
        {
            "full_name": "Rocky Balboa",
            "email": "rocky@gym.com",
            "gender": "Male",
            "dob": date(1946, 7, 6),
            "phone": "+1 (555) 010-1976",
            "address": "1818 Tusculum St, Philadelphia, PA",
            "plan": yearly,
            "months_ago": 5, # Joined 5 months ago, active
            "status": "Active"
        },
        {
            "full_name": "Diana Prince",
            "email": "diana@gym.com",
            "gender": "Female",
            "dob": date(1988, 3, 22),
            "phone": "+1 (555) 017-0077",
            "address": "1 Wonder St, Themyscira, VA",
            "plan": yearly,
            "months_ago": 1, # Joined 1 month ago, active
            "status": "Active"
        },
        {
            "full_name": "Bruce Wayne",
            "email": "bruce@gym.com",
            "gender": "Male",
            "dob": date(1985, 2, 19),
            "phone": "+1 (555) 012-9922",
            "address": "1007 Mountain Drive, Gotham, NJ",
            "plan": monthly,
            "months_ago": 2, # Joined 2 months ago (expired since 1-mo plan), expired
            "status": "Expired"
        }
    ]
    
    for index, m in enumerate(members_data, start=1):
        try:
            joined_year = today.year
            joined_month = today.month - m["months_ago"]
            if joined_month <= 0:
                joined_month += 12
                joined_year -= 1
            joined_date = date(joined_year, joined_month, min(today.day, 28))
            expiry_date = calc_expiry(joined_date, m["plan"].duration_months)
            
            user = User(email=m["email"], role="member")
            user.set_password("member123")
            db.session.add(user)
            db.session.flush() # Grab user.id
            
            member = Member(
                user_id=user.id,
                full_name=m["full_name"],
                profile_photo=None,
                gender=m["gender"],
                dob=m["dob"],
                phone=m["phone"],
                email=m["email"],
                address=m["address"],
                plan_id=m["plan"].id,
                join_date=joined_date,
                expiry_date=expiry_date,
                status=m["status"]
            )
            db.session.add(member)
        except Exception as member_err:
            print(f"Error seeding member {m['full_name']}: {member_err}")
            db.session.rollback()
            continue
        
    try:
        db.session.commit()
        print("Database successfully seeded with 10 mock members!")
    except Exception as commit_err:
        print(f"Failed to commit seeded database: {commit_err}")
        db.session.rollback()
