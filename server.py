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

    string_to_write = '\n' + datetime.datetime.now().strftime("%c") + "; - " + indicator.closeData() + "; - " + indicator.rolling_window() + '; - ' + indicator.simple_moving_average() + "; - " + indicator.exponentially_weighted_moving_average() + "; - " + indicator.relative_strength_index() + "; - " + indicator.moving_average_convergence_divergence() + "; - " + indicator.rsi_and_macd() + "; - " + indicator.triple_exponential_average() + "; - " + indicator.williams_percent_r() + "; - " + indicator.bollinger_bands()

    f.write(string_to_write)
    f.close()




@app.route("/")
def hello_world():
    return "<p><a href='/static/result.txt'>Перейти в точку входа</a>!</p>"
    
