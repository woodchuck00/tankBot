# ham__fish_tank

streaming and slackbot code for PI to stream to twitch https://www.twitch.tv/markham_stein

if you can't SSH to pi

```sudo rm /etc/ssh/ssh_host_* && sudo dpkg-reconfigure openssh-server```

### packages to install
```sudo apt-get install rng-tools```
```pip install psutil```
```pip install slackclient```
```pip install requests```

### Start Twitch stream on bot
edit rc.local
```sudo nano /etc/rc.local```

add 
```sh /home/pi/fish_stream/twitch_stream.sh &```

### Start Slack bot on boot
edit crontab
```crontab -e```

add
```
@reboot python /home/pi/fish_stream/tank_bot.py >> /home/pi/fish_stream/logs/slack.out 2>&1
5 0 0 0 0 sh /home.pi/fish_stream/errors.sh
```

### twitch
get channel status
```bash
curl -H 'Client-ID: 6phnz4pj0kz6aayj5f59ci0nes7qf8' \
-X GET 'https://api.twitch.tv/helix/streams?user_login=markham_stein'
```
oauth
```
https://api.twitch.tv/kraken/oauth2/authorize
?client_id=6phnz4pj0kz6aayj5f59ci0nes7qf8
&redirect_uri=https://work.markhamandstein.com/twitch
&response_type=code
&scope=
```

case: https://www.thingiverse.com/thing:1707484/apps/print

### TODO
* add more ifs to errors.sh
