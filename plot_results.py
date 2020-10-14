#!/usr/bin/env python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

import sys
from datetime import datetime, timedelta
from json import loads as json_loads
from json.decoder import JSONDecodeError

from git import Repo, Actor
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter


download_dict = {}
upload_dict = {}
ping_dict = {}
r = Repo('.')  # Repo name...

r.git.checkout('gh-pages')
commit = r.commit('HEAD')
commit_date = datetime.fromtimestamp(commit.committed_date)
r.git.checkout('results')
# Plot only when the last plot has been made more than two hours ago!
if datetime.now() - commit_date < timedelta(hours=2) and commit.message != 'Initial commit\n':
    print(f'Nothing to do yet ({commit_date}).')
    exit(0)

for i in r.iter_commits():
    if r.commit(i).message == 'Automated speedtest\n':
        # Get the data
        try:
            j = json_loads(r.commit(i).tree['result.json'].data_stream.read())
        except JSONDecodeError:
            print('ERROR: JSON reading failed for: ', i, file=sys.stderr)
            continue

        download = j['download']
        upload = j['upload']
        ping = j['ping']
        timestamp = datetime.strptime(j['timestamp'], '%Y-%m-%dT%H:%M:%S.%fZ')
        # Store it
        download_dict[timestamp] = download/10**6  # Megabits!
        upload_dict[timestamp] = upload/10**6  # Megabits!
        ping_dict[timestamp] = ping  # milliseconds

fig, (ax1, ax2, ax3) = plt.subplots(ncols=3)
DPI = fig.get_dpi()
fig.set_size_inches(1920.0/float(DPI), 1080.0/float(DPI))  # FULL HD image
fig.suptitle(f'Last updated on {datetime.now()}', fontsize=16)

ax1.plot(list(download_dict.keys()), list(download_dict.values()))
ax1.set_title('Download')
ax1.set_xlabel('Time (m)')
ax1.set_ylabel('Download (Megabit/s)')
ax1.xaxis.set_tick_params(rotation=30, labelsize=10)
ax1.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d %H:%M'))

ax2.plot(list(upload_dict.keys()), list(upload_dict.values()))
ax2.set_title('Upload')
ax2.set_xlabel('Time (m)')
ax2.set_ylabel('Upload (Megabit/s)')
ax2.xaxis.set_tick_params(rotation=30, labelsize=10)
ax2.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d %H:%M'))

ax3.plot(list(ping_dict.keys()), list(ping_dict.values()))
ax3.set_title('Ping')
ax3.set_xlabel('Time (m)')
ax3.set_ylabel('Ping (ms)')
ax3.xaxis.set_tick_params(rotation=30, labelsize=10)
ax3.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d %H:%M'))

plt.autoscale()
plt.tight_layout()

r.git.checkout('gh-pages')
plt.savefig('result.png')
r.index.add(['result.png'])
author = Actor('Speedtest-CLI Bot', 'bot@has.no.email')
r.index.commit(f'Update automated speedtest graph on {datetime.now()}', author=author, committer=author)
r.remotes['origin'].push()
r.git.checkout('results')
print('Pushed!')
