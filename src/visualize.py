#!/usr/bin/env python3

# command line args
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--input_path',required=True)
parser.add_argument('--key',required=True)
parser.add_argument('--percent',action='store_true')
parser.add_argument('--output_path')
args = parser.parse_args()

# imports
import os
import json
from collections import Counter,defaultdict
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# open the input path
with open(args.input_path) as f:
    counts = json.load(f)

# normalize the counts by the total values
if args.percent:
    for k in counts[args.key]:
        counts[args.key][k] /= counts['_all'][k]

# print the count values
items = sorted(counts[args.key].items(), key=lambda item: (item[1],item[0]), reverse=True)
for k,v in items:
    print(k,':',v)

# keep only the top 10, then sort them from low to high for plotting
top = items[:10]
top.reverse()
keys = [k for k,v in top]
values = [v for k,v in top]

# generate the bar graph
plt.figure()
plt.bar(keys,values)
plt.xlabel(args.key)
plt.ylabel('percent of tweets' if args.percent else 'number of tweets')
plt.title(args.key)
plt.tight_layout()

# save the figure
output_path = args.output_path
if output_path is None:
    output_path = args.input_path + '.' + args.key.lstrip('#') + '.png'
plt.savefig(output_path)
print('saving',output_path)
