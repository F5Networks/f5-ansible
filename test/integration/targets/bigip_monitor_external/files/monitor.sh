#!/bin/sh
# (c) Copyright 1996-2007 F5 Networks, Inc.
#
# This software is confidential and may contain trade secrets that are the
# property of F5 Networks, Inc.  No part of the software may be disclosed
# to other parties without the express written consent of F5 Networks, Inc.
# It is against the law to copy the software.  No part of the software may
# be reproduced, transmitted, or distributed in any form or by any means,
# electronic or mechanical, including photocopying, recording, or information
# storage and retrieval systems, for any purpose without the express written
# permission of F5 Networks, Inc.  Our services are only available for legal
# users of the program, for instance in the event that we extend our services
# by offering the updating of files via the Internet.
#
#
# these arguments supplied automatically for all external monitors:
# $1 = IP (nnn.nnn.nnn.nnn notation or hostname)
# $2 = port (decimal, host byte order) -- not used in this monitor, assumes default port 53
# $3 = name to be looked up
# $4 = string in expected response

node_ip=`echo $1 | sed 's/::ffff://'`

pidfile="/var/run/`basename $0`.$node_ip..$2.pid"
LOGFILE="/var/log/`basename $0`.log"


if [ -f $pidfile ]
then
   kill -9 `cat $pidfile` > /dev/null 2>&1
fi
echo "$$" > $pidfile

#dig @${node_ip} ${3} | egrep -v '^$|^;' | grep ${4} > /dev/null 2>&1
#dig @${4} ${3} | egrep -v '^$|^;' | grep ${node_ip} > /dev/null 2>&1

if [ ${DEBUG} -gt 0 ]
   then
      echo "`date +"%Y-%m-%d %H:%M:%S"`|IP=${node_ip}|QUERY=${QUERY}" >> ${LOGFILE}
   fi

dig ${QUERY} | egrep -v '^$|^;' | grep ${node_ip} > /dev/null 2>&1


# For AAAA lookups, use this instead
# dig @${node_ip} ${3} AAAA| egrep -v '^$|^;' | grep ${4} > /dev/null 2>&1

status=$?
if [ $status -eq 0 ]
then
    if [ ${DEBUG} -gt 0 ]
      then
         echo "`date +"%Y-%m-%d %H:%M:%S"`|Host ${node_ip} found : UP" >> ${LOGFILE}
      fi
    echo "UP"
else
      if [ ${DEBUG} -gt 0 ]
      then
         echo "`date +"%Y-%m-%d %H:%M:%S"`|Host ${node_ip} not found : DOWN" >> ${LOGFILE}
      fi
fi

rm -f $pidfile
