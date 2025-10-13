#!/bin/bash

WIFI_SSID=$(aws ssm get-parameter --name /${ENVIRONMENT}/aws-gg-handson/${SUB_SID}/wifi/ssid --with-decryption --region ${AWS_DEFAULT_REGION} | jq -r '.Parameter.Value')
WIFI_PASS=$(aws ssm get-parameter --name /${ENVIRONMENT}/aws-gg-handson/${SUB_SID}/wifi/password --with-decryption --region ${AWS_DEFAULT_REGION} | jq -r '.Parameter.Value')

cat <<EOL >> ${GITHUB_WORKSPACE}/docker/wpa_supplicant.conf
network={
   ssid="${WIFI_SSID}"
   psk="${WIFI_PASS}"
}
EOL