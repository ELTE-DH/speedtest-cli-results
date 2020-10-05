# Speedtest CLI results

Collect and plot [`speedtest-cli`](https://pypi.org/project/speedtest-cli/) results to [https://elte-dh.github.io/speedtest-cli-results](https://elte-dh.github.io/speedtest-cli-results)

# Setup
1. Install requirements: `sudo pip3 install -r requirements.txt`
2. Set basedir in backup.sh:4 cd /home/dh/speedtest-cli-results
3. Set public key at [github](https://github.com/ELTE-DH/speedtest-cli-results/settings/keys/new) and private key to `chmod 600 id_rsa.github`
4. Clone the repo (also tests key): `ssh-agent bash -c 'ssh-add id_rsa.github; git clone git@github.com:ELTE-DH/speedtest-cli-results.git'`
5. Set branch and credentials: `cd speedtest-cli-results; git config user.name 'Speedtest-CLI Bot'; git config user.email 'bot@has.no.email'; git checkout results`
6. Set crontab with `crontab -e: * * * * * /home/dh/speedtest-cli-results/upload.sh >> /home/dh/speedtest-cli-results/upload.log 2>&1` to test in every minute
