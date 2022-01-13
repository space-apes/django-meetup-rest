#!/usr/bin/bash
#script to use curl to retrieve admin JWT tokens and request an endpoint from api

#arg1 is username
#arg2 is password
#arg3 is endpoint (EX: /users/)

tokenResponse=$(curl \
		-q \
		-X POST \
		-H "Content-type: application/json" \
		-d '{"username":"'$1'", "password":"'$2'"}' \
		http://localhost:62231/api/token/)

#-d '{"username":"admin", "password":"password"}' \
#printf "\n"
#printf "\n"
#printf "\n"

accessToken=$(echo $tokenResponse | sed 's/.*access\":\"\(.*\)\".*/\1/')
refreshToken=$(echo $tokenResponse | sed 's/^.*refresh\":\"\(.*\)\",.*/\1/')


#printf "TOKEN RESPONSE:\n$tokenResponse\n"

#printf "ACCESS TOKEN:\n$accessToken\n"
#printf "REFRESH TOKEN:\n$refreshToken\n"


curl \
	     -X GET \
	     -H  "Authorization: Bearer ${accessToken}"\
	     "http://localhost:62231$3"
