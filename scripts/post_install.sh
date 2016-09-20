#!/usr/bin/env bash
# Post install script to get up and running with Docker on Ubuntu 16.04
# Available on https://gist.github.com/MarkDoggen/37e5d388d45690e4c37766adfc49207a
# Colors
colors=$(cat <<EOF
export CLICOLOR=1
export LSCOLORS=HxGxHxHxHxHxHxHxHxHxHx
C_DEFAULT="\[\033[m\]"
C_WHITE="\[\033[1m\]"
C_BLACK="\[\033[30m\]"
C_RED="\[\033[31m\]"
C_GREEN="\[\033[32m\]"
C_YELLOW="\[\033[33m\]"
C_BLUE="\[\033[34m\]"
C_PURPLE="\[\033[35m\]"
C_CYAN="\[\033[36m\]"
C_LIGHTGRAY="\[\033[37m\]"
C_DARKGRAY="\[\033[1;30m\]"
C_LIGHTRED="\[\033[1;31m\]"
C_LIGHTGREEN="\[\033[1;32m\]"
C_LIGHTYELLOW="\[\033[1;33m\]"
C_LIGHTBLUE="\[\033[1;34m\]"
C_LIGHTPURPLE="\[\033[1;35m\]"
C_LIGHTCYAN="\[\033[1;36m\]"
C_BG_BLACK="\[\033[40m\]"
C_BG_RED="\[\033[41m\]"
C_BG_GREEN="\[\033[42m\]"
C_BG_YELLOW="\[\033[43m\]"
C_BG_BLUE="\[\033[44m\]"
C_BG_PURPLE="\[\033[45m\]"
C_BG_CYAN="\[\033[46m\]"
C_BG_LIGHTGRAY="\[\033[47m\]"
export PS1="\n\$C_CYAN\u\$C_DEFAULT@\$C_LIGHTGRAY\h \$C_LIGHTGRAY: \$C_GREEN\w\n\$C_DEFAULT\$ "
EOF
)
echo "$colors" > ~/.colors

# User profile
user_profile=$(cat <<EOF
source ~/.colors

# Aliases (general)
alias profile='nano ~/.user_profile'
alias rl='source ~/.user_profile'
alias q='exit'
alias c='clear'
alias o='open'
alias cd..='cd ..'
alias ..='cd ..'
alias ...='cd ../../'
alias ....='cd ../../../'
alias grep='grep --color=auto'
alias header='curl -I -L'
alias hosts='sudo nano /etc/hosts'

# Aliases (development)
alias django='docker exec -i -t django bash'
alias redis='docker exec -i -t redis redis-cli -s /app/docker/etc/redis.sock'
alias flushredis='docker exec -i -t redis redis-cli -s /app/docker/etc/redis.sock flushall'
alias flushvarnish='docker exec -i -t varnish varnishadm -T 127.0.0.1:6082 -S /etc/varnish/secret ban.url .'
alias varnish='docker exec -i -t varnish varnishadm -T 127.0.0.1:6082 -S /etc/varnish/secret'
alias varnishstat='docker exec -i -t varnish bash -c "export TERM=xterm;varnishstat"'
alias flushtemplates='docker exec -i -t bash -c "rm -rf /app/cache/*"'
alias flushcache='flushredis && flushvarnish && flushtemplates'

# Aliases (folders)
alias ~='cd ~;ls -al'
alias home='cd /home/'
alias app='cd /home/app/'

# Functions (general)
cdl() {
  cd "\$@";
  ls -al;
}
EOF
)
echo "$user_profile" > ~/.user_profile
profile=$(cat <<EOF
source ~/.user_profile
app
EOF
)
echo "$profile" >> ~/.profile
source ~/.profile

# Install git
apt-get update
apt-get install -y git

# Install docker
apt-get update
apt-get install -y apt-transport-https ca-certificates
apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D
echo "deb https://apt.dockerproject.org/repo ubuntu-xenial main" >> /etc/apt/sources.list.d/docker.list
apt-get update
apt-get purge lxc-docker
apt-cache policy docker-engine
apt-get install -y linux-image-extra-$(uname -r) linux-image-extra-virtual
apt-get install -y docker-engine

# Install docker-compose
apt-get install -y python-pip
pip install docker-compose

# Varnish logrotate
varnish_logrotate=$(cat <<EOF
# http://go2linux.garron.me/linux/2011/05/configure-varnish-logs-varnishnsca-logrotate-and-awstats-1014/
/home/app/docker/log/varnish/*log {
    daily
    rotate 30
    size 100M
    compress
    delaycompress
    missingok
    notifempty
    create 640 root root
    copytruncate
}
EOF
)
echo "$varnish_logrotate" > /etc/logrotate.d/varnish

# Crontab
(crontab -l ; echo "*/5 * * * * docker exec django python /app/manage.py runcrons") 2>&1 | grep -v "no crontab" | sort | uniq | crontab -