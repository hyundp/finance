import matplotlib.pyplot as plt
from slacker import Slacker
from datetime import datetime
from datetime import timedelta
import pandas as pd


end_date = datetime.today().strftime('%Y-%m-%d')
six_month_ago = datetime.today() - timedelta(days=180)
start_date = six_month_ago.strftime('%Y-%m-%d')
