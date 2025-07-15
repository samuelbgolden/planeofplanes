# DCA coords
LAMIN=38.837905
LOMIN=-77.059469
LAMAX=38.869518
LOMAX=-77.026852

# Response schema: https://openskynetwork.github.io/opensky-api/rest.html#all-state-vectors
curl -H "Authorization: Bearer $(cat local/token.txt)" -s "https://opensky-network.org/api/states/all?lamin=$LAMIN&lomin=$LOMIN&lamax=$LAMAX&lomax=$LOMAX" | jq '.states | map(.[1])'