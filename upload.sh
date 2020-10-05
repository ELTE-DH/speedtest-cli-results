#!/bin/bash

date
cd /home/dh/speedtest-cli-results
# rm -rf speedtest-cli-results  # Optionally start clean
# ssh-agent bash -c 'ssh-add id_rsa.github; git clone git@github.com:ELTE-DH/speedtest-cli-results.git'
cd speedtest-cli-results
ssh-agent bash -c 'ssh-add ../id_rsa.github; git pull'
git rm -- result.json
speedtest-cli --json > result.json
git add result.json
git config user.name 'Speedtest-CLI Bot'
git config user.email 'bot@has.no.email'
git commit -m 'Automated speedtest'
ssh-agent bash -c 'ssh-add ../id_rsa.github; git push'
ssh-agent bash -c 'ssh-add ../id_rsa.github; python3 ../plot_results.py'
echo # To separate entries
