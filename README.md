# sb6141_uptime
  
This script was tested and written for the SB6141 cable modem  
on the TWC RoadRunner service.  The script should be easily  
altered to work with other modems/services.  

The script assumes that you are running a local MTA.  The MTA  
helps ensure that the emails queue up and are delivered once  
the service is restored.  

This small python script is meant to be ran from cron.  
It outputs the current date/time along with the uptime of the modem.  

If the uptime is less than the uptime from the last run then an email  
will be sent to the toaddr listed in the script.  

The script also catches the situation when the modem is offline.  
After max_retries of not being able to reach the cable modem an email will  
sent to the to toaddr listed in the script. 
