import boto3

from ptCryptoClub.admin.config import EmailLogin


class Email:
    def send_email(self, email, hash):
        ses = boto3.client("ses",
                           aws_access_key_id=EmailLogin().aws_access_key_id,
                           aws_secret_access_key=EmailLogin().aws_secret_access_key,
                           region_name=EmailLogin().region_name)
        body = f"""
            <!DOCTYPE html>
            <body>
                <br>
                <H4>Welcome to ptcrypto.club</H4>
                <br>
                <p>Please activate your account by following the link below</p>
                <br>
                <H5><a href='https://app.ptcrypto.club/activate-account?hash={hash}&email={email}' target="_blank">Activate account</a></H5>
                <br>
                <br>
                <p>Kind regards</p>
                <br>
                <small><q><i>This email was generated automatically. Please do not reply to this email.</i></q></small>
            </body>
        </html>
        """
        ses.send_email(
            Source="donotreply@ptcrypto.club",
            Destination={
                "ToAddresses": [f"{email}"]
                },
            Message={
                "Subject": {
                    "Data": "ptcrypto.club - Email confirmation",
                    "Charset": "UTF-8"
                    },
                "Body": {
                    "Html": {
                        "Data": body,
                        "Charset": "UTF-8"
                        }
                    }
                }
            )
