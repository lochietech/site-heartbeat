# Very Basic Site Monitor
This is a quick and dirty system I slapped together to generate an alarm if my main site where the normal network monitoring is goes offline (and therefor can't get an alarm out). 
It works by an onprem server hitting an endpoint offnet once a minute. This is received by some php which writes a timestamp into a file. There is then a python script checking that this is not more than 5 minutes old. 

At some point I'll clean this up and make it multi site aware as well as more robust.

## Prerequisites 
1. Debian 11 or similar server hosted off-net
2. On prem server with the ability to connect to off-net server on port 80
3. Opsgenie or similar for raising alarm to oncall staff
4. Ability to follow Lochie's dodgy code and instructions

## Installation - Off-net server
1. Configure server with nginx, php and python3
````
apt update
apt install nginx php php7.4-fpm php7.4-cli php7.4-curl php7.4-json -y
systemctl enable php7.4-fpm nginx
systemctl start php7.4-fpm nginx
````

2. Replace /etc/nginx/sites-enabled/default with `nginx-config` and restart nginx with `systemctl restart nginx`

3. Copy index.php into /var/www/html/

4. Create a directory inside /var/www/html/ called heartbeat and allow the php script to write to it
````
mkdir /var/www/html/heartbeat/
chown -r www-data /var/www/html/heartbeat/
````

5. Test the php script by going to http://serverip:80 (it will return a blank page) and see if site.txt has been created with a timestamp inside it. Refreshing the page again should update the timestamp.

6. Copy check.py to /root/ and make executable with `chmod +x check.py` update alarm_hook as required for your alerting platform.

7. Create a systemd service for this by copying site-alarm.service into /etc/systemd/system/

8. Configure and start the systemd service
```
systemctl daemon-reload
systemctl enable site-alarm
systemctl start site-alarm
````

9. Server installation is complete, if you don't do the next part within 5 minutes it will trigger an alarm...

## Installation - On prem server

1. add the following line to `crontab -e` on your on-prem server to send a heartbeat once a minute
````
* * * * * wget http://serverip/ -O /dev/null
````

## General Security
It's worth noting the firewall on your off-net server should be only allowing connections from your onprem IP on port 80. You could also lock this down using an nginx ACL.

