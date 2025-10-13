#!/bin/bash
THING_NAME="${ENVIRONMENT}-${PROJECT}-${SUB_SID}-${NUMBER}-thing"
cat <<EOL > ${GITHUB_WORKSPACE}/docker/GreengrassInstaller/config.yaml
---
system:
  certificateFilePath: "/home/pi/certs/certificate.crt"
  privateKeyPath: "/home/pi/certs/private.pem"
  rootCaPath: "/home/pi/certs/AmazonRootCA1.pem"
  rootpath: "/home/pi/greengrass/v2"
  thingName: "${THING_NAME}"
services:
  aws.greengrass.Nucleus:
    componentType: "NUCLEUS"
    version: "2.15.0"
    configuration:
      awsRegion: "${AWS_DEFAULT_REGION}"
      iotRoleAlias: "${THING_NAME}-alias"
      iotDataEndpoint: "${IOT_DATA_ENDPOINT}"
      iotCredEndpoint: "${IOT_CRED_ENDPOINT}"

EOL