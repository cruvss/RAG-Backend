import smtplib
from email.message import EmailMessage
from app.models.schemas import BookingRequest
from app.config import SMTP_HOST, SMTP_PASS, SMTP_PORT, SMTP_USER
import os

def send_confirmation_email(booking: BookingRequest):
    msg = EmailMessage()
    msg['Subject'] = "Interview Confirmation"
    msg['From'] = SMTP_USER
    msg['To'] = booking.email
    msg.set_content(f"""
Hi {booking.name},

Your interview has been scheduled on {booking.date} at {booking.time}.

Thank you!
    """)
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.send_message(msg)
