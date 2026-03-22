import smtplib, ssl, configparser, DB
import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
from email.mime.base import MIMEBase
from email import encoders
import html
from popups import confirm_send_without_lm, confirm_send_all_without_lm

def createMessage():
    return MIMEMultipart("alternative")

def receiver(message, emailOfTheCompany):
    message["To"] = emailOfTheCompany

def objectMail(message, firstName, lastName, companyName, object_mail=""):

    default_subject = f"Candidature {firstName} {lastName} - {companyName}"

    if object_mail:
        subject = object_mail
    else:
        subject = default_subject

    message["Subject"] = subject

def textMail(message, firstName, lastName, companyName, textmail=""):

    default_plaintext = f"""Bonjour,

    Je vous transmets ma lettre de motivation ainsi que mon CV pour {companyName}.

    Cordialement,
    {firstName} {lastName}
    """

    default_html = f"""
    <html>
        <body>
            <p>
                Bonjour,<br /><br />
                Je vous transmets ma lettre de motivation ainsi que mon CV pour {companyName}.<br /><br />
                Cordialement,<br />
                {firstName} {lastName}
            </p>
        </body>
    </html>
    """

    if textmail.strip():
        plaintext = textmail

        escaped = html.escape(plaintext).replace("\n", "<br />")

        html_content = f"""
        <html>
            <body>
                <p>{escaped}</p>
            </body>
        </html>
        """
    else:
        plaintext = default_plaintext
        html_content = default_html

    message.attach(MIMEText(plaintext, "plain", "utf-8"))
    message.attach(MIMEText(html_content, "html", "utf-8"))


def attachment(message, companyName):
    """
    Attache le CV (obligatoire) et la LM (optionnelle).
    Retourne False si l'utilisateur annule l'envoi.
    Retourne True sinon.
    """

    cv_file = max(Path("../CV").iterdir(), key=lambda f: f.stat().st_mtime)

    with open(cv_file, "rb") as f:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(f.read())

    encoders.encode_base64(part)
    part.add_header(
        "Content-Disposition",
        f'attachment; filename="{cv_file.name}"'
    )
    message.attach(part)

    pathLM = Path("../LM_PDF")
    lm_file = list(pathLM.glob(f"*{companyName}*.pdf"))

    
    if not lm_file:
        user_choice = confirm_send_without_lm(companyName)

        if not user_choice:
            print("Envoi annulé par l'utilisateur.")
            return False

        print("Envoi sans lettre de motivation.")
        return True

    lm_file = lm_file[0]

    with open(lm_file, "rb") as f:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(f.read())

    encoders.encode_base64(part)
    part.add_header(
        "Content-Disposition",
        f'attachment; filename="{lm_file.name}"'
    )
    message.attach(part)

    return True

def sendEmail(message, email_address, email_password, smtp_address, smtp_port):
    context = ssl.create_default_context()

    # Champ FROM (important)
    message["From"] = email_address

    with smtplib.SMTP_SSL(smtp_address, smtp_port, context=context) as server:
        server.login(email_address, email_password)
        server.sendmail(
            email_address,
            message["To"],
            message.as_string()
        )


def loopCompanies():

    config = configparser.ConfigParser()
    config.read('config.ini')

    email_address = config.get('EMAIL', 'EMAIL_ADDRESS')
    email_password = config.get('EMAIL', 'EMAIL_PASSWORD')
    firstName = config.get('GENERAL', 'firstName')
    lastName = config.get('GENERAL', 'lastName')
    textmail = config.get("SETUP", "textmail", fallback="").strip()
    frequency = config.get('SETUP', 'frequency')

    smtp_address = "smtp.gmail.com"
    smtp_port = 465

    now = datetime.datetime.now().replace(microsecond=0)

    companies = DB.getDB("companyName, companyEmail, date")

    for companyName, companyEmail, last_date in companies:

        send_mail = False

        if last_date is None:
            send_mail = True
        else:
            last_date = datetime.datetime.fromisoformat(last_date)

            if frequency is not None:
                if now - last_date > datetime.timedelta(days=int(frequency)):
                    send_mail = True

        if not send_mail:
            continue

        message = createMessage()
        receiver(message, companyEmail)
        objectMail(message, firstName, lastName, companyName)
        textMail(message, firstName, lastName, companyName, textmail)

        should_send = attachment(message, companyName)

        if not should_send:
            continue

        sendEmail(
            message,
            email_address,
            email_password,
            smtp_address,
            smtp_port
        )

        DB.updateDateForCompany("date", now, companyName)

    DB.updateDatabase("emailSent")