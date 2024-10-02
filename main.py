# from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask
from flask_scheduler import Scheduler
import indicator
import datetime

app = Flask(__name__)

# Initialize the extension
scheduler = Scheduler(app)

# scheduler config interval
app.config['SCHEDULER_API_INTERVAL'] = 600 # in seconds

@scheduler.runner(interval=7200)
def my_task():
    print('tick')
    f = open("static/result.txt", "a", encoding="utf-8")

    string_to_write = '\n' + datetime.datetime.now().strftime("%c") + " | Close:" + indicator.getData()
    f.write(string_to_write)
    f.close()




@app.route("/")
def hello_world():
    return "<p><a href='/static/result.txt'>Перейти в точку входа</a>!</p>"
    
