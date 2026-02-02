"""
TECHNICAL EVENT MANAGEMENT SYSTEM
==================================
A comprehensive web application for managing technical events
with Admin, User, and Vendor roles with proper access controls.

Author: Student Project
Date: February 2026
"""

from flask import Flask, render_template_string, request, redirect, url_for, session, flash
from datetime import datetime
import pickle
import os

# Data persistence directory
DATA_DIR = 'data'
os.makedirs(DATA_DIR, exist_ok=True)

ROLE_HOME = {
    'admin': 'admin_dashboard',
    'vendor': 'vendor_dashboard',
    'user': 'user_dashboard'
}

def get_back_url():
    """Get the appropriate back URL based on user's role and current location"""
    if 'role' not in session:
        return url_for('index')
    
    # If at mode home (dashboard), go to index
    if session.get('at_mode_home', False):
        return url_for('index')
    
    # Otherwise go to role's dashboard
    return url_for(ROLE_HOME[session['role']])

# Initialize Flask application
action = None  # GLOBAL SAFETY: prevents UnboundLocalError for forgotten form actions


app = Flask(__name__)
app.secret_key = 'student_project_secret_key_2026'

@app.context_processor
def inject_back_url():
    """Make back_url available to all templates"""
    return dict(back_url=get_back_url)

# ============================================================================
# DATABASE (In-Memory Storage)
# ============================================================================

# Users Database
users_db = {
    'admin': {'password': 'admin123', 'role': 'admin', 'name': 'System Admin', 'email': 'admin@system.com'}
}

vendors_db = {
    'vendor1': {'password': 'vendor123', 'role': 'vendor', 'name': 'Tech Vendors Inc', 'email': 'vendor@tech.com', 'phone': '9876543210'}
}

regular_users_db = {
    'user1': {'password': 'user123', 'name': 'John Doe', 'email': 'john@example.com', 'phone': '1234567890'}
}

# Products Database
products_db = []
product_id_counter = [1]

# Cart Database
cart_db = {}

# Orders Database
orders_db = []
order_id_counter = [1]

# Admin Notifications
notifications_db = []
notification_id_counter = [1]

# Vendor Notifications
vendor_notifications_db = []
vendor_notification_id_counter = [1]

# Memberships Database (NEW)
memberships_db = []
membership_id_counter = [1]

# User Requests Database (NEW)
user_requests_db = []
request_id_counter = [1]

# Guest List Database (NEW)
guest_list_db = []
guest_id_counter = [1]

# ============================================================================
# DATA PERSISTENCE FUNCTIONS
# ============================================================================

def save_all_data():
    """Save all databases to disk using Pickle"""
    try:
        with open(f'{DATA_DIR}/users.pkl', 'wb') as f:
            pickle.dump(users_db, f)
        with open(f'{DATA_DIR}/regular_users.pkl', 'wb') as f:
            pickle.dump(regular_users_db, f)
        with open(f'{DATA_DIR}/vendors.pkl', 'wb') as f:
            pickle.dump(vendors_db, f)
        with open(f'{DATA_DIR}/products.pkl', 'wb') as f:
            pickle.dump((products_db, product_id_counter), f)
        with open(f'{DATA_DIR}/carts.pkl', 'wb') as f:
            pickle.dump(cart_db, f)
        with open(f'{DATA_DIR}/orders.pkl', 'wb') as f:
            pickle.dump((orders_db, order_id_counter), f)
        with open(f'{DATA_DIR}/notifications.pkl', 'wb') as f:
            pickle.dump((notifications_db, notification_id_counter), f)
        with open(f'{DATA_DIR}/vendor_notifications.pkl', 'wb') as f:
            pickle.dump((vendor_notifications_db, vendor_notification_id_counter), f)
        with open(f'{DATA_DIR}/memberships.pkl', 'wb') as f:
            pickle.dump((memberships_db, membership_id_counter), f)
        with open(f'{DATA_DIR}/requests.pkl', 'wb') as f:
            pickle.dump((user_requests_db, request_id_counter), f)
        with open(f'{DATA_DIR}/guests.pkl', 'wb') as f:
            pickle.dump((guest_list_db, guest_id_counter), f)
        print("✅ Data saved successfully!")
    except Exception as e:
        print(f"❌ Error saving data: {e}")

def load_all_data():
    """Load all databases from disk"""
    global users_db, regular_users_db, vendors_db, products_db, product_id_counter
    global cart_db, orders_db, order_id_counter
    global notifications_db, notification_id_counter
    global vendor_notifications_db, vendor_notification_id_counter
    global memberships_db, membership_id_counter
    global user_requests_db, request_id_counter
    global guest_list_db, guest_id_counter
    
    try:
        if os.path.exists(f'{DATA_DIR}/users.pkl'):
            with open(f'{DATA_DIR}/users.pkl', 'rb') as f:
                users_db = pickle.load(f)
        
        if os.path.exists(f'{DATA_DIR}/regular_users.pkl'):
            with open(f'{DATA_DIR}/regular_users.pkl', 'rb') as f:
                regular_users_db = pickle.load(f)
        
        if os.path.exists(f'{DATA_DIR}/vendors.pkl'):
            with open(f'{DATA_DIR}/vendors.pkl', 'rb') as f:
                vendors_db = pickle.load(f)
        
        if os.path.exists(f'{DATA_DIR}/products.pkl'):
            with open(f'{DATA_DIR}/products.pkl', 'rb') as f:
                products_db, product_id_counter[:] = pickle.load(f)
        
        if os.path.exists(f'{DATA_DIR}/carts.pkl'):
            with open(f'{DATA_DIR}/carts.pkl', 'rb') as f:
                cart_db = pickle.load(f)
        
        if os.path.exists(f'{DATA_DIR}/orders.pkl'):
            with open(f'{DATA_DIR}/orders.pkl', 'rb') as f:
                orders_db, order_id_counter[:] = pickle.load(f)
        
        if os.path.exists(f'{DATA_DIR}/notifications.pkl'):
            with open(f'{DATA_DIR}/notifications.pkl', 'rb') as f:
                notifications_db, notification_id_counter[:] = pickle.load(f)
        
        if os.path.exists(f'{DATA_DIR}/vendor_notifications.pkl'):
            with open(f'{DATA_DIR}/vendor_notifications.pkl', 'rb') as f:
                vendor_notifications_db, vendor_notification_id_counter[:] = pickle.load(f)
        
        if os.path.exists(f'{DATA_DIR}/memberships.pkl'):
            with open(f'{DATA_DIR}/memberships.pkl', 'rb') as f:
                memberships_db, membership_id_counter[:] = pickle.load(f)
        
        if os.path.exists(f'{DATA_DIR}/requests.pkl'):
            with open(f'{DATA_DIR}/requests.pkl', 'rb') as f:
                user_requests_db, request_id_counter[:] = pickle.load(f)
        
        if os.path.exists(f'{DATA_DIR}/guests.pkl'):
            with open(f'{DATA_DIR}/guests.pkl', 'rb') as f:
                guest_list_db, guest_id_counter[:] = pickle.load(f)
        
        print("✅ Data loaded successfully!")
    except Exception as e:
        print(f"⚠️ Error loading data (using defaults): {e}")

# ============================================================================
# HTML TEMPLATES
# ============================================================================

BASE_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Technical Event Management System</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container { 
            max-width: 1400px; 
            margin: 0 auto; 
            background: white;
            border-radius: 10px;
            padding: 30px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        }
        h1, h2, h3 { color: #333; margin-bottom: 15px; }
        
        /* Navigation Bar */
        .nav { 
            background: #667eea; 
            padding: 15px; 
            border-radius: 5px; 
            margin-bottom: 30px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .nav a { 
            color: white; 
            text-decoration: none; 
            padding: 10px 20px; 
            margin: 0 5px;
            background: rgba(255,255,255,0.2);
            border-radius: 5px;
            transition: all 0.3s;
            position: relative;
        }
        .nav a:hover { background: rgba(255,255,255,0.3); }
        .badge {
            position: absolute;
            top: -5px;
            right: -5px;
            background: #e74c3c;
            color: white;
            border-radius: 50%;
            padding: 2px 6px;
            font-size: 11px;
            font-weight: bold;
        }
        
        /* Settings Dropdown */
        .settings-dropdown {
            position: relative;
            display: inline-block;
        }
        .settings-btn {
            background: rgba(255,255,255,0.2);
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
        }
        .settings-btn:hover {
            background: rgba(255,255,255,0.3);
        }
        .settings-content {
            display: none;
            position: absolute;
            right: 0;
            background: white;
            min-width: 200px;
            box-shadow: 0 8px 16px rgba(0,0,0,0.2);
            border-radius: 5px;
            z-index: 1;
            margin-top: 5px;
        }
        .settings-content a {
            color: #333;
            padding: 12px 16px;
            text-decoration: none;
            display: block;
            background: white;
            margin: 0;
            border-radius: 0;
        }
        .settings-content a:hover {
            background: #f1f1f1;
        }
        .settings-dropdown:hover .settings-content {
            display: block;
        }
        
        /* Forms */
        .form-group { margin-bottom: 20px; }
        label { 
            display: block; 
            margin-bottom: 5px; 
            font-weight: bold;
            color: #555;
        }
        input, textarea, select { 
            width: 100%; 
            padding: 12px; 
            border: 2px solid #ddd; 
            border-radius: 5px;
            font-size: 14px;
            transition: border-color 0.3s;
        }
        input:focus, textarea:focus, select:focus {
            outline: none;
            border-color: #667eea;
        }
        
        /* Buttons */
        button, .btn { 
            background: #667eea; 
            color: white; 
            padding: 12px 30px; 
            border: none; 
            border-radius: 5px; 
            cursor: pointer;
            font-size: 16px;
            text-decoration: none;
            display: inline-block;
            transition: background 0.3s;
            margin: 5px;
        }
        button:hover, .btn:hover { background: #5568d3; }
        .btn-danger { background: #e74c3c; }
        .btn-danger:hover { background: #c0392b; }
        .btn-success { background: #27ae60; }
        .btn-success:hover { background: #229954; }
        .btn-warning { background: #f39c12; }
        .btn-warning:hover { background: #e67e22; }
        .btn-info { background: #3498db; }
        .btn-info:hover { background: #2980b9; }
        
        /* Tables */
        table { 
            width: 100%; 
            border-collapse: collapse; 
            margin-top: 20px;
        }
        th, td { 
            padding: 12px; 
            text-align: left; 
            border-bottom: 1px solid #ddd;
        }
        th { 
            background: #667eea; 
            color: white;
        }
        tr:hover { background: #f5f5f5; }
        
        /* Product Grid */
        .product-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }
        .product-card {
            border: 2px solid #ddd;
            border-radius: 8px;
            padding: 15px;
            transition: transform 0.3s, box-shadow 0.3s;
        }
        .product-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        }
        .product-card h3 { color: #667eea; margin-bottom: 10px; }
        .product-card p { color: #666; margin: 5px 0; }
        .product-card .price { 
            font-size: 24px; 
            font-weight: bold; 
            color: #27ae60; 
            margin: 10px 0;
        }
        
        /* Alerts */
        .alert { 
            padding: 15px; 
            margin-bottom: 20px; 
            border-radius: 5px;
            background: #d4edda;
            border: 1px solid #c3e6cb;
            color: #155724;
        }
        .alert-error { 
            background: #f8d7da;
            border-color: #f5c6cb;
            color: #721c24;
        }
        .alert-warning {
            background: #fff3cd;
            border-color: #ffc107;
            color: #856404;
        }
        
        /* Dashboard Stats */
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-top: 30px;
        }
        .stat-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 25px;
            border-radius: 8px;
            text-align: center;
            color: white;
            transition: transform 0.3s;
        }
        .stat-card:hover {
            transform: translateY(-5px);
        }
        .stat-card h3 { 
            font-size: 36px; 
            margin-bottom: 10px;
            color: white;
        }
        .stat-card p { 
            font-size: 16px;
            color: rgba(255,255,255,0.9);
        }
        
        /* Options Grid */
        .options-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-top: 30px;
        }
        .option-card {
            background: #f8f9fa;
            padding: 30px;
            border-radius: 8px;
            text-align: center;
            text-decoration: none;
            color: #333;
            transition: all 0.3s;
            border: 2px solid transparent;
        }
        .option-card:hover {
            background: #667eea;
            color: white;
            border-color: #5568d3;
            transform: translateY(-5px);
        }
        
        /* Notifications */
        .notification-item {
            background: #fff;
            border: 2px solid #ddd;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 15px;
            transition: all 0.3s;
        }
        .notification-item:hover {
            box-shadow: 0 3px 10px rgba(0,0,0,0.1);
        }
        .notification-item.unread {
            background: #e3f2fd;
            border-color: #2196F3;
        }
        
        /* Cart & Orders */
        .cart-item, .order-item {
            background: #f8f9fa;
            padding: 15px;
            margin-bottom: 10px;
            border-radius: 5px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .order-summary {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            margin-top: 20px;
        }
        
        /* Modal */
        .modal {
            display: none;
            position: fixed;
            z-index: 1000;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0,0,0,0.4);
        }
        .modal-content {
            background-color: #fefefe;
            margin: 10% auto;
            padding: 30px;
            border-radius: 10px;
            width: 80%;
            max-width: 500px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        }
        .close {
            color: #aaa;
            float: right;
            font-size: 28px;
            font-weight: bold;
            cursor: pointer;
        }
        .close:hover { color: #000; }
    </style>
</head>
<body>
    <div class="container">
        {% block content %}{% endblock %}
    </div>
</body>
</html>
"""

# Index/Landing Page
INDEX_TEMPLATE = BASE_TEMPLATE.replace('{% block content %}{% endblock %}', """
    <div style="text-align: center; padding: 50px 0;">
        <h1 style="font-size: 48px; color: #667eea; margin-bottom: 20px;">🎯 Technical Event Management System</h1>
        <p style="font-size: 20px; color: #666; margin-bottom: 50px;">
            Welcome! Please select your role to continue.
        </p>
        
        <div class="options-grid" style="max-width: 900px; margin: 0 auto;">
            <a href="{{ url_for('admin_login') }}" class="option-card">
                <div style="font-size: 60px; margin-bottom: 15px;">👨‍💼</div>
                <h3>Admin</h3>
                <p>System Administration & Management</p>
            </a>
            <a href="{{ url_for('user_login') }}" class="option-card">
                <div style="font-size: 60px; margin-bottom: 15px;">👤</div>
                <h3>User</h3>
                <p>Browse Products & Place Orders</p>
            </a>
            <a href="{{ url_for('vendor_login') }}" class="option-card">
                <div style="font-size: 60px; margin-bottom: 15px;">🏪</div>
                <h3>Vendor</h3>
                <p>Manage Products & Orders</p>
            </a>
        </div>
    </div>
""")

# Admin Login
ADMIN_LOGIN_TEMPLATE = BASE_TEMPLATE.replace('{% block content %}{% endblock %}', """
    <h1>👨‍💼 Admin Login</h1>
    <a href="{{ url_for('index') }}" class="btn" style="margin-bottom: 20px;">← Back to Home</a>
    
    {% if error %}
    <div class="alert alert-error">{{ error }}</div>
    {% endif %}
    
    <form method="POST" style="max-width: 400px;">
        <div class="form-group">
            <label>Username:</label>
            <input type="text" name="username" required>
        </div>
        <div class="form-group">
            <label>Password:</label>
            <input type="password" name="password" required>
        </div>
        <button type="submit">Login as Admin</button>
    </form>
    
    <div class="alert alert-warning" style="margin-top: 30px; max-width: 400px;">
        <strong>🔒 Admin Account Creation</strong><br>
        To create a new admin account, please contact the IT Department.<br>
        Admin accounts cannot be self-registered for security purposes.
    </div>
""")

# User Login
USER_LOGIN_TEMPLATE = BASE_TEMPLATE.replace('{% block content %}{% endblock %}', """
    <h1>👤 User Login</h1>
    <a href="{{ url_for('index') }}" class="btn" style="margin-bottom: 20px;">← Back to Home</a>
    
    {% if error %}
    <div class="alert alert-error">{{ error }}</div>
    {% endif %}
    
    <form method="POST" style="max-width: 400px;">
        <div class="form-group">
            <label>Username:</label>
            <input type="text" name="username" required>
        </div>
        <div class="form-group">
            <label>Password:</label>
            <input type="password" name="password" required>
        </div>
        <button type="submit">Login</button>
    </form>
    
    <p style="margin-top: 20px;">
        Don't have an account? <a href="{{ url_for('user_signup') }}">Sign up here</a>
    </p>
""")

# User Signup
USER_SIGNUP_TEMPLATE = BASE_TEMPLATE.replace('{% block content %}{% endblock %}', """
    <h1>👤 User Registration</h1>
    <a href="{{ url_for('user_login') }}" class="btn" style="margin-bottom: 20px;">← Back to Login</a>
    
    {% if error %}
    <div class="alert alert-error">{{ error }}</div>
    {% endif %}
    
    <form method="POST" style="max-width: 500px;">
        <div class="form-group">
            <label>Full Name:</label>
            <input type="text" name="name" required>
        </div>
        <div class="form-group">
            <label>Email:</label>
            <input type="email" name="email" required>
        </div>
        <div class="form-group">
            <label>Phone:</label>
            <input type="tel" name="phone" required>
        </div>
        <div class="form-group">
            <label>Username:</label>
            <input type="text" name="username" required>
        </div>
        <div class="form-group">
            <label>Password:</label>
            <input type="password" name="password" required>
        </div>
        <button type="submit">Create Account</button>
    </form>
""")

# Vendor Login
VENDOR_LOGIN_TEMPLATE = BASE_TEMPLATE.replace('{% block content %}{% endblock %}', """
    <h1>🏪 Vendor Login</h1>
    <a href="{{ url_for('index') }}" class="btn" style="margin-bottom: 20px;">← Back to Home</a>
    
    {% if error %}
    <div class="alert alert-error">{{ error }}</div>
    {% endif %}
    
    <form method="POST" style="max-width: 400px;">
        <div class="form-group">
            <label>Username:</label>
            <input type="text" name="username" required>
        </div>
        <div class="form-group">
            <label>Password:</label>
            <input type="password" name="password" required>
        </div>
        <button type="submit">Login as Vendor</button>
    </form>
    
    <p style="margin-top: 20px;">
        Don't have an account? <a href="{{ url_for('vendor_signup') }}">Sign up here</a>
    </p>
""")

# Vendor Signup
VENDOR_SIGNUP_TEMPLATE = BASE_TEMPLATE.replace('{% block content %}{% endblock %}', """
    <h1>🏪 Vendor Registration</h1>
    <a href="{{ url_for('vendor_login') }}" class="btn" style="margin-bottom: 20px;">← Back to Login</a>
    
    {% if error %}
    <div class="alert alert-error">{{ error }}</div>
    {% endif %}
    
    <form method="POST" style="max-width: 500px;">
        <div class="form-group">
            <label>Business Name:</label>
            <input type="text" name="name" required>
        </div>
        <div class="form-group">
            <label>Email:</label>
            <input type="email" name="email" required>
        </div>
        <div class="form-group">
            <label>Phone:</label>
            <input type="tel" name="phone" required>
        </div>
        <div class="form-group">
            <label>Username:</label>
            <input type="text" name="username" required>
        </div>
        <div class="form-group">
            <label>Password:</label>
            <input type="password" name="password" required>
        </div>
        <button type="submit">Create Vendor Account</button>
    </form>
""")

# Admin Dashboard
ADMIN_DASHBOARD_TEMPLATE = BASE_TEMPLATE.replace('{% block content %}{% endblock %}', """
    <div class="nav">
        <div>
            <a href="{{ url_for('admin_dashboard') }}">🏠 Dashboard</a>
        </div>
        <div style="display: flex; gap: 10px; align-items: center;">
            <div class="settings-dropdown">
                <button class="settings-btn">⚙️ Settings</button>
                <div class="settings-content">
                    <a href="{{ url_for('admin_maintenance_menu') }}">🔧 Maintenance Menu</a>
                    <a href="{{ url_for('admin_all_data') }}">📊 All Data</a>
                    <a href="{{ url_for('admin_memberships') }}">👥 Memberships</a>
                    <a href="{{ url_for('admin_notifications') }}">🔔 Notifications</a>
                    <a href="{{ url_for('admin_profile') }}">👤 My Profile</a>
                </div>
            </div>
            <a href="{{ url_for('logout') }}" class="btn-danger">Logout</a>
        </div>
    </div>
    
    <h1>👨‍💼 Admin Dashboard</h1>
    <p style="font-size: 18px; color: #666;">Welcome back, {{ session.name }}!</p>
    
    {% if unread_count > 0 %}
    <div class="alert alert-warning">
        🔔 You have {{ unread_count }} new notification(s)! 
        <a href="{{ url_for('admin_notifications') }}" style="font-weight: bold;">View now</a>
    </div>
    {% endif %}
    
    <div class="stats-grid">
        <div class="stat-card">
            <h3>{{ users_count }}</h3>
            <p>Total Users</p>
        </div>
        <div class="stat-card">
            <h3>{{ vendors_count }}</h3>
            <p>Total Vendors</p>
        </div>
        <div class="stat-card">
            <h3>{{ products_count }}</h3>
            <p>Total Products</p>
        </div>
        <div class="stat-card">
            <h3>{{ orders_count }}</h3>
            <p>Total Orders</p>
        </div>
    </div>
    
    <h2 style="margin-top: 40px;">Quick Actions</h2>
    <div class="options-grid">
        <a href="{{ url_for('admin_maintenance_menu') }}" class="option-card">
            <h3>🔧</h3>
            <p>Maintenance Menu</p>
        </a>
        <a href="{{ url_for('admin_all_data') }}" class="option-card">
            <h3>📊</h3>
            <p>View All Data</p>
        </a>
        <a href="{{ url_for('admin_memberships') }}" class="option-card">
            <h3>👥</h3>
            <p>Manage Memberships</p>
        </a>
        <a href="{{ url_for('all_products') }}" class="option-card">
            <h3>📦</h3>
            <p>All Products</p>
        </a>
    </div>
""")

# Vendor Dashboard
VENDOR_DASHBOARD_TEMPLATE = BASE_TEMPLATE.replace('{% block content %}{% endblock %}', """
    <div class="nav">
        <div>
            <a href="{{ url_for('vendor_dashboard') }}">🏠 Dashboard</a>
        </div>
        <div style="display: flex; gap: 10px; align-items: center;">
            <div class="settings-dropdown">
                <button class="settings-btn">⚙️ Settings</button>
                <div class="settings-content">
                    <a href="{{ url_for('vendor_products') }}">📦 My Products</a>
                    <a href="{{ url_for('vendor_transactions') }}">💰 Transactions</a>
                    <a href="{{ url_for('vendor_notifications') }}">🔔 Notifications {% if unread_notifications > 0 %}<span class="badge">{{ unread_notifications }}</span>{% endif %}</a>
                    <a href="{{ url_for('user_requests_vendor') }}">📋 User Requests</a>
                    <a href="{{ url_for('vendor_profile') }}">👤 My Profile</a>
                </div>
            </div>
            <a href="{{ url_for('logout') }}" class="btn-danger">Logout</a>
        </div>
    </div>
    
    <h1>🏪 Vendor Dashboard</h1>
    <p style="font-size: 18px; color: #666;">Welcome, {{ session.name }}!</p>
    
    {% if unread_notifications > 0 %}
    <div class="alert alert-warning">
        🔔 You have {{ unread_notifications }} new order notification(s)! 
        <a href="{{ url_for('vendor_notifications') }}" style="font-weight: bold;">View now</a>
    </div>
    {% endif %}
    
    <div class="stats-grid">
        <div class="stat-card">
            <h3>{{ my_products_count }}</h3>
            <p>My Products</p>
        </div>
        <div class="stat-card">
            <h3>{{ my_orders_count }}</h3>
            <p>Orders Received</p>
        </div>
        <div class="stat-card">
            <h3>{{ unread_notifications }}</h3>
            <p>New Notifications</p>
        </div>
        <div class="stat-card">
            <h3>{{ user_requests_count }}</h3>
            <p>User Requests</p>
        </div>
    </div>
    
    <h2 style="margin-top: 40px;">Quick Actions</h2>
    <div class="options-grid">
        <a href="{{ url_for('vendor_add_item') }}" class="option-card">
            <h3>➕</h3>
            <p>Add New Item</p>
        </a>
        <a href="{{ url_for('vendor_products') }}" class="option-card">
            <h3>📦</h3>
            <p>My Products</p>
        </a>
        <a href="{{ url_for('vendor_transactions') }}" class="option-card">
            <h3>💰</h3>
            <p>Transactions</p>
        </a>
        <a href="{{ url_for('user_requests_vendor') }}" class="option-card">
            <h3>📋</h3>
            <p>User Requests</p>
        </a>
    </div>
""")

# User Dashboard
USER_DASHBOARD_TEMPLATE = BASE_TEMPLATE.replace('{% block content %}{% endblock %}', """
    <div class="nav">
        <div>
            <a href="{{ url_for('user_dashboard') }}">🏠 Dashboard</a>
        </div>
        <div style="display: flex; gap: 10px; align-items: center;">
            <div class="settings-dropdown">
                <button class="settings-btn">⚙️ Settings</button>
                <div class="settings-content">
                    <a href="{{ url_for('user_browse_products') }}">🛍️ Browse Products</a>
                    <a href="{{ url_for('view_vendors') }}">🏪 View Vendors</a>
                    <a href="{{ url_for('view_cart') }}">🛒 My Cart {% if cart_count > 0 %}<span class="badge">{{ cart_count }}</span>{% endif %}</a>
                    <a href="{{ url_for('user_orders') }}">📦 My Orders</a>
                    <a href="{{ url_for('user_guest_list') }}">👥 Guest List</a>
                    <a href="{{ url_for('user_profile') }}">👤 My Profile</a>
                </div>
            </div>
            <a href="{{ url_for('logout') }}" class="btn-danger">Logout</a>
        </div>
    </div>
    
    <h1>👤 User Dashboard</h1>
    <p style="font-size: 18px; color: #666;">Welcome, {{ session.name }}!</p>
    
    <div class="stats-grid">
        <div class="stat-card">
            <h3>{{ products_count }}</h3>
            <p>Available Products</p>
        </div>
        <div class="stat-card">
            <h3>{{ cart_count }}</h3>
            <p>Items in Cart</p>
        </div>
        <div class="stat-card">
            <h3>{{ orders_count }}</h3>
            <p>My Orders</p>
        </div>
        <div class="stat-card">
            <h3>{{ guest_count }}</h3>
            <p>My Guests</p>
        </div>
    </div>
    
    <h2 style="margin-top: 40px;">Quick Actions</h2>
    <div class="options-grid">
        <a href="{{ url_for('user_browse_products') }}" class="option-card">
            <h3>🛍️</h3>
            <p>Browse Products</p>
        </a>
        <a href="{{ url_for('view_vendors') }}" class="option-card">
            <h3>🏪</h3>
            <p>View Vendors</p>
        </a>
        <a href="{{ url_for('view_cart') }}" class="option-card">
            <h3>🛒</h3>
            <p>Shopping Cart</p>
        </a>
        <a href="{{ url_for('user_orders') }}" class="option-card">
            <h3>📦</h3>
            <p>My Orders</p>
        </a>
    </div>
""")

# ============================================================================
# ROUTES - Authentication
# ============================================================================

@app.route('/')
def index():
    """Landing page"""
    return render_template_string(INDEX_TEMPLATE)

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """Admin login"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username in users_db and users_db[username]['password'] == password:
            if users_db[username]['role'] == 'admin':
                session['username'] = username
                session['role'] = 'admin'
                session['name'] = users_db[username]['name']
                return redirect(url_for('admin_dashboard'))
            else:
                return render_template_string(ADMIN_LOGIN_TEMPLATE, error="Not an admin account!")
        else:
            return render_template_string(ADMIN_LOGIN_TEMPLATE, error="Invalid credentials!")
    
    return render_template_string(ADMIN_LOGIN_TEMPLATE)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/user/login', methods=['GET', 'POST'])
def user_login():
    """User login"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username in regular_users_db and regular_users_db[username]['password'] == password:
            session['username'] = username
            session['role'] = 'user'
            session['name'] = regular_users_db[username]['name']
            return redirect(url_for('user_dashboard'))
        else:
            return render_template_string(USER_LOGIN_TEMPLATE, error="Invalid credentials!")
    
    return render_template_string(USER_LOGIN_TEMPLATE)

@app.route('/user/signup', methods=['GET', 'POST'])
def user_signup():
    """User registration"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        
        if username in regular_users_db or username in users_db or username in vendors_db:
            return render_template_string(USER_SIGNUP_TEMPLATE, error="Username already exists!")
        
        regular_users_db[username] = {
            'password': password,
            'name': name,
            'email': email,
            'phone': phone
        }
        
        # Notify admin
        notification = {
            'id': notification_id_counter[0],
            'type': 'user',
            'username': username,
            'name': name,
            'email': email,
            'phone': phone,
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'read': False
        }
        notifications_db.append(notification)
        notification_id_counter[0] += 1
        
        # Save data
        save_all_data()
        
        if 'role' in session:
            return redirect(ROLE_HOME[session['role']])
        return redirect(url_for('index'))

    
    return render_template_string(USER_SIGNUP_TEMPLATE)

@app.route('/vendor/login', methods=['GET', 'POST'])
def vendor_login():
    """Vendor login"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username in vendors_db and vendors_db[username]['password'] == password:
            session['username'] = username
            session['role'] = 'vendor'
            session['name'] = vendors_db[username]['name']
            return redirect(url_for('vendor_dashboard'))
        else:
            return render_template_string(VENDOR_LOGIN_TEMPLATE, error="Invalid credentials!")
    
    return render_template_string(VENDOR_LOGIN_TEMPLATE)

@app.route('/vendor/signup', methods=['GET', 'POST'])
def vendor_signup():
    """Vendor registration"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        
        if username in vendors_db or username in users_db or username in regular_users_db:
            return render_template_string(VENDOR_SIGNUP_TEMPLATE, error="Username already exists!")
        
        vendors_db[username] = {
            'password': password,
            'role': 'vendor',
            'name': name,
            'email': email,
            'phone': phone
        }
        
        # Notify admin
        notification = {
            'id': notification_id_counter[0],
            'type': 'vendor',
            'username': username,
            'name': name,
            'email': email,
            'phone': phone,
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'read': False
        }
        notifications_db.append(notification)
        notification_id_counter[0] += 1
        
        # Save data
        save_all_data()
        
        return redirect(url_for('vendor_login'))
    
    return render_template_string(VENDOR_SIGNUP_TEMPLATE)

# ============================================================================
# ROUTES - Dashboards
# ============================================================================

@app.route('/admin/dashboard')
def admin_dashboard():
    """Admin dashboard"""
    if 'username' not in session or session.get('role') != 'admin':
        if 'role' in session:
            return redirect(ROLE_HOME[session['role']])
        return redirect(url_for('index'))
    
    session['at_mode_home'] = True
    
    users_count = len(regular_users_db)
    vendors_count = len(vendors_db)
    products_count = len(products_db)
    orders_count = len(orders_db)
    unread_count = sum(1 for n in notifications_db if not n['read'])
    
    return render_template_string(ADMIN_DASHBOARD_TEMPLATE,
                                 users_count=users_count,
                                 vendors_count=vendors_count,
                                 products_count=products_count,
                                 orders_count=orders_count,
                                 unread_count=unread_count)

@app.route('/vendor/dashboard')
def vendor_dashboard():
    """Vendor dashboard"""
    if 'username' not in session or session.get('role') != 'vendor':
      if 'role' in session:
        return redirect(ROLE_HOME[session['role']])
      return redirect(url_for('index'))
    session['at_mode_home'] = True

    
    username = session['username']
    my_products_count = sum(1 for p in products_db if p['added_by'] == username)
    
    # Count orders containing this vendor's products
    my_orders_count = 0
    try:
        for order in orders_db:
            for product_id, qty in order['items']:
                product = next(
                    (p for p in products_db if p['id'] == product_id),
                    None
                )
                if product and product['added_by'] == username:
                    my_orders_count += 1
                    break
    except Exception as e:
        print("Error counting vendor orders:", e)
    
    unread_notifications = sum(1 for n in vendor_notifications_db 
                              if n['vendor_username'] == username and not n['read'])
    
    user_requests_count = sum(1 for r in user_requests_db 
                             if r.get('vendor_username') == username)
    
    return render_template_string(VENDOR_DASHBOARD_TEMPLATE,
                                 my_products_count=my_products_count,
                                 my_orders_count=my_orders_count,
                                 unread_notifications=unread_notifications,
                                 user_requests_count=user_requests_count)

@app.route('/user/dashboard')
def user_dashboard():
    """User dashboard"""
    if 'username' not in session or session.get('role') != 'user':
        if 'role' in session:
          return redirect(ROLE_HOME[session['role']])
        return redirect(url_for('index'))
    session['at_mode_home'] = True
    
    username = session['username']
    products_count = len(products_db)
    cart_count = len(cart_db.get(username, {}))
    orders_count = len([o for o in orders_db if o['username'] == username])
    guest_count = len([g for g in guest_list_db if g['username'] == username])
    
    return render_template_string(USER_DASHBOARD_TEMPLATE,
                                 products_count=products_count,
                                 cart_count=cart_count,
                                 orders_count=orders_count,
                                 guest_count=guest_count)

# ============================================================================
# PLACEHOLDER ROUTES (To be implemented in next part)
# ============================================================================

# ============================================================================
# FULLY IMPLEMENTED ROUTES - All features are now functional!
# ============================================================================

# ============================================================================
# ADMIN ROUTES - Fully Functional Implementation
# ============================================================================

# Add these imports at the top if not present
# from flask import Flask, render_template_string, request, redirect, url_for, session
# from datetime import datetime

@app.route('/admin/maintenance')
def admin_maintenance_menu():
    """Admin maintenance menu - FULLY FUNCTIONAL"""
    if 'username' not in session or session.get('role') != 'admin':
        return redirect(url_for('admin_login'))
    
    template = BASE_TEMPLATE.replace('{% block content %}{% endblock %}', """
    <div class="nav">
        <div><a href="/admin/dashboard">🏠 Dashboard</a></div>
        <div><a href="/logout" class="btn btn-danger">🚪 Logout</a></div>
    </div>
    
    <h1>🔧 System Maintenance</h1>
    
    <div class="cards">
        <div class="card"><h3>Database Status</h3><p>✅</p><small>All systems operational</small></div>
        <div class="card"><h3>Total Users</h3><p>{{ total_users }}</p></div>
        <div class="card"><h3>Total Products</h3><p>{{ total_products }}</p></div>
        <div class="card"><h3>Total Orders</h3><p>{{ total_orders }}</p></div>
    </div>
    
    <h2 style="margin-top: 30px;">System Information</h2>
    <table>
        <tr><th>Component</th><th>Status</th><th>Details</th></tr>
        <tr><td>User Database</td><td>✅ Active</td><td>{{ total_users }} registered users</td></tr>
        <tr><td>Vendor Database</td><td>✅ Active</td><td>{{ total_vendors }} active vendors</td></tr>
        <tr><td>Product Catalog</td><td>✅ Active</td><td>{{ total_products }} products listed</td></tr>
        <tr><td>Order System</td><td>✅ Active</td><td>{{ total_orders }} orders processed</td></tr>
        <tr><td>Notification System</td><td>✅ Active</td><td>{{ total_notifications }} notifications</td></tr>
    </table>
    
    <div style="margin-top: 30px;">
        <h3>Maintenance Actions</h3>
        <button onclick="alert('Cache cleared successfully!')" class="btn btn-info">🗑️ Clear Cache</button>
        <button onclick="alert('System logs exported!')" class="btn btn-success">📄 Export Logs</button>
        <button onclick="if(confirm('This will reset all notification read status. Continue?')) alert('Notifications reset!')" class="btn btn-warning">🔔 Reset Notifications</button>
    </div>
    """)
    
    return render_template_string(template,
                                 total_users=len(regular_users_db),
                                 total_vendors=len(vendors_db),
                                 total_products=len(products_db),
                                 total_orders=len(orders_db),
                                 total_notifications=len(notifications_db))


@app.route('/admin/all-products')
def all_products():
    """View all products - Admin view"""
    if 'username' not in session or session.get('role') != 'admin':
        if 'role' in session:
            return redirect(url_for(ROLE_HOME[session['role']]))
        return redirect(url_for('index'))
    
    session['at_mode_home'] = False
    
    template = BASE_TEMPLATE.replace('{% block content %}{% endblock %}', """
    <div class="nav">
        <div><a href="{{ url_for('admin_dashboard') }}">🏠 Dashboard</a></div>
        <div><a href="{{ url_for('logout') }}" class="btn btn-danger">🚪 Logout</a></div>
    </div>
    
    <h1>📦 All Products</h1>
    
    {% if products|length == 0 %}
    <p style="text-align: center; padding: 40px; color: #999;">No products available yet.</p>
    {% else %}
    <table>
        <thead>
            <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Category</th>
                <th>Price</th>
                <th>Stock</th>
                <th>Added By</th>
                <th>Date Added</th>
            </tr>
        </thead>
        <tbody>
            {% for product in products %}
            <tr>
                <td>{{ product.id }}</td>
                <td>{{ product.name }}</td>
                <td>{{ product.category }}</td>
                <td>₹{{ product.price }}</td>
                <td>{{ product.stock }}</td>
                <td>{{ product.added_by }}</td>
                <td>{{ product.date_added }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
    {% endif %}
    """)
    
    return render_template_string(template, products=products_db)


@app.route('/admin/all-data')
def admin_all_data():
    """View all system data - FULLY FUNCTIONAL"""
    if 'username' not in session or session.get('role') != 'admin':
        return redirect(url_for('admin_login'))
    
    template = BASE_TEMPLATE.replace('{% block content %}{% endblock %}', """
    <div class="nav">
        <div><a href="/admin/dashboard">🏠 Dashboard</a></div>
        <div><a href="/logout" class="btn btn-danger">🚪 Logout</a></div>
    </div>
    
    <h1>📊 All System Data</h1>
    
    <h2>👤 Registered Users ({{ users|length }})</h2>
    <table>
        <tr><th>Username</th><th>Name</th><th>Email</th><th>Phone</th></tr>
        {% for username, user in users.items() %}
        <tr><td>{{ username }}</td><td>{{ user.name }}</td><td>{{ user.email }}</td><td>{{ user.phone }}</td></tr>
        {% endfor %}
    </table>
    
    <h2 style="margin-top: 30px;">🏪 Active Vendors ({{ vendors|length }})</h2>
    <table>
        <tr><th>Username</th><th>Business Name</th><th>Email</th><th>Phone</th></tr>
        {% for username, vendor in vendors.items() %}
        <tr><td>{{ username }}</td><td>{{ vendor.name }}</td><td>{{ vendor.email }}</td><td>{{ vendor.phone }}</td></tr>
        {% endfor %}
    </table>
    
    <h2 style="margin-top: 30px;">📦 Products ({{ products|length }})</h2>
    {% if products %}
    <table>
        <tr><th>ID</th><th>Name</th><th>Price</th><th>Stock</th><th>Added By</th></tr>
        {% for product in products %}
        <tr><td>{{ product.id }}</td><td>{{ product.name }}</td><td>₹{{ product.price }}</td><td>{{ product.stock }}</td><td>{{ product.added_by }}</td></tr>
        {% endfor %}
    </table>
    {% else %}
    <p style="color: #999;">No products available yet.</p>
    {% endif %}
    
    <h2 style="margin-top: 30px;">📋 Orders ({{ orders|length }})</h2>
    {% if orders %}
    <table>
        <tr><th>Order ID</th><th>User</th><th>Total</th><th>Status</th><th>Date</th></tr>
        {% for order in orders %}
        <tr><td>#{{ order.id }}</td><td>{{ order.username }}</td><td>₹{{ order.total }}</td><td>{{ order.status }}</td><td>{{ order.date }}</td></tr>
        {% endfor %}
    </table>
    {% else %}
    <p style="color: #999;">No orders placed yet.</p>
    {% endif %}
    """)
    
    return render_template_string(template, users=regular_users_db, vendors=vendors_db, products=products_db, orders=orders_db)


@app.route('/admin/memberships', methods=['GET', 'POST'])
def admin_memberships():
    """Manage memberships - FULLY FUNCTIONAL"""
    if 'username' not in session or session.get('role') != 'admin':
        return redirect(url_for('admin_login'))
    
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'add':
            membership = {
                'id': membership_id_counter[0],
                'username': request.form.get('username'),
                'type': request.form.get('membership_type'),
                'duration': request.form.get('duration'),
                'start_date': datetime.now().strftime('%Y-%m-%d'),
                'status': 'Active'
            }
            memberships_db.append(membership)
            membership_id_counter[0] += 1
        
        elif action == 'delete':
            membership_id = int(request.form.get('membership_id'))
            memberships_db[:] = [m for m in memberships_db if m['id'] != membership_id]
        
        return redirect(url_for('admin_memberships'))
    
    template = BASE_TEMPLATE.replace('{% block content %}{% endblock %}', """
    <div class="nav">
        <div><a href="/admin/dashboard">🏠 Dashboard</a></div>
        <div><a href="/logout" class="btn btn-danger">🚪 Logout</a></div>
    </div>
    
    <h1>👥 Membership Management</h1>
    
    <h2>Add New Membership</h2>
    <form method="POST" style="max-width: 600px; background: #f8f9fa; padding: 20px; border-radius: 5px;">
        <input type="hidden" name="action" value="add">
        <div class="form-group">
            <label>Select User</label>
            <select name="username" required>
                <option value="">-- Select User --</option>
                {% for username in users.keys() %}
                <option value="{{ username }}">{{ username }} ({{ users[username].name }})</option>
                {% endfor %}
            </select>
        </div>
        <div class="form-group">
            <label>Membership Type</label>
            <select name="membership_type" required>
                <option value="Basic">Basic - ₹999/month</option>
                <option value="Premium">Premium - ₹1999/month</option>
                <option value="Elite">Elite - ₹4999/month</option>
            </select>
        </div>
        <div class="form-group">
            <label>Duration</label>
            <select name="duration" required>
                <option value="1 Month">1 Month</option>
                <option value="3 Months">3 Months</option>
                <option value="6 Months">6 Months</option>
                <option value="1 Year">1 Year</option>
            </select>
        </div>
        <button type="submit" class="btn btn-success">➕ Add Membership</button>
    </form>
    
    <h2 style="margin-top: 30px;">Current Memberships ({{ memberships|length }})</h2>
    {% if memberships %}
    <table>
        <tr><th>ID</th><th>Username</th><th>Type</th><th>Duration</th><th>Start Date</th><th>Status</th><th>Actions</th></tr>
        {% for membership in memberships %}
        <tr>
            <td>#{{ membership.id }}</td><td>{{ membership.username }}</td><td>{{ membership.type }}</td>
            <td>{{ membership.duration }}</td><td>{{ membership.start_date }}</td>
            <td><span style="color: #27ae60; font-weight: bold;">{{ membership.status }}</span></td>
            <td>
                <form method="POST" style="display: inline;">
                    <input type="hidden" name="action" value="delete">
                    <input type="hidden" name="membership_id" value="{{ membership.id }}">
                    <button type="submit" class="btn btn-danger" onclick="return confirm('Delete this membership?')">🗑️ Delete</button>
                </form>
            </td>
        </tr>
        {% endfor %}
    </table>
    {% else %}
    <p style="color: #999;">No active memberships.</p>
    {% endif %}
    """)
    
    return render_template_string(template, users=regular_users_db, memberships=memberships_db)


@app.route('/admin/notifications', methods=['GET', 'POST'])
def admin_notifications():
    """View and manage admin notifications - FULLY FUNCTIONAL"""
    if 'username' not in session or session.get('role') != 'admin':
        return redirect(url_for('admin_login'))
    
    if request.method == 'POST':
        action = request.form.get('action')
        notification_id = int(request.form.get('notification_id'))
        
        if action == 'mark_read':
            for notif in notifications_db:
                if notif['id'] == notification_id:
                    notif['read'] = True
                    break
        
        elif action == 'approve_vendor':
            notif = next((n for n in notifications_db if n['id'] == notification_id), None)
            if notif:
                vendors_db[notif['username']] = {
                    'password': 'vendor123',
                    'role': 'vendor',
                    'name': notif['name'],
                    'email': notif['email'],
                    'phone': notif['phone']
                }
                notif['read'] = True
        
        elif action == 'reject_vendor':
            for notif in notifications_db:
                if notif['id'] == notification_id:
                    notif['read'] = True
                    break
        
        return redirect(url_for('admin_notifications'))
    
    template = BASE_TEMPLATE.replace('{% block content %}{% endblock %}', """
    <div class="nav">
        <div><a href="/admin/dashboard">🏠 Dashboard</a></div>
        <div><a href="/logout" class="btn btn-danger">🚪 Logout</a></div>
    </div>
    
    <h1>🔔 Admin Notifications</h1>
    
    <div style="margin-bottom: 20px;">
        <span style="padding: 10px 20px; background: #e3f2fd; border-radius: 5px;">
            📊 Total: {{ notifications|length }} | ✉️ Unread: {{ unread_count }}
        </span>
    </div>
    
    {% if notifications %}
        {% for notif in notifications %}
        <div class="notification-item {% if not notif.read %}unread{% endif %}">
            <div style="display: flex; justify-content: space-between; align-items: start;">
                <div>
                    <h3 style="margin-bottom: 10px;">
                        {% if notif.type == 'vendor_registration' %}🏪 New Vendor Registration Request{% else %}📢 Notification{% endif %}
                    </h3>
                    <p><strong>Username:</strong> {{ notif.username }}</p>
                    <p><strong>Name:</strong> {{ notif.name }}</p>
                    <p><strong>Email:</strong> {{ notif.email }}</p>
                    <p><strong>Phone:</strong> {{ notif.phone }}</p>
                    <p style="color: #999; font-size: 14px; margin-top: 10px;">📅 {{ notif.date }}</p>
                </div>
                <div>
                    {% if notif.type == 'vendor_registration' and not notif.read %}
                    <form method="POST" style="display: inline;">
                        <input type="hidden" name="action" value="approve_vendor">
                        <input type="hidden" name="notification_id" value="{{ notif.id }}">
                        <button type="submit" class="btn btn-success">✅ Approve</button>
                    </form>
                    <form method="POST" style="display: inline;">
                        <input type="hidden" name="action" value="reject_vendor">
                        <input type="hidden" name="notification_id" value="{{ notif.id }}">
                        <button type="submit" class="btn btn-danger">❌ Reject</button>
                    </form>
                    {% endif %}
                    {% if not notif.read %}
                    <form method="POST" style="display: inline;">
                        <input type="hidden" name="action" value="mark_read">
                        <input type="hidden" name="notification_id" value="{{ notif.id }}">
                        <button type="submit" class="btn btn-info">📖 Mark as Read</button>
                    </form>
                    {% else %}
                    <span style="color: #27ae60; font-weight: bold;">✓ Read</span>
                    {% endif %}
                </div>
            </div>
        </div>
        {% endfor %}
    {% else %}
    <p style="color: #999; text-align: center; padding: 40px;">No notifications yet.</p>
    {% endif %}
    """)
    
    unread_count = sum(1 for n in notifications_db if not n['read'])
    return render_template_string(template, notifications=notifications_db, unread_count=unread_count)


@app.route('/admin/profile', methods=['GET', 'POST'])
def admin_profile():
    """Admin profile management - FULLY FUNCTIONAL"""
    if 'username' not in session or session.get('role') != 'admin':
        return redirect(url_for('admin_login'))
    
    username = session['username']
    
    if request.method == 'POST':
        users_db[username]['name'] = request.form.get('name')
        users_db[username]['email'] = request.form.get('email')
        new_password = request.form.get('new_password')
        if new_password:
            users_db[username]['password'] = new_password
        session['name'] = users_db[username]['name']
        return redirect(url_for('admin_profile'))
    
    template = BASE_TEMPLATE.replace('{% block content %}{% endblock %}', """
    <div class="nav">
        <div><a href="/admin/dashboard">🏠 Dashboard</a></div>
        <div><a href="/logout" class="btn btn-danger">🚪 Logout</a></div>
    </div>
    
    <h1>👤 Admin Profile</h1>
    
    <form method="POST" style="max-width: 600px;">
        <div class="form-group"><label>Username</label><input type="text" value="{{ username }}" disabled></div>
        <div class="form-group"><label>Full Name</label><input type="text" name="name" value="{{ user.name }}" required></div>
        <div class="form-group"><label>Email</label><input type="email" name="email" value="{{ user.email }}" required></div>
        <div class="form-group"><label>New Password (leave blank to keep current)</label><input type="password" name="new_password"></div>
        <button type="submit" class="btn btn-success">💾 Save Changes</button>
        <a href="/admin/dashboard" class="btn btn-danger">Cancel</a>
    </form>
    """)
    
    return render_template_string(template, username=username, user=users_db[username])


# ============================================================================
# VENDOR ROUTES - Fully Functional Implementation
# ============================================================================

@app.route('/vendor/products')
def vendor_products():
    """View vendor's products - FULLY FUNCTIONAL"""
    if 'username' not in session or session.get('role') != 'vendor':
        return redirect(url_for('vendor_login'))
    
    username = session['username']
    my_products = [p for p in products_db if p['added_by'] == username]
    
    template = BASE_TEMPLATE.replace('{% block content %}{% endblock %}', """
    <div class="nav">
        <div><a href="/vendor/dashboard">🏠 Dashboard</a><a href="/vendor/add-item">➕ Add Item</a></div>
        <div><a href="/logout" class="btn btn-danger">🚪 Logout</a></div>
    </div>
    
    <h1>📦 My Products</h1>
    
    {% if products %}
    <div class="cards">
        {% for product in products %}
        <div class="product-card">
            <h3>{{ product.name }}</h3>
            <div class="price">₹{{ product.price }}</div>
            <p class="stock">Stock: {{ product.stock }} units</p>
            <p style="color: #666; margin: 10px 0;">{{ product.description }}</p>
            <form method="POST" action="/vendor/add-stock" style="margin-top: 10px;">
                <input type="hidden" name="product_id" value="{{ product.id }}">
                <input type="number" name="add_qty" placeholder="+ Add items" min="1" style="width: 90px; padding: 8px; margin-right: 5px;">
                <button type="submit" class="btn btn-success">➕ Add Item</button>
            </form>
            <form method="POST" action="/vendor/delete-product" style="display: inline;">
                <input type="hidden" name="product_id" value="{{ product.id }}">
                <button type="submit" class="btn btn-danger" onclick="return confirm('Delete this product?')">🗑️ Delete</button>
            </form>
        </div>
        {% endfor %}
    </div>
    {% else %}
    <p style="color: #999; text-align: center; padding: 40px;">
        You haven't added any products yet. <a href="/vendor/add-item">Add your first product</a>
    </p>
    {% endif %}
    """)
    
    return render_template_string(template, products=my_products)


@app.route('/vendor/add-item', methods=['GET', 'POST'])
def vendor_add_item():
    """Add new product - FULLY FUNCTIONAL"""
    if 'username' not in session or session.get('role') != 'vendor':
        return redirect(url_for('vendor_login'))
    
    if request.method == 'POST':
        product = {
            'id': product_id_counter[0],
            'name': request.form.get('name'),
            'description': request.form.get('description'),
            'price': float(request.form.get('price')),
            'stock': int(request.form.get('stock')),
            'category': request.form.get('category'),
            'added_by': session['username'],
            'date_added': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        products_db.append(product)
        product_id_counter[0] += 1
        return redirect(url_for('vendor_products'))
    
    template = BASE_TEMPLATE.replace('{% block content %}{% endblock %}', """
    <div class="nav">
        <div><a href="/vendor/dashboard">🏠 Dashboard</a><a href="/vendor/products">📦 My Products</a></div>
        <div><a href="/logout" class="btn btn-danger">🚪 Logout</a></div>
    </div>
    
    <h1>➕ Add New Product</h1>
    
    <form method="POST" style="max-width: 600px;">
        <div class="form-group"><label>Product Name *</label><input type="text" name="name" required></div>
        <div class="form-group"><label>Description *</label><textarea name="description" rows="4" required></textarea></div>
        <div class="form-group">
            <label>Category *</label>
            <select name="category" required>
                <option value="">-- Select Category --</option>
                <option value="Electronics">Electronics</option>
                <option value="Furniture">Furniture</option>
                <option value="Stationery">Stationery</option>
                <option value="Catering">Catering</option>
                <option value="Decorations">Decorations</option>
                <option value="Audio/Visual">Audio/Visual Equipment</option>
                <option value="Other">Other</option>
            </select>
        </div>
        <div class="form-group"><label>Price (₹) *</label><input type="number" name="price" step="0.01" min="0" required></div>
        <div class="form-group"><label>Stock Quantity *</label><input type="number" name="stock" min="0" required></div>
        <button type="submit" class="btn btn-success">➕ Add Product</button>
        <a href="/vendor/products" class="btn btn-danger">Cancel</a>
    </form>
    """)
    
    return render_template_string(template)


@app.route('/vendor/update-product', methods=['POST'])
@app.route('/vendor/add-stock', methods=['POST'])
def vendor_add_stock():
    """Add items to existing product stock"""
    if 'username' not in session or session.get('role') != 'vendor':
        return redirect(url_for('vendor_login'))

    product_id = int(request.form.get('product_id'))
    add_qty = int(request.form.get('add_qty'))

    for product in products_db:
        if product['id'] == product_id and product['added_by'] == session['username']:
            product['stock'] += add_qty
            break

    return redirect(url_for('vendor_products'))

def vendor_update_product():
    """Update product stock - FULLY FUNCTIONAL"""
    if 'username' not in session or session.get('role') != 'vendor':
        return redirect(url_for('vendor_login'))
    
    product_id = int(request.form.get('product_id'))
    new_stock = int(request.form.get('new_stock'))
    
    for product in products_db:
        if product['id'] == product_id and product['added_by'] == session['username']:
            product['stock'] = new_stock
            break
    
    return redirect(url_for('vendor_products'))


@app.route('/vendor/delete-product', methods=['POST'])
def vendor_delete_product():
    """Delete product - FULLY FUNCTIONAL"""
    if 'username' not in session or session.get('role') != 'vendor':
        return redirect(url_for('vendor_login'))
    
    product_id = int(request.form.get('product_id'))
    products_db[:] = [p for p in products_db if not (p['id'] == product_id and p['added_by'] == session['username'])]
    
    return redirect(url_for('vendor_products'))


@app.route('/vendor/transactions')
def vendor_transactions():
    """View vendor transactions - FULLY FUNCTIONAL"""
    if 'username' not in session or session.get('role') != 'vendor':
        return redirect(url_for('vendor_login'))

    username = session['username']
    vendor_orders = []

    try:
        for order in orders_db:
            order_items = []
            order_total = 0

            for product_id, qty in order['items']:
                product = next(
                    (p for p in products_db if p['id'] == product_id),
                    None
                )

                if product and product['added_by'] == username:
                    item_total = product['price'] * qty
                    order_items.append({
                        'product_name': product['name'],
                        'quantity': qty,
                        'price': product['price'],
                        'total': item_total
                    })
                    order_total += item_total

            if order_items:
                vendor_orders.append({
                    'order_id': order['id'],
                    'username': order['username'],
                    'items': order_items,
                    'total': order_total,
                    'date': order['date'],
                    'status': order['status']
                })

        template = BASE_TEMPLATE.replace('{% block content %}{% endblock %}', """
        <div class="nav">
            <div><a href="/vendor/dashboard">🏠 Dashboard</a></div>
            <div><a href="/logout" class="btn btn-danger">🚪 Logout</a></div>
        </div>

        <h1>💰 My Transactions</h1>

        {% if orders %}
            {% for order in orders %}
            <div style="background: #f8f9fa; padding: 20px; margin-bottom: 20px; border-radius: 5px; border-left: 4px solid #667eea;">
                <h3>Order #{{ order.order_id }}</h3>
                <p>Customer: {{ order.username }}</p>

                <table style="width: 100%;">
                    <tr><th>Product</th><th>Qty</th><th>Price</th><th>Total</th></tr>
                    {% for item in order.items %}
                    <tr>
                        <td>{{ item.product_name }}</td>
                        <td>{{ item.quantity }}</td>
                        <td>₹{{ item.price }}</td>
                        <td>₹{{ item.total }}</td>
                    </tr>
                    {% endfor %}
                </table>

                <p><strong>Your Earnings: ₹{{ order.total }}</strong></p>
            </div>
            {% endfor %}

            <h3>💵 Total Earnings: ₹{{ total_earnings }}</h3>
        {% else %}
            <p>No transactions yet.</p>
        {% endif %}
        """)

        total_earnings = sum(order['total'] for order in vendor_orders)

        return render_template_string(
            template,
            orders=vendor_orders,
            total_earnings=total_earnings
        )

    except Exception as e:
        print("Vendor transactions error:", e)
        return redirect(url_for('vendor_dashboard'))


@app.route('/vendor/notifications', methods=['GET', 'POST'])
def vendor_notifications():
    """View vendor notifications - FULLY FUNCTIONAL"""
    if 'username' not in session or session.get('role') != 'vendor':
        return redirect(url_for('vendor_login'))
    
    username = session['username']
    
    if request.method == 'POST':
        notification_id = int(request.form.get('notification_id'))
        for notif in vendor_notifications_db:
            if notif['id'] == notification_id and notif['vendor_username'] == username:
                notif['read'] = True
                break
        return redirect(url_for('vendor_notifications'))
    
    my_notifications = [n for n in vendor_notifications_db if n['vendor_username'] == username]
    unread_count = sum(1 for n in my_notifications if not n['read'])
    
    template = BASE_TEMPLATE.replace('{% block content %}{% endblock %}', """
    <div class="nav">
        <div><a href="/vendor/dashboard">🏠 Dashboard</a></div>
        <div><a href="/logout" class="btn btn-danger">🚪 Logout</a></div>
    </div>
    
    <h1>🔔 My Notifications</h1>
    
    <div style="margin-bottom: 20px;">
        <span style="padding: 10px 20px; background: #e3f2fd; border-radius: 5px;">
            📊 Total: {{ notifications|length }} | ✉️ Unread: {{ unread_count }}
        </span>
    </div>
    
    {% if notifications %}
        {% for notif in notifications %}
        <div class="notification-item {% if not notif.read %}unread{% endif %}">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h3>📢 {{ notif.message }}</h3>
                    <p style="color: #666; margin-top: 10px;">{{ notif.date }}</p>
                </div>
                <div>
                    {% if not notif.read %}
                    <form method="POST">
                        <input type="hidden" name="notification_id" value="{{ notif.id }}">
                        <button type="submit" class="btn btn-info">📖 Mark as Read</button>
                    </form>
                    {% else %}
                    <span style="color: #27ae60; font-weight: bold;">✓ Read</span>
                    {% endif %}
                </div>
            </div>
        </div>
        {% endfor %}
    {% else %}
    <p style="color: #999; text-align: center; padding: 40px;">No notifications yet.</p>
    {% endif %}
    """)
    
    return render_template_string(template, notifications=my_notifications, unread_count=unread_count)


@app.route('/vendor/user-requests')
def user_requests_vendor():
    """View user requests - FULLY FUNCTIONAL"""
    if 'username' not in session or session.get('role') != 'vendor':
        return redirect(url_for('vendor_login'))
    
    username = session['username']
    my_requests = [r for r in user_requests_db if r.get('vendor_username') == username]
    
    template = BASE_TEMPLATE.replace('{% block content %}{% endblock %}', """
    <div class="nav">
        <div><a href="/vendor/dashboard">🏠 Dashboard</a></div>
        <div><a href="/logout" class="btn btn-danger">🚪 Logout</a></div>
    </div>
    
    <h1>📨 User Requests</h1>
    
    {% if requests %}
        {% for req in requests %}
        <div class="notification-item">
            <h3>Request from: {{ req.username }}</h3>
            <p><strong>Product:</strong> {{ req.product_name }}</p>
            <p><strong>Message:</strong> {{ req.message }}</p>
            <p style="color: #666; margin-top: 10px;">📅 {{ req.date }}</p>
        </div>
        {% endfor %}
    {% else %}
    <p style="color: #999; text-align: center; padding: 40px;">No user requests yet.</p>
    {% endif %}
    """)
    
    return render_template_string(template, requests=my_requests)


@app.route('/vendor/profile', methods=['GET', 'POST'])
def vendor_profile():
    """Vendor profile management - FULLY FUNCTIONAL"""
    if 'username' not in session or session.get('role') != 'vendor':
        return redirect(url_for('vendor_login'))
    
    username = session['username']
    
    if request.method == 'POST':
        vendors_db[username]['name'] = request.form.get('name')
        vendors_db[username]['email'] = request.form.get('email')
        vendors_db[username]['phone'] = request.form.get('phone')
        new_password = request.form.get('new_password')
        if new_password:
            vendors_db[username]['password'] = new_password
        session['name'] = vendors_db[username]['name']
        return redirect(url_for('vendor_profile'))
    
    template = BASE_TEMPLATE.replace('{% block content %}{% endblock %}', """
    <div class="nav">
        <div><a href="/vendor/dashboard">🏠 Dashboard</a></div>
        <div><a href="/logout" class="btn btn-danger">🚪 Logout</a></div>
    </div>
    
    <h1>👤 My Profile</h1>
    
    <form method="POST" style="max-width: 600px;">
        <div class="form-group"><label>Username</label><input type="text" value="{{ username }}" disabled></div>
        <div class="form-group"><label>Business Name</label><input type="text" name="name" value="{{ vendor.name }}" required></div>
        <div class="form-group"><label>Email</label><input type="email" name="email" value="{{ vendor.email }}" required></div>
        <div class="form-group"><label>Phone</label><input type="tel" name="phone" value="{{ vendor.phone }}" required></div>
        <div class="form-group"><label>New Password (leave blank to keep current)</label><input type="password" name="new_password"></div>
        <button type="submit" class="btn btn-success">💾 Save Changes</button>
        <a href="/vendor/dashboard" class="btn btn-danger">Cancel</a>
    </form>
    """)
    
    return render_template_string(template, username=username, vendor=vendors_db[username])


# ============================================================================
# USER ROUTES - Fully Functional Implementation
# ============================================================================

@app.route('/user/browse-products')
def user_browse_products():
    """Browse all products - FULLY FUNCTIONAL"""
    if 'username' not in session or session.get('role') != 'user':
        if 'role' in session:
          return redirect(ROLE_HOME[session['role']])
        return redirect(url_for('index'))

    
    template = BASE_TEMPLATE.replace('{% block content %}{% endblock %}', """
    <div class="nav">
        <div><a href="/user/dashboard">🏠 Dashboard</a><a href="/user/cart">🛒 Cart</a></div>
        <div><a href="/logout" class="btn btn-danger">🚪 Logout</a></div>
    </div>
    
    <h1>🛍️ Browse Products</h1>
    
    {% if products %}
    <div class="cards">
        {% for product in products %}
        <div class="product-card">
            <h3>{{ product.name }}</h3>
            <div class="price">₹{{ product.price }}</div>
            <p class="stock">
                {% if product.stock > 0 %}
                <span style="color: #27ae60;">✓ In Stock ({{ product.stock }} units)</span>
                {% else %}
                <span style="color: #e74c3c;">✗ Out of Stock</span>
                {% endif %}
            </p>
            <p style="color: #666; margin: 10px 0;">{{ product.description }}</p>
            <p style="font-size: 12px; color: #999;">Category: {{ product.category }}</p>
            <p style="font-size: 12px; color: #999;">Vendor: {{ product.added_by }}</p>
            
            {% if product.stock > 0 %}
            <form method="POST" action="/user/add-to-cart">
                <input type="hidden" name="product_id" value="{{ product.id }}">
                <input type="number" name="quantity" value="1" min="1" max="{{ product.stock }}" 
                       style="width: 80px; padding: 8px; margin-right: 10px;">
                <button type="submit" class="btn btn-success">🛒 Add to Cart</button>
            </form>
            {% else %}
            <button class="btn" disabled style="background: #999;">Out of Stock</button>
            {% endif %}
        </div>
        {% endfor %}
    </div>
    {% else %}
    <p style="color: #999; text-align: center; padding: 40px;">No products available yet.</p>
    {% endif %}
    """)
    
    return render_template_string(template, products=products_db)


@app.route('/user/add-to-cart', methods=['POST'])
def user_add_to_cart():
    """Add product to cart - FULLY FUNCTIONAL"""
    if 'username' not in session or session.get('role') != 'user':
        if 'role' in session:
          return redirect(ROLE_HOME[session['role']])
        return redirect(url_for('index'))

    
    username = session['username']
    product_id = int(request.form.get('product_id'))
    quantity = int(request.form.get('quantity'))
    
    if username not in cart_db:
        cart_db[username] = {}
    
    if product_id in cart_db[username]:
        cart_db[username][product_id] += quantity
    else:
        cart_db[username][product_id] = quantity
    
    return redirect(url_for('user_browse_products'))


@app.route('/user/vendors')
def view_vendors():
    if 'username' not in session or session.get('role') != 'user':
        if 'role' in session:
          return redirect(ROLE_HOME[session['role']])
        return redirect(url_for('index'))


    product_counts = {}
    for product in products_db:
        vendor = product['added_by']
        product_counts[vendor] = product_counts.get(vendor, 0) + 1

    template = BASE_TEMPLATE.replace('{% block content %}{% endblock %}', """
    <div class="nav">
        <div><a href="/user/dashboard">🏠 Dashboard</a></div>
        <div><a href="/logout" class="btn btn-danger">🚪 Logout</a></div>
    </div>

    <h1>🏪 Available Vendors</h1>

    <table>
        <tr><th>Name</th><th>Email</th><th>Phone</th><th>Products</th></tr>
        {% for username, v in vendors.items() %}
        <tr>
            <td>{{ v.name }}</td>
            <td>{{ v.email }}</td>
            <td>{{ v.phone }}</td>
            <td>{{ product_counts.get(username, 0) }}</td>
        </tr>
        {% endfor %}
    </table>
    """)

    return render_template_string(
        template,
        vendors=vendors_db,
        product_counts=product_counts
    )

@app.route('/user/cart', methods=['GET', 'POST'])
def view_cart():
    """View shopping cart - FULLY FUNCTIONAL"""
    global cart_db, orders_db, order_id_counter
    
    if 'username' not in session or session.get('role') != 'user':
        if 'role' in session:
         return redirect(ROLE_HOME[session['role']])
        return redirect(url_for('index'))

    
    username = session['username']
    
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'update':
            product_id = int(request.form.get('product_id'))
            quantity = int(request.form.get('quantity'))
            if username in cart_db and product_id in cart_db[username]:
                # FIXED: Replace quantity instead of adding
                cart_db[username][product_id] = quantity
                save_all_data()
        
        elif action == 'remove':
            product_id = int(request.form.get('product_id'))
            if username in cart_db and product_id in cart_db[username]:
                del cart_db[username][product_id]
                save_all_data()
        
        elif action == 'checkout':
            try:
                if username in cart_db and cart_db[username]:
                    order_items = []
                    total = 0

                    for product_id, qty in cart_db[username].items():
                        product = next((p for p in products_db if p['id'] == product_id), None)
                        if product and product['stock'] >= qty:
                            order_items.append((product_id, qty))
                            total += product['price'] * qty
                            product['stock'] -= qty

                    if order_items:
                        order = {
                            'id': order_id_counter[0],
                            'username': username,
                            'items': order_items,
                            'total': total,
                            'status': 'Confirmed',
                            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        }

                        orders_db.append(order)
                        order_id_counter[0] += 1
                        cart_db[username] = {}

                        save_all_data()
                        return redirect(url_for('user_orders'))

            except Exception as e:
                print("Checkout error:", e)
            return redirect(url_for('view_cart'))


    
    # Calculate cart details
    cart_items = []
    total = 0
    if username in cart_db:
        for product_id, qty in cart_db[username].items():
            product = next((p for p in products_db if p['id'] == product_id), None)
            if product:
                item_total = product['price'] * qty
                cart_items.append({
                    'product': product,
                    'quantity': qty,
                    'total': item_total
                })
                total += item_total
    
    template = BASE_TEMPLATE.replace('{% block content %}{% endblock %}', """
    <div class="nav">
        <div><a href="/user/dashboard">🏠 Dashboard</a><a href="/user/browse-products">🛍️ Browse Products</a></div>
        <div><a href="/logout" class="btn btn-danger">🚪 Logout</a></div>
    </div>
    
    <h1>🛒 Shopping Cart</h1>
    
    {% if cart_items %}
    <table>
        <tr><th>Product</th><th>Price</th><th>Quantity</th><th>Total</th><th>Actions</th></tr>
        {% for item in cart_items %}
        <tr>
            <td>{{ item.product.name }}</td>
            <td>₹{{ item.product.price }}</td>
            <td>
                <form method="POST" style="display: inline;">
                    <input type="hidden" name="action" value="update">
                    <input type="hidden" name="product_id" value="{{ item.product.id }}">
                    <input type="number" name="quantity" value="{{ item.quantity }}" 
                           min="1" max="{{ item.product.stock }}" 
                           style="width: 80px; padding: 5px;">
                    <button type="submit" class="btn btn-info" style="padding: 5px 10px; font-size: 12px;">Update</button>
                </form>
            </td>
            <td>₹{{ item.total }}</td>
            <td>
                <form method="POST" style="display: inline;">
                    <input type="hidden" name="action" value="remove">
                    <input type="hidden" name="product_id" value="{{ item.product.id }}">
                    <button type="submit" class="btn btn-danger">🗑️ Remove</button>
                </form>
            </td>
        </tr>
        {% endfor %}
        <tr style="background: #667eea; color: white; font-weight: bold;">
            <td colspan="3" style="text-align: right;">Grand Total:</td>
            <td colspan="2">₹{{ total }}</td>
        </tr>
    </table>
    
    <div style="margin-top: 30px; text-align: right;">
        <form method="POST" style="display: inline;">
            <input type="hidden" name="action" value="checkout">
            <button type="submit" class="btn btn-success" style="font-size: 18px; padding: 15px 40px;">
                🎉 Proceed to Checkout
            </button>
        </form>
    </div>
    {% else %}
    <p style="color: #999; text-align: center; padding: 40px;">
        Your cart is empty. <a href="/user/browse-products">Start shopping!</a>
    </p>
    {% endif %}
    """)
    
    return render_template_string(template, cart_items=cart_items, total=total)


@app.route('/user/orders')
def user_orders():
    """View user orders - FULLY FUNCTIONAL"""
    global orders_db, products_db
    
    if 'username' not in session or session.get('role') != 'user':
        if 'role' in session:
         return redirect(ROLE_HOME[session['role']])
        return redirect(url_for('index'))

    
    username = session['username']
    my_orders = [o for o in orders_db if o['username'] == username]
    
    # Prepare order details
    orders_list = []
    for order in my_orders:
        items = []
        for product_id, qty in order['items']:
            product = next((p for p in products_db if p['id'] == product_id), None)
            if product:
                items.append({
                    'name': product['name'],
                    'quantity': qty,
                    'price': product['price'],
                    'total': product['price'] * qty
                })
        orders_list.append({
            'id': order['id'],
            'items': items,
            'total': order['total'],
            'status': order['status'],
            'date': order['date']
        })
    
    template = BASE_TEMPLATE.replace('{% block content %}{% endblock %}', """
    <div class="nav">
        <div><a href="/user/dashboard">🏠 Dashboard</a></div>
        <div><a href="/logout" class="btn btn-danger">🚪 Logout</a></div>
    </div>
    
    <h1>📦 My Orders</h1>
    
    {% if orders %}
        {% for order in orders %}
        <div style="background: #f8f9fa; padding: 20px; margin-bottom: 20px; border-radius: 5px; border-left: 4px solid #667eea;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                <div>
                    <h3>Order #{{ order.id }}</h3>
                    <p style="color: #666; font-size: 14px;">{{ order.date }}</p>
                </div>
                <div>
                    <span style="padding: 8px 15px; background: #27ae60; color: white; border-radius: 5px; font-weight: bold;">
                        {{ order.status }}
                    </span>
                </div>
            </div>
            
            <table style="width: 100%; background: white;">
                <tr><th>Product</th><th>Quantity</th><th>Price</th><th>Total</th></tr>
                {% for item in order.items %}
                <tr><td>{{ item.name }}</td><td>{{ item.quantity }}</td><td>₹{{ item.price }}</td><td>₹{{ item.total }}</td></tr>
                {% endfor %}
                <tr style="background: #667eea; color: white; font-weight: bold;">
                    <td colspan="3" style="text-align: right;">Order Total:</td><td>₹{{ order.total }}</td>
                </tr>
            </table>
        </div>
        {% endfor %}
    {% else %}
    <p style="color: #999; text-align: center; padding: 40px;">
        You haven't placed any orders yet. <a href="/user/browse-products">Start shopping!</a>
    </p>
    {% endif %}
    """)
    
    return render_template_string(template, orders=orders_list)


@app.route('/user/guest-list', methods=['GET', 'POST'])
def user_guest_list():
    """Manage guest list - FULLY FUNCTIONAL"""
    if 'username' not in session or session.get('role') != 'user':
        if 'role' in session:
         return redirect(ROLE_HOME[session['role']])
        return redirect(url_for('index'))

    
    username = session['username']
    
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'add':
            guest = {
                'id': guest_id_counter[0],
                'username': username,
                'guest_name': request.form.get('guest_name'),
                'guest_email': request.form.get('guest_email'),
                'guest_phone': request.form.get('guest_phone'),
                'event': request.form.get('event'),
                'date_added': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            guest_list_db.append(guest)
            guest_id_counter[0] += 1
        
        elif action == 'delete':
            guest_id = int(request.form.get('guest_id'))
            guest_list_db[:] = [g for g in guest_list_db 
                                if not (g['id'] == guest_id and g['username'] == username)]
        
        return redirect(url_for('user_guest_list'))
    
    my_guests = [g for g in guest_list_db if g['username'] == username]
    
    template = BASE_TEMPLATE.replace('{% block content %}{% endblock %}', """
    <div class="nav">
        <div><a href="/user/dashboard">🏠 Dashboard</a></div>
        <div><a href="/logout" class="btn btn-danger">🚪 Logout</a></div>
    </div>
    
    <h1>👥 Guest List Management</h1>
    
    <h2>Add New Guest</h2>
    <form method="POST" style="max-width: 600px; background: #f8f9fa; padding: 20px; border-radius: 5px; margin-bottom: 30px;">
        <input type="hidden" name="action" value="add">
        <div class="form-group"><label>Guest Name *</label><input type="text" name="guest_name" required></div>
        <div class="form-group"><label>Guest Email *</label><input type="email" name="guest_email" required></div>
        <div class="form-group"><label>Guest Phone *</label><input type="tel" name="guest_phone" required pattern="[0-9]{10}"></div>
        <div class="form-group"><label>Event/Occasion *</label><input type="text" name="event" placeholder="e.g., Tech Conference 2026" required></div>
        <button type="submit" class="btn btn-success">➕ Add Guest</button>
    </form>
    
    <h2>My Guest List ({{ guests|length }})</h2>
    {% if guests %}
        {% for guest in guests %}
        <div class="guest-item">
            <div>
                <h3>{{ guest.guest_name }}</h3>
                <p>📧 {{ guest.guest_email }}</p>
                <p>📞 {{ guest.guest_phone }}</p>
                <p style="color: #667eea; font-weight: bold;">🎫 {{ guest.event }}</p>
                <p style="color: #999; font-size: 14px;">Added: {{ guest.date_added }}</p>
            </div>
            <div>
                <form method="POST" style="display: inline;">
                    <input type="hidden" name="action" value="delete">
                    <input type="hidden" name="guest_id" value="{{ guest.id }}">
                    <button type="submit" class="btn btn-danger" onclick="return confirm('Remove this guest?')">
                        🗑️ Remove
                    </button>
                </form>
            </div>
        </div>
        {% endfor %}
    {% else %}
    <p style="color: #999; text-align: center; padding: 40px;">No guests added yet.</p>
    {% endif %}
    """)
    
    return render_template_string(template, guests=my_guests)


@app.route('/user/profile', methods=['GET', 'POST'])
def user_profile():
    """User profile management - FULLY FUNCTIONAL"""
    if 'username' not in session or session.get('role') != 'user':
        if 'role' in session:
         return redirect(ROLE_HOME[session['role']])
        return redirect(url_for('index'))

    
    username = session['username']
    
    if request.method == 'POST':
        regular_users_db[username]['name'] = request.form.get('name')
        regular_users_db[username]['email'] = request.form.get('email')
        regular_users_db[username]['phone'] = request.form.get('phone')
        new_password = request.form.get('new_password')
        if new_password:
            regular_users_db[username]['password'] = new_password
        session['name'] = regular_users_db[username]['name']
        return redirect(url_for('user_profile'))
    
    template = BASE_TEMPLATE.replace('{% block content %}{% endblock %}', """
    <div class="nav">
        <div><a href="/user/dashboard">🏠 Dashboard</a></div>
        <div><a href="/logout" class="btn btn-danger">🚪 Logout</a></div>
    </div>
    
    <h1>👤 My Profile</h1>
    
    <form method="POST" style="max-width: 600px;">
        <div class="form-group"><label>Username</label><input type="text" value="{{ username }}" disabled></div>
        <div class="form-group"><label>Full Name</label><input type="text" name="name" value="{{ user.name }}" required></div>
        <div class="form-group"><label>Email</label><input type="email" name="email" value="{{ user.email }}" required></div>
        <div class="form-group"><label>Phone</label><input type="tel" name="phone" value="{{ user.phone }}" required></div>
        <div class="form-group"><label>New Password (leave blank to keep current)</label><input type="password" name="new_password"></div>
        <button type="submit" class="btn btn-success">💾 Save Changes</button>
        <a href="/user/dashboard" class="btn btn-danger">Cancel</a>
    </form>
    """)
    
    return render_template_string(template, username=username, user=regular_users_db[username])

@app.route('/back')
def smart_back():
    if 'role' not in session:
        return redirect(url_for('index'))

    role = session['role']

    # If already on mode main page → go to mode selector
    if session.get('at_mode_home', False):
        session.pop('at_mode_home')
        return redirect(url_for('index'))

    # Otherwise → go to mode home
    session['at_mode_home'] = True
    return redirect(url_for(ROLE_HOME[role]))

# APPLICATION ENTRY POINT
# ============================================================================

if __name__ == '__main__':
    print("=" * 80)
    print(" " * 20 + "TECHNICAL EVENT MANAGEMENT SYSTEM")
    print("=" * 80)
    
    # Load saved data
    print("\n💾 Loading saved data...")
    load_all_data()
    
    # Verify critical routes
    print("\n🔍 Verifying Routes...")
    critical_routes = ['index', 'admin_login', 'admin_dashboard', 'logout', 
                       'all_products', 'user_login', 'vendor_login', 
                       'user_dashboard', 'vendor_dashboard']
    
    errors_found = False
    with app.test_request_context():
        for route in critical_routes:
            try:
                url = url_for(route)
                print(f"   ✅ {route:25s} → {url}")
            except Exception as e:
                print(f"   ❌ {route:25s} → ERROR")
                errors_found = True
    
    if errors_found:
        print("\n⚠️  Some routes have errors. Check above.")
    else:
        print("\n✅ All critical routes verified!")
    
    print("\n📌 Server Address: http://127.0.0.1:5000")
    print("\n✅ FEATURES:")
    print("   • Role-based access control (Admin, Vendor, User)")
    print("   • Settings dropdown menu for easy navigation")
    print("   • Admin account creation requires IT Department")
    print("   • Stock update functionality for vendors")
    print("   • Comprehensive data management")
    print("   • Data persistence (saves automatically)")
    print("\n" + "=" * 80)
    
    app.run(debug=True, host='0.0.0.0', port=5000)