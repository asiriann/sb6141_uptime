#!/bin/sh
MYDATE=`date "+%Y%m%d%H%M%S"`
curl --create-dirs -o /srv/www/cable_modem/signal/${MYDATE}-signal.htm http://192.168.100.1/cmSignalData.htm -o /srv/www/cable_modem/logs/${MYDATE}-logs.htm  http://192.168.100.1/cmLogsData.htm
