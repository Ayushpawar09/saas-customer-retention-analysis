# ============================================================
# FILE: generate_data.py
# PURPOSE: Generate realistic sample data for saas_analytics
# AUTHOR: Your Name
# DATE: 2024
# ============================================================

import random
import string
from datetime import datetime, timedelta, date
import psycopg2
from faker import Faker
import numpy as np

# Initialize Faker
fake = Faker()
Faker.seed(42)
random.seed(42)
np.random.seed(42)

# ============================================================
# DATABASE CONNECTION
# Change these settings to match your PostgreSQL setup
# ============================================================
DB_CONFIG = {
    'host': 'localhost',
    'database': 'saas_analytics',
    'user': 'postgres',
    'password': 'postgres123',   # Change this to YOUR password
    'port': '5432'
}

def connect_db():
    """Create database connection"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        print("✅ Connected to database successfully")
        return conn
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        raise

# ============================================================
# REFERENCE DATA
# ============================================================

INDUSTRIES = [
    'Technology', 'Finance', 'Healthcare', 'Retail', 
    'Manufacturing', 'Education', 'Real Estate', 
    'Consulting', 'Marketing', 'Logistics'
]

COMPANY_SIZES = ['Startup', 'SMB', 'Mid-Market', 'Enterprise']
COMPANY_SIZE_WEIGHTS = [0.25, 0.40, 0.25, 0.10]

SEGMENTS = ['Starter', 'Growth', 'Professional', 'Enterprise']
SEGMENT_WEIGHTS = [0.40, 0.30, 0.20, 0.10]

ACQUISITION_SOURCES = [
    'Organic Search', 'Paid Search', 'Referral', 
    'Partner', 'Event', 'Social Media', 'Email Campaign'
]
ACQUISITION_WEIGHTS = [0.25, 0.30, 0.20, 0.10, 0.05, 0.05, 0.05]

ACCOUNT_MANAGERS = [
    'Sarah Johnson', 'Michael Chen', 'Emma Rodriguez',
    'James Wilson', 'Priya Patel', 'David Kim',
    'Lisa Thompson', 'Robert Martinez'
]

COUNTRIES = ['USA', 'UK', 'Canada', 'Australia', 'Germany', 
             'France', 'Netherlands', 'India', 'Singapore']
COUNTRY_WEIGHTS = [0.45, 0.15, 0.10, 0.08, 0.06, 0.05, 0.04, 0.04, 0.03]

# Plan IDs and their prices (must match what you inserted)
PLAN_DATA = {
    'PLAN-001': {'tier': 'Starter',      'cycle': 'Monthly', 'price': 29.00},
    'PLAN-002': {'tier': 'Starter',      'cycle': 'Annual',  'price': 24.17},
    'PLAN-003': {'tier': 'Growth',       'cycle': 'Monthly', 'price': 79.00},
    'PLAN-004': {'tier': 'Growth',       'cycle': 'Annual',  'price': 65.83},
    'PLAN-005': {'tier': 'Professional', 'cycle': 'Monthly', 'price': 149.00},
    'PLAN-006': {'tier': 'Professional', 'cycle': 'Annual',  'price': 124.17},
    'PLAN-007': {'tier': 'Enterprise',   'cycle': 'Monthly', 'price': 399.00},
    'PLAN-008': {'tier': 'Enterprise',   'cycle': 'Annual',  'price': 332.50},
}

# Segment to plan mapping
SEGMENT_TO_PLANS = {
    'Starter':      ['PLAN-001', 'PLAN-002'],
    'Growth':       ['PLAN-003', 'PLAN-004'],
    'Professional': ['PLAN-005', 'PLAN-006'],
    'Enterprise':   ['PLAN-007', 'PLAN-008'],
}

CANCELLATION_REASONS = [
    'Price', 'Missing Features', 'Competitor', 
    'Business Closure', 'Low Usage', 'Poor Support'
]
CANCELLATION_WEIGHTS = [0.32, 0.22, 0.18, 0.08, 0.12, 0.08]

COMPETITORS = ['Asana', 'Monday.com', 'Jira', 'Notion', 
               'ClickUp', 'Trello', None, None]

FAILURE_REASONS = [
    'Insufficient Funds', 'Card Expired', 'Bank Declined',
    'Card Lost or Stolen', 'Invalid Card Number', 
    'Processing Error', 'Daily Limit Exceeded'
]

PAYMENT_METHODS = ['Credit Card', 'Debit Card', 'Bank Transfer', 'PayPal']
PAYMENT_METHOD_WEIGHTS = [0.55, 0.20, 0.15, 0.10]

TICKET_CATEGORIES = ['Billing', 'Technical', 'Feature Request', 
                     'Account', 'Onboarding', 'Integration']
TICKET_PRIORITIES = ['Low', 'Medium', 'High', 'Critical']
TICKET_STATUS_OPTIONS = ['Open', 'In Progress', 'Resolved', 'Closed', 'Escalated']
TICKET_CHANNELS = ['Email', 'Chat', 'Phone', 'Portal']

SUPPORT_AGENTS = [
    'Alex Turner', 'Maria Santos', 'Kevin Lee',
    'Sophie Brown', 'Daniel White', 'Natasha Green'
]

# ============================================================
# HELPER FUNCTIONS
# ============================================================

def random_date(start_date, end_date):
    """Generate a random date between two dates"""
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    return start_date + timedelta(days=random_days)

def generate_id(prefix, number, padding=6):
    """Generate formatted ID like CUST-000001"""
    return f"{prefix}-{str(number).zfill(padding)}"

def weighted_choice(options, weights):
    """Make a weighted random choice"""
    return random.choices(options, weights=weights, k=1)[0]

# ============================================================
# DATA GENERATION FUNCTIONS
# ============================================================

def generate_customers(num_customers=500):
    """Generate customer records"""
    print(f"\n📊 Generating {num_customers} customers...")
    customers = []
    
    start_date = date(2019, 1, 1)
    end_date = date(2023, 12, 31)
    
    for i in range(1, num_customers + 1):
        customer_id = generate_id('CUST', i)
        segment = weighted_choice(SEGMENTS, SEGMENT_WEIGHTS)
        company_size = weighted_choice(COMPANY_SIZES, COMPANY_SIZE_WEIGHTS)
        
        # Generate a signup date
        signup = random_date(start_date, end_date)
        
        # About 15% of customers are inactive (churned)
        is_active = random.random() > 0.15
        
        customer = {
            'customer_id': customer_id,
            'company_name': fake.company(),
            'industry': random.choice(INDUSTRIES),
            'company_size': company_size,
            'country': weighted_choice(COUNTRIES, COUNTRY_WEIGHTS),
            'city': fake.city(),
            'signup_date': signup,
            'acquisition_source': weighted_choice(ACQUISITION_SOURCES, ACQUISITION_WEIGHTS),
            'account_manager': random.choice(ACCOUNT_MANAGERS),
            'customer_segment': segment,
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'email': fake.unique.company_email(),
            'phone': fake.phone_number()[:20],
            'is_active': is_active,
        }
        customers.append(customer)
        
        if i % 100 == 0:
            print(f"  Generated {i}/{num_customers} customers...")
    
    print(f"  ✅ {num_customers} customers generated")
    return customers

def generate_subscriptions(customers):
    """Generate subscription records for each customer"""
    print(f"\n📊 Generating subscriptions...")
    subscriptions = []
    sub_counter = 1
    
    for customer in customers:
        customer_id = customer['customer_id']
        segment = customer['customer_segment']
        signup_date = customer['signup_date']
        is_active = customer['is_active']
        
        # Select initial plan based on segment
        plan_options = SEGMENT_TO_PLANS[segment]
        initial_plan_id = random.choice(plan_options)
        plan_price = PLAN_DATA[initial_plan_id]['price']
        
        # Calculate subscription dates
        sub_start = signup_date
        
        if is_active:
            # Active customer - subscription still running
            sub_status = random.choices(
                ['Active', 'Past Due', 'Trial'],
                weights=[0.85, 0.10, 0.05]
            )[0]
            cancelled_date = None
            end_date = None
            
            # Renewal date is next month or next year
            renewal_date = date.today() + timedelta(days=random.randint(1, 365))
            
            # Some active customers upgraded or downgraded
            flag = random.choices(
                ['New', 'Upgrade', 'Downgrade', 'No Change'],
                weights=[0.60, 0.20, 0.15, 0.05]
            )[0]
            
            if flag == 'Upgrade':
                # Try to upgrade to next tier
                if segment == 'Starter':
                    prev_plan = initial_plan_id
                    initial_plan_id = random.choice(SEGMENT_TO_PLANS['Growth'])
                elif segment == 'Growth':
                    prev_plan = initial_plan_id
                    initial_plan_id = random.choice(SEGMENT_TO_PLANS['Professional'])
                else:
                    flag = 'New'
                    prev_plan = None
            elif flag == 'Downgrade':
                prev_plan = initial_plan_id
                if segment == 'Enterprise':
                    initial_plan_id = random.choice(SEGMENT_TO_PLANS['Professional'])
                elif segment == 'Professional':
                    initial_plan_id = random.choice(SEGMENT_TO_PLANS['Growth'])
                elif segment == 'Growth':
                    initial_plan_id = random.choice(SEGMENT_TO_PLANS['Starter'])
                else:
                    flag = 'New'
                    prev_plan = None
            else:
                prev_plan = None
                
            plan_price = PLAN_DATA[initial_plan_id]['price']
            
        else:
            # Churned customer
            sub_status = 'Cancelled'
            
            # Cancelled sometime after signup, before today
            max_days = (date.today() - signup_date).days
            if max_days < 30:
                max_days = 30
            cancelled_days_after = random.randint(30, min(max_days, 730))
            cancelled_date = signup_date + timedelta(days=cancelled_days_after)
            end_date = cancelled_date
            renewal_date = None
            flag = 'New'
            prev_plan = None
        
        sub_id = generate_id('SUB', sub_counter)
        sub_counter += 1
        
        subscription = {
            'subscription_id': sub_id,
            'customer_id': customer_id,
            'plan_id': initial_plan_id,
            'status': sub_status,
            'start_date': sub_start,
            'end_date': end_date,
            'trial_end_date': sub_start + timedelta(days=14) 
                              if sub_status == 'Trial' else None,
            'cancelled_date': cancelled_date,
            'renewal_date': renewal_date,
            'auto_renew': random.random() > 0.15,
            'discount_percent': random.choice([0, 0, 0, 5, 10, 15, 20]),
            'mrr_value': plan_price if sub_status != 'Cancelled' else 0,
            'previous_plan_id': prev_plan,
            'upgrade_downgrade_flag': flag,
        }
        subscriptions.append(subscription)
    
    print(f"  ✅ {len(subscriptions)} subscriptions generated")
    return subscriptions

def generate_payments(customers, subscriptions):
    """Generate payment records"""
    print(f"\n📊 Generating payments...")
    payments = []
    pay_counter = 1
    
    # Create lookup dictionaries
    sub_by_customer = {}
    for sub in subscriptions:
        cid = sub['customer_id']
        if cid not in sub_by_customer:
            sub_by_customer[cid] = sub
    
    for customer in customers:
        cid = customer['customer_id']
        sub = sub_by_customer.get(cid)
        
        if not sub:
            continue
            
        sub_start = sub['start_date']
        sub_end = sub['cancelled_date'] or date.today()
        plan_id = sub['plan_id']
        plan_price = PLAN_DATA[plan_id]['price']
        sub_id = sub['subscription_id']
        
        # Generate monthly payments
        current_date = sub_start
        month_count = 0
        
        while current_date < sub_end and month_count < 36:
            # Determine if payment succeeds or fails
            # Failed payment probability increases for past-due accounts
            if sub['status'] == 'Past Due':
                fail_prob = 0.40
            else:
                fail_prob = 0.12
            
            payment_status = random.choices(
                ['Successful', 'Failed', 'Refunded', 'Disputed'],
                weights=[1 - fail_prob, fail_prob * 0.70, 
                         fail_prob * 0.20, fail_prob * 0.10]
            )[0]
            
            failure_reason = None
            retry_attempt = 0
            
            if payment_status == 'Failed':
                failure_reason = random.choice(FAILURE_REASONS)
                retry_attempt = random.randint(1, 3)
                
                # After retry, some succeed
                if retry_attempt >= 2 and random.random() > 0.5:
                    # Create a successful retry payment
                    retry_pay_id = generate_id('PAY', pay_counter)
                    pay_counter += 1
                    
                    payments.append({
                        'payment_id': retry_pay_id,
                        'customer_id': cid,
                        'subscription_id': sub_id,
                        'invoice_id': generate_id('INV', pay_counter),
                        'payment_date': current_date + timedelta(days=retry_attempt * 3),
                        'amount': plan_price,
                        'currency': 'USD',
                        'payment_method': weighted_choice(PAYMENT_METHODS, PAYMENT_METHOD_WEIGHTS),
                        'payment_status': 'Successful',
                        'failure_reason': None,
                        'retry_attempt': retry_attempt,
                        'gateway_response': 'APPROVED',
                        'is_recurring': True,
                        'payment_period_start': current_date,
                        'payment_period_end': current_date + timedelta(days=30),
                    })
            
            pay_id = generate_id('PAY', pay_counter)
            pay_counter += 1
            
            payment = {
                'payment_id': pay_id,
                'customer_id': cid,
                'subscription_id': sub_id,
                'invoice_id': generate_id('INV', pay_counter),
                'payment_date': current_date,
                'amount': plan_price,
                'currency': 'USD',
                'payment_method': weighted_choice(PAYMENT_METHODS, PAYMENT_METHOD_WEIGHTS),
                'payment_status': payment_status,
                'failure_reason': failure_reason,
                'retry_attempt': retry_attempt,
                'gateway_response': 'APPROVED' if payment_status == 'Successful' else 'DECLINED',
                'is_recurring': True,
                'payment_period_start': current_date,
                'payment_period_end': current_date + timedelta(days=30),
            }
            payments.append(payment)
            
            # Move to next month
            current_date = date(current_date.year + (current_date.month // 12),
                              (current_date.month % 12) + 1,
                              min(current_date.day, 28))
            month_count += 1
    
    print(f"  ✅ {len(payments)} payments generated")
    return payments

def generate_product_usage(customers, subscriptions):
    """Generate product usage records (weekly records per customer)"""
    print(f"\n📊 Generating product usage records...")
    usage_records = []
    usage_counter = 1
    
    sub_by_customer = {sub['customer_id']: sub for sub in subscriptions}
    
    for customer in customers:
        cid = customer['customer_id']
        sub = sub_by_customer.get(cid)
        
        if not sub:
            continue
        
        sub_start = sub['start_date']
        sub_end = sub['cancelled_date'] or date.today()
        segment = customer['customer_segment']
        
        # High usage customers vs low usage (some will churn due to low usage)
        is_high_usage = random.random() > 0.30
        
        # Generate weekly usage records
        current_date = sub_start
        while current_date < sub_end:
            
            # Base usage varies by segment
            if segment == 'Enterprise':
                base_users = random.randint(15, 80)
                base_sessions = random.randint(50, 300)
                base_features = random.randint(6, 12)
            elif segment == 'Professional':
                base_users = random.randint(8, 40)
                base_sessions = random.randint(20, 150)
                base_features = random.randint(4, 10)
            elif segment == 'Growth':
                base_users = random.randint(3, 20)
                base_sessions = random.randint(10, 80)
                base_features = random.randint(3, 8)
            else:  # Starter
                base_users = random.randint(1, 8)
                base_sessions = random.randint(2, 30)
                base_features = random.randint(1, 5)
            
            # Low usage customers use much less
            if not is_high_usage:
                base_users = max(0, base_users - int(base_users * 0.7))
                base_sessions = max(0, base_sessions - int(base_sessions * 0.7))
                base_features = max(0, base_features - 2)
            
            # Usage declines before churn
            days_to_end = (sub_end - current_date).days
            if sub['status'] == 'Cancelled' and days_to_end < 60:
                decay_factor = days_to_end / 60
                base_users = int(base_users * decay_factor)
                base_sessions = int(base_sessions * decay_factor)
                base_features = max(0, int(base_features * decay_factor))
            
            usage_id = generate_id('USG', usage_counter)
            usage_counter += 1
            
            record = {
                'usage_id': usage_id,
                'customer_id': cid,
                'subscription_id': sub['subscription_id'],
                'usage_date': current_date,
                'active_users': max(0, base_users + random.randint(-2, 2)),
                'total_sessions': max(0, base_sessions + random.randint(-5, 5)),
                'avg_session_duration_mins': round(random.uniform(5, 45), 2),
                'projects_created': random.randint(0, 5),
                'reports_generated': random.randint(0, 10),
                'api_calls': random.randint(0, 500) if segment in ['Professional', 'Enterprise'] else 0,
                'features_used': max(0, base_features),
                'storage_used_gb': round(random.uniform(0.1, 10), 2),
                'login_count': max(0, base_sessions),
                'last_login_date': current_date + timedelta(days=random.randint(0, 6)),
            }
            usage_records.append(record)
            
            # Weekly records
            current_date += timedelta(days=7)
    
    print(f"  ✅ {len(usage_records)} usage records generated")
    return usage_records

def generate_support_tickets(customers, subscriptions):
    """Generate support ticket records"""
    print(f"\n📊 Generating support tickets...")
    tickets = []
    ticket_counter = 1
    
    sub_by_customer = {sub['customer_id']: sub for sub in subscriptions}
    
    for customer in customers:
        cid = customer['customer_id']
        sub = sub_by_customer.get(cid)
        
        if not sub:
            continue
        
        sub_start = sub['start_date']
        sub_end = sub['cancelled_date'] or date.today()
        months_active = max(1, (sub_end - sub_start).days // 30)
        
        # Average 3-4 tickets per year, more for unhappy customers
        is_unhappy = sub['status'] == 'Cancelled'
        avg_tickets = int(months_active / 3) + (3 if is_unhappy else 0)
        num_tickets = random.randint(0, avg_tickets + 2)
        
        for t in range(num_tickets):
            ticket_date = random_date(sub_start, sub_end)
            category = random.choices(
                TICKET_CATEGORIES,
                weights=[0.25, 0.30, 0.15, 0.15, 0.10, 0.05]
            )[0]
            priority = random.choices(
                TICKET_PRIORITIES,
                weights=[0.30, 0.40, 0.20, 0.10]
            )[0]
            is_escalated = priority == 'Critical' or (priority == 'High' and random.random() > 0.7)
            
            status = random.choices(
                TICKET_STATUS_OPTIONS,
                weights=[0.10, 0.15, 0.35, 0.30, 0.10]
            )[0]
            
            resolution_date = None
            resolution_hours = None
            csat = None
            
            if status in ['Resolved', 'Closed']:
                resolution_days = random.randint(0, 5)
                resolution_date = ticket_date + timedelta(days=resolution_days)
                resolution_hours = round(resolution_days * 8 + random.uniform(1, 8), 2)
                csat = random.choices([1, 2, 3, 4, 5], weights=[0.05, 0.10, 0.20, 0.35, 0.30])[0]
            
            ticket_id = generate_id('TKT', ticket_counter)
            ticket_counter += 1
            
            ticket = {
                'ticket_id': ticket_id,
                'customer_id': cid,
                'subscription_id': sub['subscription_id'],
                'ticket_date': ticket_date,
                'category': category,
                'priority': priority,
                'status': status,
                'subject': f"{category} issue - {fake.bs()[:80]}",
                'channel': random.choice(TICKET_CHANNELS),
                'assigned_agent': random.choice(SUPPORT_AGENTS),
                'resolution_date': resolution_date,
                'resolution_time_hours': resolution_hours,
                'csat_score': csat,
                'is_escalated': is_escalated,
            }
            tickets.append(ticket)
    
    print(f"  ✅ {len(tickets)} support tickets generated")
    return tickets

def generate_cancellations(customers, subscriptions):
    """Generate cancellation records for churned customers"""
    print(f"\n📊 Generating cancellation records...")
    cancellations = []
    cancel_counter = 1
    
    for sub in subscriptions:
        if sub['status'] != 'Cancelled':
            continue
        
        cid = sub['customer_id']
        cancelled_date = sub['cancelled_date']
        plan_id = sub['plan_id']
        
        reason_category = weighted_choice(CANCELLATION_REASONS, CANCELLATION_WEIGHTS)
        
        # 40% involuntary (payment failure), 60% voluntary
        cancel_type = random.choices(
            ['Voluntary', 'Involuntary'],
            weights=[0.60, 0.40]
        )[0]
        
        # Competitor info only for voluntary cancellations due to competitor
        competitor = None
        if reason_category == 'Competitor':
            competitor = random.choice([c for c in COMPETITORS if c is not None])
        
        was_offered_discount = random.random() > 0.50
        discount_accepted = False
        if was_offered_discount:
            discount_accepted = random.random() > 0.33
        
        cancel_id = generate_id('CAN', cancel_counter)
        cancel_counter += 1
        
        cancellation = {
            'cancellation_id': cancel_id,
            'customer_id': cid,
            'subscription_id': sub['subscription_id'],
            'cancellation_date': cancelled_date,
            'effective_date': cancelled_date + timedelta(days=random.randint(0, 30)),
            'cancellation_reason_category': reason_category,
            'cancellation_reason_detail': f"Customer stated: {fake.sentence()[:200]}",
            'cancellation_type': cancel_type,
            'was_offered_discount': was_offered_discount,
            'discount_accepted': discount_accepted,
            'competitor_name': competitor,
            'win_back_eligible': random.random() > 0.25,
            'feedback_score': random.randint(1, 7),
            'processed_by': random.choice(ACCOUNT_MANAGERS),
        }
        cancellations.append(cancellation)
    
    print(f"  ✅ {len(cancellations)} cancellation records generated")
    return cancellations

def generate_invoices(payments, subscriptions):
    """Generate invoice records matching payments"""
    print(f"\n📊 Generating invoice records...")
    invoices = []
    inv_counter = 1
    
    sub_dict = {sub['subscription_id']: sub for sub in subscriptions}
    
    # Group payments by customer and period
    processed = set()
    
    for payment in payments:
        if not payment['payment_period_start']:
            continue
            
        key = (payment['customer_id'], 
               payment['subscription_id'],
               str(payment['payment_period_start']))
        
        if key in processed:
            continue
        processed.add(key)
        
        sub = sub_dict.get(payment['subscription_id'])
        if not sub:
            continue
        
        invoice_date = payment['payment_period_start']
        due_date = invoice_date + timedelta(days=15)
        subtotal = payment['amount']
        tax = round(subtotal * 0.08, 2)
        total = round(subtotal + tax, 2)
        
        # Determine invoice status
        if payment['payment_status'] == 'Successful':
            inv_status = 'Paid'
            amount_paid = total
        elif payment['payment_status'] == 'Refunded':
            inv_status = 'Void'
            amount_paid = 0
        elif payment['payment_status'] == 'Failed':
            today = date.today()
            if today > due_date:
                days_over = (today - due_date).days
                if days_over > 30:
                    inv_status = 'Overdue'
                else:
                    inv_status = 'Sent'
                amount_paid = 0
            else:
                inv_status = 'Sent'
                amount_paid = 0
        else:
            inv_status = 'Partially Paid'
            amount_paid = round(total * 0.5, 2)
        
        outstanding = round(total - amount_paid, 2)
        days_overdue = max(0, (date.today() - due_date).days) if inv_status == 'Overdue' else 0
        
        inv_id = generate_id('INV', inv_counter)
        inv_counter += 1
        
        invoice = {
            'invoice_id': inv_id,
            'customer_id': payment['customer_id'],
            'subscription_id': payment['subscription_id'],
            'invoice_date': invoice_date,
            'due_date': due_date,
            'billing_period_start': payment['payment_period_start'],
            'billing_period_end': payment['payment_period_end'],
            'subtotal': subtotal,
            'discount_amount': 0.00,
            'tax_amount': tax,
            'total_amount': total,
            'amount_paid': amount_paid,
            'outstanding_amount': outstanding,
            'invoice_status': inv_status,
            'payment_terms': random.choice(['Net 15', 'Net 30', 'Due on Receipt']),
            'days_overdue': days_overdue,
        }
        invoices.append(invoice)
    
    print(f"  ✅ {len(invoices)} invoice records generated")
    return invoices

# ============================================================
# DATABASE INSERTION FUNCTIONS
# ============================================================

def insert_customers(conn, customers):
    """Insert customers into database"""
    print(f"\n💾 Inserting {len(customers)} customers...")
    cursor = conn.cursor()
    
    sql = """
    INSERT INTO customers (
        customer_id, company_name, industry, company_size, 
        country, city, signup_date, acquisition_source, 
        account_manager, customer_segment, first_name, 
        last_name, email, phone, is_active
    ) VALUES (
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
    ) ON CONFLICT (customer_id) DO NOTHING;
    """
    
    batch_size = 100
    for i in range(0, len(customers), batch_size):
        batch = customers[i:i + batch_size]
        data = [(
            c['customer_id'], c['company_name'], c['industry'],
            c['company_size'], c['country'], c['city'],
            c['signup_date'], c['acquisition_source'],
            c['account_manager'], c['customer_segment'],
            c['first_name'], c['last_name'], c['email'],
            c['phone'], c['is_active']
        ) for c in batch]
        cursor.executemany(sql, data)
        conn.commit()
        print(f"  Inserted batch {i//batch_size + 1}...")
    
    print(f"  ✅ Customers inserted successfully")
    cursor.close()

def insert_subscriptions(conn, subscriptions):
    """Insert subscriptions into database"""
    print(f"\n💾 Inserting {len(subscriptions)} subscriptions...")
    cursor = conn.cursor()
    
    sql = """
    INSERT INTO subscriptions (
        subscription_id, customer_id, plan_id, status,
        start_date, end_date, trial_end_date, cancelled_date,
        renewal_date, auto_renew, discount_percent, mrr_value,
        previous_plan_id, upgrade_downgrade_flag
    ) VALUES (
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
    ) ON CONFLICT (subscription_id) DO NOTHING;
    """
    
    batch_size = 100
    for i in range(0, len(subscriptions), batch_size):
        batch = subscriptions[i:i + batch_size]
        data = [(
            s['subscription_id'], s['customer_id'], s['plan_id'],
            s['status'], s['start_date'], s['end_date'],
            s['trial_end_date'], s['cancelled_date'],
            s['renewal_date'], s['auto_renew'], s['discount_percent'],
            s['mrr_value'], s['previous_plan_id'], s['upgrade_downgrade_flag']
        ) for s in batch]
        cursor.executemany(sql, data)
        conn.commit()
        print(f"  Inserted batch {i//batch_size + 1}...")
    
    print(f"  ✅ Subscriptions inserted successfully")
    cursor.close()

def insert_payments(conn, payments):
    """Insert payments into database"""
    print(f"\n💾 Inserting {len(payments)} payments...")
    cursor = conn.cursor()
    
    sql = """
    INSERT INTO payments (
        payment_id, customer_id, subscription_id, invoice_id,
        payment_date, amount, currency, payment_method,
        payment_status, failure_reason, retry_attempt,
        gateway_response, is_recurring, payment_period_start,
        payment_period_end
    ) VALUES (
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
    ) ON CONFLICT (payment_id) DO NOTHING;
    """
    
    batch_size = 200
    for i in range(0, len(payments), batch_size):
        batch = payments[i:i + batch_size]
        data = [(
            p['payment_id'], p['customer_id'], p['subscription_id'],
            p['invoice_id'], p['payment_date'], p['amount'],
            p['currency'], p['payment_method'], p['payment_status'],
            p['failure_reason'], p['retry_attempt'],
            p['gateway_response'], p['is_recurring'],
            p['payment_period_start'], p['payment_period_end']
        ) for p in batch]
        cursor.executemany(sql, data)
        conn.commit()
        if i % 1000 == 0:
            print(f"  Inserted {i}/{len(payments)} payments...")
    
    print(f"  ✅ Payments inserted successfully")
    cursor.close()

def insert_product_usage(conn, usage_records):
    """Insert product usage records"""
    print(f"\n💾 Inserting {len(usage_records)} usage records...")
    cursor = conn.cursor()
    
    sql = """
    INSERT INTO product_usage (
        usage_id, customer_id, subscription_id, usage_date,
        active_users, total_sessions, avg_session_duration_mins,
        projects_created, reports_generated, api_calls,
        features_used, storage_used_gb, login_count, last_login_date
    ) VALUES (
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
    ) ON CONFLICT (usage_id) DO NOTHING;
    """
    
    batch_size = 500
    for i in range(0, len(usage_records), batch_size):
        batch = usage_records[i:i + batch_size]
        data = [(
            u['usage_id'], u['customer_id'], u['subscription_id'],
            u['usage_date'], u['active_users'], u['total_sessions'],
            u['avg_session_duration_mins'], u['projects_created'],
            u['reports_generated'], u['api_calls'],
            u['features_used'], u['storage_used_gb'],
            u['login_count'], u['last_login_date']
        ) for u in batch]
        cursor.executemany(sql, data)
        conn.commit()
        if i % 2000 == 0:
            print(f"  Inserted {i}/{len(usage_records)} usage records...")
    
    print(f"  ✅ Usage records inserted successfully")
    cursor.close()

def insert_support_tickets(conn, tickets):
    """Insert support tickets"""
    print(f"\n💾 Inserting {len(tickets)} support tickets...")
    cursor = conn.cursor()
    
    sql = """
    INSERT INTO support_tickets (
        ticket_id, customer_id, subscription_id, ticket_date,
        category, priority, status, subject, channel,
        assigned_agent, resolution_date, resolution_time_hours,
        csat_score, is_escalated
    ) VALUES (
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
    ) ON CONFLICT (ticket_id) DO NOTHING;
    """
    
    batch_size = 200
    for i in range(0, len(tickets), batch_size):
        batch = tickets[i:i + batch_size]
        data = [(
            t['ticket_id'], t['customer_id'], t['subscription_id'],
            t['ticket_date'], t['category'], t['priority'],
            t['status'], t['subject'], t['channel'],
            t['assigned_agent'], t['resolution_date'],
            t['resolution_time_hours'], t['csat_score'],
            t['is_escalated']
        ) for t in batch]
        cursor.executemany(sql, data)
        conn.commit()
        print(f"  Inserted batch {i//batch_size + 1}...")
    
    print(f"  ✅ Support tickets inserted successfully")
    cursor.close()

def insert_cancellations(conn, cancellations):
    """Insert cancellation records"""
    print(f"\n💾 Inserting {len(cancellations)} cancellations...")
    cursor = conn.cursor()
    
    sql = """
    INSERT INTO cancellations (
        cancellation_id, customer_id, subscription_id,
        cancellation_date, effective_date,
        cancellation_reason_category, cancellation_reason_detail,
        cancellation_type, was_offered_discount, discount_accepted,
        competitor_name, win_back_eligible, feedback_score,
        processed_by
    ) VALUES (
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
    ) ON CONFLICT (cancellation_id) DO NOTHING;
    """
    
    batch_size = 100
    for i in range(0, len(cancellations), batch_size):
        batch = cancellations[i:i + batch_size]
        data = [(
            c['cancellation_id'], c['customer_id'], c['subscription_id'],
            c['cancellation_date'], c['effective_date'],
            c['cancellation_reason_category'], c['cancellation_reason_detail'],
            c['cancellation_type'], c['was_offered_discount'],
            c['discount_accepted'], c['competitor_name'],
            c['win_back_eligible'], c['feedback_score'],
            c['processed_by']
        ) for c in batch]
        cursor.executemany(sql, data)
        conn.commit()
    
    print(f"  ✅ Cancellations inserted successfully")
    cursor.close()

def insert_invoices(conn, invoices):
    """Insert invoice records"""
    print(f"\n💾 Inserting {len(invoices)} invoices...")
    cursor = conn.cursor()
    
    sql = """
    INSERT INTO invoices (
        invoice_id, customer_id, subscription_id, invoice_date,
        due_date, billing_period_start, billing_period_end,
        subtotal, discount_amount, tax_amount, total_amount,
        amount_paid, outstanding_amount, invoice_status,
        payment_terms, days_overdue
    ) VALUES (
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
    ) ON CONFLICT (invoice_id) DO NOTHING;
    """
    
    batch_size = 200
    for i in range(0, len(invoices), batch_size):
        batch = invoices[i:i + batch_size]
        data = [(
            inv['invoice_id'], inv['customer_id'], inv['subscription_id'],
            inv['invoice_date'], inv['due_date'],
            inv['billing_period_start'], inv['billing_period_end'],
            inv['subtotal'], inv['discount_amount'], inv['tax_amount'],
            inv['total_amount'], inv['amount_paid'],
            inv['outstanding_amount'], inv['invoice_status'],
            inv['payment_terms'], inv['days_overdue']
        ) for inv in batch]
        cursor.executemany(sql, data)
        conn.commit()
        if i % 1000 == 0:
            print(f"  Inserted {i}/{len(invoices)} invoices...")
    
    print(f"  ✅ Invoices inserted successfully")
    cursor.close()

# ============================================================
# VERIFICATION FUNCTION
# ============================================================

def verify_data(conn):
    """Verify all data was inserted correctly"""
    print("\n📊 VERIFICATION REPORT")
    print("=" * 50)
    
    cursor = conn.cursor()
    
    tables = [
        'customers', 'plans', 'subscriptions', 'payments',
        'product_usage', 'support_tickets', 'cancellations', 'invoices'
    ]
    
    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"  {table:<20} → {count:>8,} records")
    
    print("\n📊 DATA QUALITY CHECKS")
    print("=" * 50)
    
    # Check payment status distribution
    cursor.execute("""
        SELECT payment_status, COUNT(*) as count,
               ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 1) as pct
        FROM payments
        GROUP BY payment_status
        ORDER BY count DESC
    """)
    print("\nPayment Status Distribution:")
    for row in cursor.fetchall():
        print(f"  {row[0]:<20} → {row[1]:>6,} ({row[2]}%)")
    
    # Check subscription status
    cursor.execute("""
        SELECT status, COUNT(*) as count
        FROM subscriptions
        GROUP BY status
        ORDER BY count DESC
    """)
    print("\nSubscription Status Distribution:")
    for row in cursor.fetchall():
        print(f"  {row[0]:<20} → {row[1]:>6,}")
    
    # Check MRR
    cursor.execute("""
        SELECT ROUND(SUM(mrr_value), 2) as total_mrr
        FROM subscriptions
        WHERE status = 'Active'
    """)
    mrr = cursor.fetchone()[0]
    print(f"\n  Total Current MRR: ${mrr:,.2f}")
    print(f"  Projected ARR:     ${mrr * 12:,.2f}")
    
    cursor.close()
    print("\n✅ VERIFICATION COMPLETE")

# ============================================================
# MAIN EXECUTION
# ============================================================

def main():
    print("=" * 60)
    print("  STREAMLINE ANALYTICS - DATA GENERATION SCRIPT")
    print("=" * 60)
    print("\nThis script will generate all sample data for the")
    print("SaaS Customer Retention Analysis project.\n")
    
    # Number of customers to generate
    # Start with 500 for testing, increase to 2000 for full dataset
    NUM_CUSTOMERS = 500
    
    print(f"Configuration: {NUM_CUSTOMERS} customers")
    print("Estimated time: 2-5 minutes\n")
    
    # Connect to database
    conn = connect_db()
    
    try:
        # Step 1: Generate all data in memory
        print("PHASE 1: GENERATING DATA IN MEMORY")
        print("-" * 40)
        
        customers = generate_customers(NUM_CUSTOMERS)
        subscriptions = generate_subscriptions(customers)
        payments = generate_payments(customers, subscriptions)
        usage = generate_product_usage(customers, subscriptions)
        tickets = generate_support_tickets(customers, subscriptions)
        cancellations = generate_cancellations(customers, subscriptions)
        invoices = generate_invoices(payments, subscriptions)
        
        # Step 2: Insert all data into database
        print("\nPHASE 2: INSERTING DATA INTO DATABASE")
        print("-" * 40)
        
        insert_customers(conn, customers)
        insert_subscriptions(conn, subscriptions)
        insert_payments(conn, payments)
        insert_product_usage(conn, usage)
        insert_support_tickets(conn, tickets)
        insert_cancellations(conn, cancellations)
        insert_invoices(conn, invoices)
        
        # Step 3: Verify the data
        print("\nPHASE 3: VERIFICATION")
        print("-" * 40)
        verify_data(conn)
        
        print("\n" + "=" * 60)
        print("  🎉 DATA GENERATION COMPLETE!")
        print("=" * 60)
        print("\nNext steps:")
        print("  1. Open pgAdmin and verify your data")
        print("  2. Run your SQL queries from the 03_sql_queries folder")
        print("  3. Connect Power BI to your PostgreSQL database")
        
    except Exception as e:
        print(f"\n❌ Error occurred: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()
        print("\nDatabase connection closed.")

if __name__ == "__main__":
    main()