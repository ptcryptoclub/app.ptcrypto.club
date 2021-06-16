import boto3

from ptCryptoClub.admin.config import EmailLogin, mfa_routes


class Email:
    def activation_email(self, email, hash, username):
        ses = boto3.client("ses",
                           aws_access_key_id=EmailLogin().aws_access_key_id,
                           aws_secret_access_key=EmailLogin().aws_secret_access_key,
                           region_name=EmailLogin().region_name)
        body = f"""
            <!DOCTYPE html>
            <body>
                <br>
                <H4>Hi {username}</H4>
                <p>Welcome to app.ptcrypto.club</p>
                <br>
                <p>Please activate your account by following the link below</p>
                <br>
                <H5><a href='https://app.ptcrypto.club/activate-account?hash={hash}&email={email}' target="_blank">Activate account</a></H5>
                <br>
                <p>If you didn't expect this email, please contact our team at humans@ptcrypto.club</p>
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

    def reactivation_email(self, email, hash, username):
        ses = boto3.client("ses",
                           aws_access_key_id=EmailLogin().aws_access_key_id,
                           aws_secret_access_key=EmailLogin().aws_secret_access_key,
                           region_name=EmailLogin().region_name)
        body = f"""
            <!DOCTYPE html>
            <body>
                <br>
                <H4>Hi {username}</H4>
                <br>
                <p>Your details were updated successfully. Please reactivate your account by following the link below</p>
                <br>
                <H5><a href='https://app.ptcrypto.club/activate-account?hash={hash}&email={email}' target="_blank">Activate account</a></H5>
                <br>
                <p>If you didn't expect this email, please contact our team at humans@ptcrypto.club</p>
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
                    "Data": "ptcrypto.club - Updated details",
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

    def password_recovery_email(self, email, hash, username, user_id):
        ses = boto3.client("ses",
                           aws_access_key_id=EmailLogin().aws_access_key_id,
                           aws_secret_access_key=EmailLogin().aws_secret_access_key,
                           region_name=EmailLogin().region_name)
        body = f"""
            <!DOCTYPE html>
            <body>
                <br>
                <H4>Hi {username}</H4>
                <br>
                <p>Please use the link below to recover your password.</p>
                <br>
                <H5><a href='https://app.ptcrypto.club/recovery/password/confirmation/{hash}/{user_id}/' target="_blank">Recover password</a></H5>
                <small>This link will only be valid during the next 5 minutes.</small>
                <br>
                <p>If you didn't expect this email, please contact our team at humans@ptcrypto.club and ignore the link above.</p>
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
                    "Data": "ptcrypto.club - Recover password",
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

    def deactivate_2fa(self, email, hash, username, user_id):
        ses = boto3.client("ses",
                           aws_access_key_id=EmailLogin().aws_access_key_id,
                           aws_secret_access_key=EmailLogin().aws_secret_access_key,
                           region_name=EmailLogin().region_name)
        body = f"""
            <!DOCTYPE html>
            <body>
                <br>
                <H4>Hi {username}</H4>
                <br>
                <p>Please use the link below to deactivate 2FA at login in your account.</p>
                <br>
                <H5><a href='https://app.ptcrypto.club/account/{mfa_routes['deactivate_2fa_confirmation']}/{hash}/{user_id}/' target="_blank">Deactivate 2FA at login</a></H5>
                <small>This link will only be valid during the next 5 minutes.</small>
                <br>
                <p><strong>Important information:</strong> This will only replace 2FA at login for a given PIN <i>(to be sent in a separated email)</i>, when using your account you still may be asked for 2FA.</p>
                <br>
                <br>
                <p>If you didn't expect this email, please contact our team at humans@ptcrypto.club and ignore the link above.</p>
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
                    "Data": "ptcrypto.club - 2FA deactivation at login",
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

    def activate_2fa(self, email, hash, username, user_id):
        ses = boto3.client("ses",
                           aws_access_key_id=EmailLogin().aws_access_key_id,
                           aws_secret_access_key=EmailLogin().aws_secret_access_key,
                           region_name=EmailLogin().region_name)
        body = f"""
            <!DOCTYPE html>
            <body>
                <br>
                <H4>Hi {username}</H4>
                <br>
                <p>Please use the link below to reactivate 2FA at login in your account.</p>
                <br>
                <H5><a href='https://app.ptcrypto.club/account/{mfa_routes['activate_2fa_confirmation']}/{hash}/{user_id}/' target="_blank">Reactivate 2FA at login</a></H5>
                <small>This link will only be valid during the next 5 minutes.</small>
                <br>
                <br>
                <p>If you didn't expect this email, please contact our team at humans@ptcrypto.club and ignore the link above.</p>
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
                    "Data": "ptcrypto.club - 2FA reactivation at login",
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

    def pin_2fa(self, email, username, pin):
        ses = boto3.client("ses",
                           aws_access_key_id=EmailLogin().aws_access_key_id,
                           aws_secret_access_key=EmailLogin().aws_secret_access_key,
                           region_name=EmailLogin().region_name)
        body = f"""
            <!DOCTYPE html>
            <body>
                <br>
                <H4>Hi {username}</H4>
                <br>
                <p>Your pin is <strong>{pin}</strong>. Please keep this pin safe.</p>
                <br>
                <br>
                <br>
                <p>If you didn't expect this email, please contact our team at humans@ptcrypto.club and ignore the link above.</p>
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
                    "Data": "ptcrypto.club - 2FA replacement pin",
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
