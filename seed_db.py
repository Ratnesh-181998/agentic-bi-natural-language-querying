import sqlite3
import pandas as pd
from datetime import datetime, timedelta
import random

def seed():
    conn = sqlite3.connect('enterprise_bi_db.sqlite')
    cursor = conn.cursor()
    
    # List of tables to drop/recreate
    tables = [
        'sales', 'customers', 'products', 'regions', 'marketing', 
        'subscriptions', 'support_tickets', 'inventory', 'employee_performance', 
        'website_traffic', 'expenses', 'competitor_metrics', 'churn_analysis', 
        'product_reviews', 'operating_budget'
    ]
    
    for table in tables:
        cursor.execute(f'DROP TABLE IF EXISTS {table}')

    # --- TABLE CREATION SCIPTS ---
    
    # 1. SALES
    cursor.execute('''
        CREATE TABLE sales (
            transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
            revenue REAL,
            date TEXT,
            region TEXT,
            product TEXT,
            customer_id INTEGER,
            discount REAL,
            quantity INTEGER,
            unit_price REAL,
            tax REAL
        )
    ''')

    # 2. CUSTOMERS
    cursor.execute('''
        CREATE TABLE customers (
            customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            country TEXT,
            signup_date TEXT,
            loyalty_tier TEXT,
            total_spend REAL,
            acquisition_channel TEXT,
            last_login TEXT,
            age INTEGER
        )
    ''')

    # 3. PRODUCTS
    cursor.execute('''
        CREATE TABLE products (
            product_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            category TEXT,
            base_price REAL,
            production_cost REAL,
            stock_level INTEGER,
            release_date TEXT,
            rating REAL,
            returns_count INTEGER,
            shelf_life_days INTEGER
        )
    ''')

    # 4. REGIONS
    cursor.execute('''
        CREATE TABLE regions (
            region_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            manager TEXT,
            budget_allocated REAL,
            target_revenue REAL,
            active_reps INTEGER,
            population_coverage INTEGER,
            office_count INTEGER,
            tax_rate REAL,
            seasonality_factor REAL
        )
    ''')

    # 5. MARKETING
    cursor.execute('''
        CREATE TABLE marketing (
            campaign_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            channel TEXT,
            spend REAL,
            clicks INTEGER,
            conversions INTEGER,
            date TEXT,
            impressions INTEGER,
            roi REAL,
            manager_id INTEGER,
            region TEXT
        )
    ''')

    # 6. SUBSCRIPTIONS
    cursor.execute('''
        CREATE TABLE subscriptions (
            sub_id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER,
            plan_name TEXT,
            monthly_price REAL,
            start_date TEXT,
            expiry_date TEXT,
            status TEXT,
            renewal_count INTEGER,
            churn_reason TEXT,
            auto_renew INTEGER
        )
    ''')

    # 7. SUPPORT TICKETS
    cursor.execute('''
        CREATE TABLE support_tickets (
            ticket_id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER,
            issue_type TEXT,
            priority TEXT,
            status TEXT,
            created_date TEXT,
            resolved_date TEXT,
            agent_name TEXT,
            resolution_time_hrs REAL,
            customer_satisfaction INTEGER
        )
    ''')

    # 8. INVENTORY
    cursor.execute('''
        CREATE TABLE inventory (
            entry_id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER,
            warehouse_location TEXT,
            quantity_on_hand INTEGER,
            reorder_point INTEGER,
            supplier_name TEXT,
            last_restock_date TEXT,
            unit_weight REAL,
            storage_cost REAL,
            bin_number TEXT
        )
    ''')

    # 9. EMPLOYEE PERFORMANCE
    cursor.execute('''
        CREATE TABLE employee_performance (
            emp_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            role TEXT,
            department TEXT,
            quota REAL,
            actual_sales REAL,
            bonus_percentage REAL,
            join_date TEXT,
            training_completed INTEGER,
            review_score REAL
        )
    ''')

    # 10. WEBSITE TRAFFIC
    cursor.execute('''
        CREATE TABLE website_traffic (
            traffic_id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            sessions INTEGER,
            users INTEGER,
            bounce_rate REAL,
            avg_session_duration REAL,
            pageviews_per_session REAL,
            conversion_rate REAL,
            conversions INTEGER,
            device_type TEXT,
            traffic_source TEXT
        )
    ''')

    # 11. EXPENSES
    cursor.execute('''
        CREATE TABLE expenses (
            expense_id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT,
            amount REAL,
            date TEXT,
            department_id TEXT,
            vendor_name TEXT,
            payment_method TEXT,
            tax_deductible INTEGER,
            approval_status TEXT,
            description TEXT
        )
    ''')

    # 12. COMPETITOR METRICS
    cursor.execute('''
        CREATE TABLE competitor_metrics (
            comp_id INTEGER PRIMARY KEY AUTOINCREMENT,
            competitor_name TEXT,
            product_name TEXT,
            market_price REAL,
            market_share REAL,
            rating REAL,
            year INTEGER,
            tech_score REAL,
            region TEXT,
            ad_spend_estimate REAL
        )
    ''')

    # 13. CHURN ANALYSIS
    cursor.execute('''
        CREATE TABLE churn_analysis (
            churn_id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER,
            churn_date TEXT,
            primary_reason TEXT,
            secondary_reason TEXT,
            retention_offered INTEGER,
            feedback_score INTEGER,
            account_age_months INTEGER,
            switch_to_competitor INTEGER,
            refund_granted INTEGER
        )
    ''')

    # 14. PRODUCT REVIEWS
    cursor.execute('''
        CREATE TABLE product_reviews (
            review_id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER,
            customer_id INTEGER,
            rating INTEGER,
            review_date TEXT,
            sentiment_score REAL,
            verified_purchase INTEGER,
            helpful_votes INTEGER,
            review_length INTEGER,
            platform TEXT
        )
    ''')

    # 15. OPERATING BUDGET
    cursor.execute('''
        CREATE TABLE operating_budget (
            budget_id INTEGER PRIMARY KEY AUTOINCREMENT,
            year INTEGER,
            quarter TEXT,
            department TEXT,
            allocated_budget REAL,
            actual_spend REAL,
            variance REAL,
            approved_by TEXT,
            last_updated TEXT,
            notes TEXT
        )
    ''')

    # --- DATA GENERATION CONFIG ---
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2026, 12, 31)
    delta_days = (end_date - start_date).days
    
    def random_date_str(start_yr=2023, end_yr=2026):
        start = datetime(start_yr, 1, 1)
        end = datetime(end_yr, 12, 31)
        days = (end - start).days
        return (start + timedelta(days=random.randint(0, days))).strftime('%Y-%m-%d')

    regions_list = ['North', 'South', 'East', 'West']
    prods_list = ['SaaS Pro', 'SaaS Elite', 'SaaS Basic', 'SaaS Plus', 'Enterprise Plan']
    depts_list = ['IT', 'HR', 'Sales', 'Marketing', 'Finance', 'Operations', 'R&D']
    channels_list = ['FB', 'GAds', 'LI', 'Twitter', 'Organic', 'Referral', 'Email']
    
    print("Generating Robust Data for 24 Questions Scenario...")

    # 1. SALES (2000 Records)
    sales_data = []
    for _ in range(2000):
        # Weighted revenue for realism
        prod = random.choice(prods_list)
        base = 500 if 'Basic' in prod else (2000 if 'Elite' in prod else 1000)
        
        qty = random.randint(1, 5)
        discount = random.choice([0.0, 0.05, 0.1, 0.2])
        price = base * (1 - discount)
        rev = price * qty
        
        sales_data.append((
            rev, random_date_str(), random.choice(regions_list), 
            prod, random.randint(1, 500), 
            discount, qty, base, rev*0.1
        ))
    cursor.executemany('INSERT INTO sales (revenue, date, region, product, customer_id, discount, quantity, unit_price, tax) VALUES (?,?,?,?,?,?,?,?,?)', sales_data)

    # 2. CUSTOMERS (500 Records)
    cust_data = []
    for i in range(1, 501):
        tier = random.choices(['Gold', 'Silver', 'Bronze'], weights=[0.2, 0.3, 0.5])[0]
        spend = random.uniform(5000, 20000) if tier == 'Gold' else random.uniform(100, 5000)
        cust_data.append((
            f"Customer_{i}", f"user{i}@example.com", random.choice(['USA', 'UK', 'India', 'Canada']),
            random_date_str(2023, 2025), tier, spend,
            random.choice(channels_list), random_date_str(2025, 2026), random.randint(20, 60)
        ))
    cursor.executemany('INSERT INTO customers (name, email, country, signup_date, loyalty_tier, total_spend, acquisition_channel, last_login, age) VALUES (?,?,?,?,?,?,?,?,?)', cust_data)

    # 3. PRODUCTS (Fixed List for Consistency)
    products_static = [
        ('SaaS Pro', 'Software', 99.99, 10.00, 10000),
        ('SaaS Elite', 'Software', 199.99, 15.00, 10000),
        ('SaaS Basic', 'Software', 49.99, 5.00, 10000),
        ('Enterprise Plan', 'Enterprise', 999.99, 100.00, 500),
        ('Consulting Hr', 'Service', 150.00, 100.00, 1000),
        ('Hardware Key', 'Hardware', 25.00, 5.00, 5000),
        ('Training Pack', 'Content', 500.00, 50.00, 2000)
    ]
    prod_db_data = []
    for p in products_static:
        prod_db_data.append((
            p[0], p[1], p[2], p[3], p[4], 
            '2023-01-01', random.uniform(3.5, 5.0), random.randint(0, 50), 365
        ))
    cursor.executemany('INSERT INTO products (name, category, base_price, production_cost, stock_level, release_date, rating, returns_count, shelf_life_days) VALUES (?,?,?,?,?,?,?,?,?)', prod_db_data)

    # 4. REGIONS (Fixed List)
    reg_db = []
    for r in regions_list:
        reg_db.append((
            r, f"Manager_{r}", 1000000, 1500000, 
            random.randint(5, 20), random.randint(10000, 500000), 
            random.randint(1, 4), 0.08, 1.2
        ))
    cursor.executemany('INSERT INTO regions (name, manager, budget_allocated, target_revenue, active_reps, population_coverage, office_count, tax_rate, seasonality_factor) VALUES (?,?,?,?,?,?,?,?,?)', reg_db)

    # 5. EXPENSES (500 Records)
    exp_cats = ['Travel', 'Software', 'Marketing', 'Office Supplies', 'Salaries', 'Utilities']
    exp_data = []
    for _ in range(500):
        cat = random.choice(exp_cats)
        amt = random.uniform(100, 10000)
        dept = random.choice(depts_list)
        # For "non-tax-deductible expenses > $5000 in IT"
        tax_ded = 0 if (dept == 'IT' and amt > 5000 and random.random() < 0.3) else 1
        
        exp_data.append((
            cat, amt, random_date_str(2023, 2026), dept, 
            f"Vendor_{random.randint(1,50)}", "Card", tax_ded, 
            "Approved", f"{cat} expense for {dept}"
        ))
    cursor.executemany('INSERT INTO expenses (category, amount, date, department_id, vendor_name, payment_method, tax_deductible, approval_status, description) VALUES (?,?,?,?,?,?,?,?,?)', exp_data)

    # 6. OPERATING BUDGET (Matches Expenses/Depts)
    bud_data = []
    for yr in [2024, 2025, 2026]:
        for q in ['Q1', 'Q2', 'Q3', 'Q4']:
            for d in depts_list:
                alloc = random.uniform(50000, 200000)
                # "Show me departments where actual spend exceeded the budget by more than 10%"
                # Force some variances
                variance_factor = random.choice([0.9, 1.0, 1.05, 1.2]) 
                actual = alloc * variance_factor
                
                bud_data.append((
                    yr, q, d, alloc, actual, alloc-actual, 
                    "CFO", f"{yr}-01-01", f"Budget for {d} {yr} {q}"
                ))
    cursor.executemany('INSERT INTO operating_budget (year, quarter, department, allocated_budget, actual_spend, variance, approved_by, last_updated, notes) VALUES (?,?,?,?,?,?,?,?,?)', bud_data)

    # 7. MARKETING CAMPAIGNS (Matches 'Acquisition ROI' and 'Best Campaign ROI')
    mkt_db = []
    for _ in range(100):
        # High ROI outliers
        spend = random.uniform(1000, 5000)
        conv = random.randint(10, 300)
        if random.random() < 0.05: # "Best Campaign" candidate
            conv = 1000 
            spend = 2000 # Massive ROI
            
        clicks = conv * random.randint(10, 30)
        imps = clicks * random.randint(10, 50)
        roi = (conv * 100) / spend # revenue proxy
        
        mkt_db.append((
            f"Campaign_{random.randint(1,500)}", random.choice(channels_list),
            spend, clicks, conv, random_date_str(2023, 2026),
            imps, roi, random.randint(1, 10), random.choice(regions_list)
        )),
    cursor.executemany('INSERT INTO marketing (name, channel, spend, clicks, conversions, date, impressions, roi, manager_id, region) VALUES (?,?,?,?,?,?,?,?,?,?)', mkt_db)

    # 8. SUBSCRIPTIONS (For 'Churn' and 'Plan Revenue Mix' and 'Subscription Health')
    sub_data = []
    for _ in range(800):
        plan = random.choice(prods_list)
        price = 199.99 if 'Elite' in plan else (99.99 if 'Pro' in plan else 49.99)
        status = random.choices(['Active', 'Canceled'], weights=[0.7, 0.3])[0]
        churn_reason = random.choice(['Price', 'Service', 'Competitor', 'No Usage']) if status == 'Canceled' else None
        
        sub_data.append((
            random.randint(1, 500), plan, price, random_date_str(2023, 2025),
            random_date_str(2025, 2027), status, random.randint(0, 24),
            churn_reason, 1
        ))
    cursor.executemany('INSERT INTO subscriptions (customer_id, plan_name, monthly_price, start_date, expiry_date, status, renewal_count, churn_reason, auto_renew) VALUES (?,?,?,?,?,?,?,?,?)', sub_data)

    # 9. SUPPORT TICKETS (For 'SLA Health', 'Cust Satisfaction')
    tick_data = []
    for _ in range(300):
        priority = random.choice(['High', 'Medium', 'Low'])
        agent = random.choice(['Agent Smith', 'Agent Doe', 'Agent Johnson'])
        issue = random.choice(['Bug', 'Feature', 'Billing', 'Login'])
        
        # Logic: High priority might need faster resolution
        res_time = random.uniform(1, 48) if priority == 'Low' else random.uniform(0.5, 12)
        sat = random.randint(1, 5)
        
        tick_data.append((
            random.randint(1, 500), issue, priority, random.choice(['Closed', 'Open']),
            random_date_str(), random_date_str(), agent, res_time, sat
        ))
    cursor.executemany('INSERT INTO support_tickets (customer_id, issue_type, priority, status, created_date, resolved_date, agent_name, resolution_time_hrs, customer_satisfaction) VALUES (?,?,?,?,?,?,?,?,?)', tick_data)

    # 10. INVENTORY (For 'Low Stock', 'Warehouse Load')
    inv_data = []
    warehouses = ['WH_North', 'WH_South', 'WH_Main', 'WH_East']
    for pid in range(1, 8): # 7 seeded products
        for wh in warehouses:
            qty = random.randint(0, 500)
            reorder = random.randint(50, 100)
            # Ensure some low stock
            if random.random() < 0.2:
                qty = random.randint(0, 40)
            
            inv_data.append((
                pid, wh, qty, reorder, "Supplier_X", random_date_str(), 1.0, 5.0, "Bin_A"
            ))
    cursor.executemany('INSERT INTO inventory (product_id, warehouse_location, quantity_on_hand, reorder_point, supplier_name, last_restock_date, unit_weight, storage_cost, bin_number) VALUES (?,?,?,?,?,?,?,?,?)', inv_data)

    # 11. EMPLOYEE PERFORMANCE (For 'Top Sales Reps')
    emp_data = []
    for i in range(1, 21):
        quota = 50000
        actual = random.uniform(20000, 80000)
        emp_data.append((
            f"Rep_{i}", "Sales Rep", "Sales", quota, actual, (actual/quota)*10,
            "2023-01-15", 1, random.uniform(3.0, 5.0)
        ))
    cursor.executemany('INSERT INTO employee_performance (name, role, department, quota, actual_sales, bonus_percentage, join_date, training_completed, review_score) VALUES (?,?,?,?,?,?,?,?,?)', emp_data)

    # 12. WEBSITE TRAFFIC (For 'Traffic vs Leads', 'Mobile vs Desktop')
    traffic = []
    for _ in range(365 * 3): # 3 years
        date = random_date_str(2023, 2026)
        sess = random.randint(1000, 5000)
        # Correlation: High sessions -> High conversions often
        conv = int(sess * random.uniform(0.01, 0.05)) 
        
        traffic.append((
            date, sess, int(sess*0.8), 45.5, 120.5, 3.5, 
            (conv/sess)*100, conv, random.choice(['Mobile', 'Desktop']), random.choice(channels_list)
        ))
    cursor.executemany('INSERT INTO website_traffic (date, sessions, users, bounce_rate, avg_session_duration, pageviews_per_session, conversion_rate, conversions, device_type, traffic_source) VALUES (?,?,?,?,?,?,?,?,?,?)', traffic)

    # 13. COMPETITOR METRICS (For 'Competitor Price Gap')
    # Our Pro price is ~99.99
    comp_data = []
    competitors = ['Comp_A', 'Comp_B', 'Comp_C']
    for c in competitors:
        # Market price around 120 (so ours is cheaper) or 80 (ours is pricier)
        mkt_price = random.choice([89.99, 129.99, 110.00])
        comp_data.append((
            c, "Standard Plan", mkt_price, random.uniform(5, 20), 4.2, 
            2025, 8.5, "Global", 50000
        ))
    cursor.executemany('INSERT INTO competitor_metrics (competitor_name, product_name, market_price, market_share, rating, year, tech_score, region, ad_spend_estimate) VALUES (?,?,?,?,?,?,?,?,?)', comp_data)

    # 14. CHURN ANALYSIS (Augments Subscriptions)
    churn_data = []
    for _ in range(100):
        # Top reasons: Price, Service, Competitor
        churn_data.append((
            random.randint(1, 500), random_date_str(), 
            random.choice(['Price', 'Service', 'Competitor']), "Other",
            random.randint(0, 1), random.randint(1, 10), random.randint(1, 12),
            random.randint(0, 1), random.randint(0, 1)
        ))
    cursor.executemany('INSERT INTO churn_analysis (customer_id, churn_date, primary_reason, secondary_reason, retention_offered, feedback_score, account_age_months, switch_to_competitor, refund_granted) VALUES (?,?,?,?,?,?,?,?,?)', churn_data)

    # 15. PRODUCT REVIEWS (For 'Review Sentiments')
    rev_data = []
    for _ in range(200):
        # Correlate sentinel matches region sales (simulated via random)
        rating = random.randint(1, 5)
        sent = (rating - 3) * 0.4 # crude sentiment
        
        rev_data.append((
            random.randint(1, 5), random.randint(1, 500), rating, 
            random_date_str(2024, 2025), sent, 1, random.randint(0, 10), 50, "Web"
        ))
    cursor.executemany('INSERT INTO product_reviews (product_id, customer_id, rating, review_date, sentiment_score, verified_purchase, helpful_votes, review_length, platform) VALUES (?,?,?,?,?,?,?,?,?)', rev_data)

    conn.commit()
    conn.close()
    print("Enterprise Database RE-SEEDED Successfully: 15 Tables, Robust Data for 2023-2026.")

if __name__ == "__main__":
    seed()
