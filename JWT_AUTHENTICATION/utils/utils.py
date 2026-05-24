import time


# This function takes a long time to execute,
# simulating a time-consuming task like sending an email.
def send_email(email: str):

    print("SENDING EMAIL...")

    time.sleep(10)

    print(f"Email sent to {email}")
