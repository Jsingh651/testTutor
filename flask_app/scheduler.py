import schedule
import time
from datetime import datetime
from flask_app.models.users import User

def update_is_paying_job():
    users = User.get_all()  # Retrieve all users from the database
    for user in users:
        user.update_is_paying()  # Update the is_paying attribute for each user

# Schedule the job to run every 12 hours
schedule.every(12).hours.do(update_is_paying_job)

# Keep the scheduler running
while True:
    schedule.run_pending()
    time.sleep(1)
