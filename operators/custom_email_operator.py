from airflow.utils.decorators import apply_defaults
from airflow.operators.email_operator import EmailOperator
from airflow.models import Variable

import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from airflow.configuration import conf
from typing import Iterable, List, Optional, Union


class CustomEmailOperator(EmailOperator):
    """
    Allows for emails to be sent with custom SMTP server, along with native airflow emailing.
    """

    @apply_defaults
    def __init__(
        self,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self._args = args
        self._kwargs = kwargs

    def execute(self, context):
        """
        Either use custom SMTP server or default EmailOperator
        """
        if Variable.get("email_server", None):
            send_email_custom_server(
                self.to,
                self.subject,
                self.html_content,
                files=self.files,
                cc=self.cc,
                bcc=self.bcc,
                mime_subtype=self.mime_subtype,
                mime_charset=self.mime_charset,
            )
        else:
            super().execute(context)


def send_email_custom_server(
    to: Union[str, Iterable[str]],
    subject: str,
    html_content: str,
    files: Optional[List[str]] = None,
    dryrun: bool = False,
    cc: Optional[Union[str, Iterable[str]]] = [],
    bcc: Optional[Union[str, Iterable[str]]] = [],
    mime_subtype: str = 'alternative',
    mime_charset: str = 'utf-8',
    **kwargs,
):
    composer_instance_name = conf.get("webserver", "web_server_name")
    sender_email = f"no-reply@{ composer_instance_name }.bedbath.com"
    smtp_server = Variable.get("email_server", "smtp.bedbath.com")
    cc = cc if cc is not None else []
    bcc = bcc if bcc is not None else []
    msg = MIMEMultipart(mime_subtype)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = ", ".join(to)
    msg["Cc"] = ", ".join(cc)
    msg["Bcc"] = ", ".join(bcc)
    mime_message = MIMEText(html_content, "html", mime_charset)
    msg.attach(mime_message)

    logging.info("Establishing connection with SMTP server..")
    server = smtplib.SMTP(f"{ smtp_server }:25")
    if not dryrun:
        server.sendmail(sender_email, to + cc + bcc, msg.as_string())
    server.quit()
