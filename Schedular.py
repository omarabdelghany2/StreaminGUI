import schedule
import threading
import time
from datetime import datetime
from PyQt6.QtCore import QThread, pyqtSignal, QObject
from Obs import Obs
import re
import os

class TaskScheduler(QObject):
    TaskExcuted=pyqtSignal(int)
    def __init__(self):
        super().__init__()
        self.schedule_thread = None
        self.is_running = False
        self.ob = Obs("localhost", 4444, "password")
        self.ob.connect()
        

    def _start_schedule(self):
        self.is_running = True
        # Run the scheduler
        while self.is_running:
            schedule.run_pending()
            time.sleep(1)  # Sleep for 1 second to avoid high CPU usage

    def start_schedule(self):
        # Start the scheduler in a separate thread
        print("schedualeStarted")
        self.schedule_thread = threading.Thread(target=self._start_schedule)
        self.schedule_thread.daemon = True  # Daemonize the thread so it exits when the main program exits
        self.schedule_thread.start()

    def stop_schedule(self):
        print("schedualeStopped")
        self.is_running = False

    def add_task(self, month, day, hour, minute, am_pm,platform,url,indexinGUI,duration):
        # Convert month name to month number
        hour =int(hour)
        month_number = datetime.strptime(month, "%B").month
        # Convert 12-hour clock to 24-hour clock

        if am_pm.upper() == 'PM':
            if(hour==12):
                hour=23
            else:    
                hour += 12    

        text="StartOfVideo"
        scheduled_time = datetime(datetime.now().year, int(month_number), int(day), int(hour), int(minute))
        schedule.every().day.at(scheduled_time.strftime("%H:%M")).do(lambda: self._my_task(platform,url,indexinGUI,text))
        print(f"Task scheduled for {scheduled_time.strftime('%Y-%m-%d %I:%M %p')}")

        duration2=int(duration)
        minute2=int(minute)
        while(duration2>60):
            hour=hour+1
            duration2=duration2-60
        if(minute2+duration2>60):
            hour=hour+1
            minute2=minute2+duration2-60
            duration2=0
        print(minute2+duration2)
        minute2=minute2+duration2    
        text2="EndOfVideo"        
        scheduled_time = datetime(datetime.now().year, int(month_number), int(day), int(hour), int(minute2))
        schedule.every().day.at(scheduled_time.strftime("%H:%M")).do(lambda: self._my_task(platform,url,indexinGUI,text2))
        print(f"Task scheduled for {scheduled_time.strftime('%Y-%m-%d %I:%M %p')} thats for stopping")

        
    def delete_task(self, month, day, hour, minute, am_pm,duration):
        # Convert month name to month number
        month_number = datetime.strptime(month, "%B").month

        if am_pm.upper() == 'PM':
            if(hour==12):
                hour=23
            else:    
                hour += 12    
        # Convert 12-hour clock to 24-hour clock  

        scheduled_time = datetime(datetime.now().year, int(month_number), int(day), int(hour), int(minute))
        scheduled_time_str = scheduled_time.strftime("%I:%M %p")
        for job in schedule.jobs:
            if job.next_run.strftime("%I:%M %p") == scheduled_time_str:
                schedule.cancel_job(job)
                print(f"Task scheduled for {scheduled_time_str} deleted.")
                return
        print(f"No task scheduled for {scheduled_time_str}.")

    def _my_task(self,platform,url,indexingui,text):
        print("entered TASK")
        print(text)

        if(text=="StartOfVideo"):
            print("video Started")
            #lets call Mark Functions here
            if(self.is_url_or_file_path(url)=="URL"):
                self.ob.set_video_with_link_in_view(url)
                self.ob.set_streaming_service(platform)
                self.ob.start_streaming()
            else :
                self.ob.set_video_with_path_in_view(url)
                self.ob.set_streaming_service(platform)
                self.ob.start_streaming()
            ##delete the task because its schedualed
            self.TaskExcuted.emit(indexingui)
        else:
            ##this will be ahidden task to end the stream
            self.ob.stop_streaming()
            time.sleep(1)
            print("video Ended")
        
        #delete the Task from the gui and the schedular







    def is_url_or_file_path(self,text):
        # Regular expression to match URLs
        url_pattern = re.compile(
            r'^(?:http|ftp)s?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or IP
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)

        # Check if the input resembles a URL
        if re.match(url_pattern, text):
            return "URL"
        
        # Check if the input resembles a file path (assuming it's a local file path)
        if os.path.exists(text):
            return "File Path"
        
        # If neither URL nor file path, return "Neither"
        return "Neither"
    