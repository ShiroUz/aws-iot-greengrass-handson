#!/bin/bash
mkdir -p ${GITHUB_WORKSPACE}/docker/certs

curl -o ${GITHUB_WORKSPACE}/docker/certs/AmazonRootCA1.pem https://www.amazontrust.com/repository/AmazonRootCA1.pem

aws ssm get-parameter --name /${ENVIRONMENT}/${ENVIRONMENT}-${PROJECT}-${SUB_SID}-${NUMBER}-thing/certificate --with-decryption --region ${AWS_DEFAULT_REGION} | jq -r '.Parameter.Value' > ${GITHUB_WORKSPACE}/docker/certs/certificate.crt
aws ssm get-parameter --name /${ENVIRONMENT}/${ENVIRONMENT}-${PROJECT}-${SUB_SID}-${NUMBER}-thing/private --with-decryption --region ${AWS_DEFAULT_REGION} | jq -r '.Parameter.Value' > ${GITHUB_WORKSPACE}/docker/certs/private.pem

chmod 700 "${GITHUB_WORKSPACE}/docker/certs"
chmod 644 "${GITHUB_WORKSPACE}/docker/certs/AmazonRootCA1.pem"
chmod 644 "${GITHUB_WORKSPACE}/docker/certs/certificate.crt"
chmod 644 "${GITHUB_WORKSPACE}/docker/certs/private.pem"
