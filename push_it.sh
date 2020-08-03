#!/bin/sh
set -x
# Posts growl notifications to iOS device using prowl & curl

# Fill in with your own Prowl API key here and remove 123456789
APIKEY=123456789
# Make up a cache filename in /tmp/ based on our PID
CACHE=/tmp/$$.cache.txt

# clipboard -> temp file CACHE
pbpaste > $CACHE

# Post notification to Prowl using curl
curl --globoff https://api.prowlapp.com/publicapi/add \
  -F apikey=$APIKEY \
  -F application=RSS \
  -F event="" \
  -F description="`cat $CACHE`"

rm $CACHE
pbcopy < /dev/null
