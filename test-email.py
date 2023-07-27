import smtplib

def python_send_email():
    email = "markachilesflores2004@gmail.com"
    app_pass = "dvswlovojwhbnpuy"

    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()

        smtp.login(email, app_pass)
    
        subject = "Sample email with python"
        body = "This is just a test email, don't mind me."
        msg = f"Subject: {subject}\n\n{body}"

        smtp.sendmail(email, ["anthony.basang18@gmail.com", email], msg)

python_send_email()