# OTP-Varification
The app.py file is a Flask-based Python app. It imports Flask, math, random, and smtplib. The app is initialized with a secret key for session management. It includes a generate_otp() function to create a 6-digit OTP and a send_email(recipient, otp) function to send the OTP via Gmail's SMTP, with error handling for authentication issues.
