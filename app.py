from flask import Flask, render_template, request, redirect, url_for, flash, session
import math
import random
import smtplib

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Necessary for flashing messages and session management

# Function to generate OTP
def generate_otp():
    digits = "0123456789"
    otp = "".join([digits[math.floor(random.random() * 10)] for _ in range(6)])
    return otp

# Function to send email
def send_email(recipient, otp):
    msg = f"{otp} is your OTP"
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    try:
        s.login("Sample@gmail", "Password")
        s.sendmail('Sample@gmail', recipient, msg)
        s.quit()
        return True
    except smtplib.SMTPAuthenticationError:
        print("Failed to login. Check your email or app password.")
        s.quit()
        return False
    except Exception as e:
        print(f"Failed to send email: {e}")
        s.quit()
        return False

# Home route to render the form
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        emailid = request.form['email']
        otp = generate_otp()
        if send_email(emailid, otp):
            session['otp'] = otp  # Store OTP in session
            flash("OTP sent successfully!", "success")
            return redirect(url_for('verify'))
        else:
            flash("Failed to send OTP. Please try again.", "danger")
            return redirect(url_for('index'))
    return render_template('index.html')

# Route to verify OTP
@app.route('/verify', methods=['GET', 'POST'])
def verify():
    if request.method == 'POST':
        user_otp = request.form['otp'].strip()  # Strip whitespace from user input
        session_otp = session.get('otp')  # Retrieve OTP from session
        if user_otp == session_otp:
            flash("Verification completed successfully!", "success")
            return redirect(url_for('index'))
        else:
            flash("Invalid OTP. Please try again.", "danger")
            return redirect(url_for('verify'))
    return render_template('verify.html')

if __name__ == '__main__':
    app.run(debug=True)
