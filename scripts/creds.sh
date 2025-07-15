CLIENT_ID=$(cat local/credentials.json | jq -r .clientId)
CLIENT_SECRET=$(cat local/credentials.json | jq -r .clientSecret)

RESPONSE=$(curl -X POST "https://auth.opensky-network.org/auth/realms/opensky-network/protocol/openid-connect/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=client_credentials" \
  -d "client_id=$CLIENT_ID" \
  -d "client_secret=$CLIENT_SECRET")

echo $RESPONSE | jq -r .access_token > local/token.txt