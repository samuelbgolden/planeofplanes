CURR_TIME=$(date +%s)
TIME_RADIUS=$((60*60*24))
START_TIME=$(($CURR_TIME - $TIME_RADIUS))
END_TIME=$(($CURR_TIME + $TIME_RADIUS))

echo "START_TIME: $START_TIME"
echo "END_TIME: $END_TIME"

echo "Airport: $2"

curl -H "Authorization: Bearer $(cat local/token.txt)" -s "https://opensky-network.org/api/flights/arrival?airport=$2&begin=$START_TIME&end=$END_TIME" | jq