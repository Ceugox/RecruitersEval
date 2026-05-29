"""
email_sender.py — Envia e-mails HTML via Gmail SMTP com imagens CID inline.
"""

import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email_templates import CID_HEADER, CID_FOOTER

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465


def send_email(
    sender_email: str,
    app_password: str,
    recipient_email: str,
    subject: str,
    html_body: str,
    img_header: str = None,
    img_footer: str = None,
    **kwargs,
) -> None:
    # Estrutura correta para imagens inline: multipart/related
    msg_related = MIMEMultipart("related")
    msg_related["Subject"] = subject
    msg_related["From"] = sender_email
    msg_related["To"] = recipient_email

    # HTML dentro de multipart/alternative (boas práticas)
    msg_alt = MIMEMultipart("alternative")
    msg_alt.attach(MIMEText(html_body, "html", "utf-8"))
    msg_related.attach(msg_alt)

    # Imagem cabeçalho
    if img_header:
        with open(img_header, "rb") as f:
            img = MIMEImage(f.read())
        img.add_header("Content-ID", f"<{CID_HEADER}>")
        img.add_header("Content-Disposition", "inline", filename="header.png")
        msg_related.attach(img)

    # Imagem rodapé
    if img_footer:
        with open(img_footer, "rb") as f:
            img = MIMEImage(f.read())
        img.add_header("Content-ID", f"<{CID_FOOTER}>")
        img.add_header("Content-Disposition", "inline", filename="footer.png")
        msg_related.attach(img)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, context=context) as server:
        server.login(sender_email, app_password)
        server.sendmail(sender_email, recipient_email, msg_related.as_string())
