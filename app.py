from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import os

# -------------------------------------------------
# Flask App Configuration
# -------------------------------------------------
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "supersecretkey")

# Database setup
os.makedirs("database", exist_ok=True)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(BASE_DIR, "database", "gas_agency.db")

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# -------------------------------------------------
# Database Models
# -------------------------------------------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    address = db.Column(db.String(200))
    mobile = db.Column(db.String(15), unique=True, nullable=False)
    pincode = db.Column(db.String(10))
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    date = db.Column(db.String(20))

    def __repr__(self):
        return f"<User {self.name}>"


class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    gas_type = db.Column(db.String(50))
    quantity = db.Column(db.Integer, default=1)
    status = db.Column(db.String(50), default="Pending Payment")
    date = db.Column(db.String(20))
    payment_method = db.Column(db.String(50))


# -------------------------------------------------
# Create Tables
# -------------------------------------------------
with app.app_context():
    db.create_all()

# -------------------------------------------------
# Routes
# -------------------------------------------------
@app.route('/')
@app.route('/home')
def home():
    return render_template("home.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/services')
def services():
    return render_template("services.html")

@app.route('/faq')
def faq():
    return render_template("faq.html")

# -------------------------------------------------
# Register
# -------------------------------------------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        address = request.form["address"]
        mobile = request.form["mobile"]
        pincode = request.form["pincode"]
        email = request.form["email"]
        password = generate_password_hash(request.form["password"])
        date = request.form["date"]

        existing_user = User.query.filter(
            (User.mobile == mobile) | (User.email == email)
        ).first()

        if existing_user:
            flash("User with this mobile or email already exists!", "error")
            return redirect(url_for("register"))

        new_user = User(
            name=name, address=address, mobile=mobile,
            pincode=pincode, email=email, password=password, date=date
        )
        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful! Please login.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")

# -------------------------------------------------
# Login / Logout
# -------------------------------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        name = request.form['name']
        password = request.form['password']

        user = User.query.filter((User.email == name) | (User.mobile == name)).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['user_name'] = user.name
            flash("Login successful!", "success")
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid credentials!", "danger")

    return render_template("login.html")

@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully!", "info")
    return redirect(url_for('home'))

# -------------------------------------------------
# Dashboard / Profile
# -------------------------------------------------
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash("Please log in first!", "warning")
        return redirect(url_for('login'))
    return render_template("booking.html")

@app.route("/profile")
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    return render_template("profile.html", user=user)

# -------------------------------------------------
# Booking → Payment → History
# -------------------------------------------------
@app.route("/booking", methods=["GET", "POST"])
def booking():
    if not session.get("user_id"):
        flash("Please login to continue.")
        return redirect(url_for("login"))

    if request.method == "POST":
        gas_type = request.form["cylinder_type"]
        address = request.form["address"]

        new_booking = Booking(
            user_id=session["user_id"],
            gas_type=gas_type,
            quantity=1,
            status="Pending Payment",
            date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        db.session.add(new_booking)
        db.session.commit()

        return redirect(url_for("payment", booking_id=new_booking.id))

    return render_template("booking.html")


@app.route("/payment", methods=["GET", "POST"])
def payment():
    booking_id = request.args.get("booking_id")
    booking = Booking.query.get(booking_id)

    if not booking:
        flash("Booking not found!", "error")
        return redirect(url_for("history"))

    if request.method == "POST":
        payment_method = request.form["payment_method"]
        booking.payment_method = payment_method
        booking.status = f"Payment Completed ({payment_method})"
        db.session.commit()

        flash("Payment successful! Your booking is confirmed.", "success")
        return redirect(url_for("history"))

    return render_template("payment.html", booking_id=booking_id, amount=950)


@app.route("/history")
def history():
    if not session.get("user_id"):
        flash("Please login first.")
        return redirect(url_for("login"))

    bookings = Booking.query.filter_by(user_id=session["user_id"]).all()
    return render_template("history.html", bookings=bookings)

# -------------------------------------------------
# Contact Page
# -------------------------------------------------
@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")

        if not name or not email or not message:
            flash("All fields are required!", "error")
            return redirect(url_for("contact"))

        flash("Message sent successfully!", "success")
        return redirect(url_for("contact"))

    return render_template("contact.html")

# -------------------------------------------------
# Admin & Error Pages
# -------------------------------------------------
@app.route('/admin')
def admin():
    return render_template("admin.html")

@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404

# -------------------------------------------------
# Main
# -------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
