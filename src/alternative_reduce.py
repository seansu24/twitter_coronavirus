#!/usr/bin/env python3

# command line args
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--input_folder',default='outputs')
parser.add_argument('--hashtags',nargs='+',required=True)
parser.add_argument('--output_path',default='alternative_reduce.png')
args = parser.parse_args()

# imports
import os
import json
import datetime
from collections import defaultdict
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# counts[hashtag][day_of_year] = number of tweets
counts = defaultdict(lambda: defaultdict(int))

# scan every .lang file in the outputs folder
for filename in sorted(os.listdir(args.input_folder)):
    if not filename.endswith('.lang'):
        continue

    # the date is embedded in the filename, e.g. geoTwitter20-01-01.zip.lang
    datestr = filename.split('.')[0].split('geoTwitter')[-1]
    try:
        date = datetime.datetime.strptime(datestr,'%y-%m-%d')
    except ValueError:
        print('skipping',filename)
        continue
    day_of_year = date.timetuple().tm_yday

    # load the counts for this day
    path = os.path.join(args.input_folder,filename)
    with open(path) as f:
        day_counts = json.load(f)

    # sum over every language to get one total per hashtag
    for hashtag in args.hashtags:
        if hashtag in day_counts:
            counts[hashtag][day_of_year] += sum(day_counts[hashtag].values())

# plot one line per hashtag
plt.figure(figsize=(10,6))
for hashtag in args.hashtags:
    days = sorted(counts[hashtag].keys())
    values = [counts[hashtag][day] for day in days]
    plt.plot(days,values,label=hashtag)

plt.xlabel('day of the year')
plt.ylabel('number of tweets')
plt.legend()
plt.tight_layout()
plt.savefig(args.output_path)
print('saving',args.output_path)
