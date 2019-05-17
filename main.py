# pandas for data management
import pandas as pd

# os for manipulating path
import os
from os.path import join

# to download dataset
from scripts.download_dataset import download

# to transform dataset
from scripts.transform_dataset import transurv

# call dataset
url = "http://maula.fahim:fahimhadimaula28@reportportal/Reports/Pages/Folder.aspx?ItemPath=%2f99.+Aplikasi+lain-lain%2f04.Aplikasi+Manufacturing%2fPortal+Engineering%2fWork+Order&ViewMode=List"
download(url=url)

# read dataset and getting data in the right format
history = join(os.getcwd(), 'datasets', 'filling_event.csv')
machine = join(os.getcwd(), 'datasets', 'machine.csv')
ttf = transurv(hist_url=history, mach_url=machine)