#!/usr/bin/python3
import os
import time

#Webhook for raising alarm
alarm_hook = "curl -X POST https://api.opsgenie.com/v2/alerts -H \"Content-Type: application/json\" -H \"Authorization: <YOUR OPS GENIE KEY" -d '{\"message\": \"CORE NETWORK HEARTBEAT NOT RECEIVED\",\"description\":\"<YOUR MESSAGE HERE>\",\"tags\": [\"OverwriteQuietHours\",\"Critical\"],\"priority\":\"P1\"}'"

while True:

    #Previous Update
    moddate_last = os.stat("/var/www/html/heartbeat/site.txt") [8]

    #Delay between checking for heartbeats
    time.sleep(300)

    #Current Update
    moddate_now = os.stat("/var/www/html/heartbeat/site.txt") [8]

    #Check if file hasn't been updated
    if moddate_now == moddate_last:
        print(("No new heartbeat received since ")+str(moddate_last)+(" - Raising Alarm"))
        os.system(alarm_hook)
        #Sleep for 30 min while issue fixed
        print("Waiting 30 minutes for issue to be triaged")
        time.sleep(1800)
    else:
        print(("Heartbeat Received ")+str(moddate_now)+( "- Doing Nothing"))

        