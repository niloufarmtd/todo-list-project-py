import schedule
import time
from .autoclose_overdue import autoclose_overdue_tasks

def start_scheduler():
    """Start the scheduled task runner"""
    print("🕐 Starting TodoList scheduler...")
    print("⏰ Autoclose task will run every 15 minutes")
    
    # Schedule the task to run every 15 minutes
    schedule.every(15).minutes.do(autoclose_overdue_tasks)
    
    # Run immediately once
    autoclose_overdue_tasks()
    
    # Keep the scheduler running
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    start_scheduler()