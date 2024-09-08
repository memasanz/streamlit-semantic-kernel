from semantic_kernel.functions import kernel_function
from typing import List 

class EmailPlugin:
    @kernel_function(
        name="send_email",
        description="Sends an email to a recipient."
    )
    async def send_email(self, recipient_emails: str|List[str], subject: str, body: str):
        # Add logic to send an email using the recipient_emails, subject, and body
        # For now, we'll just print out a success message to the console
        print("Email sent!")
        print("recipient_emails:" + recipient_emails)
        print("subject:" + subject)
        print("body:" + body)