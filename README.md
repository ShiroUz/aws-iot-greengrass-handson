## aws-iot-greengrass-handson


<table>
	<thead>
    	<tr>
      		<th style="text-align:center">English</th>
      		<th style="text-align:center"><a href="README_ja.md">日本語</a></th>
    	</tr>
  	</thead>
</table>

## Overview
This repository is a hands-on educational material for building an edge computing system using Raspberry Pi as an IoT device and leveraging AWS IoT Greengrass.

For more details, please refer to Chapter 13 "Hands-on AWS IoT Greengrass with Sample Applications" in [TECH BOOK By KINTO Technologies Vol.01](https://techbookfest.org/product/qCPrJpWLmKnLt7eWVd9zJ6).
The book is available for free download.

### Key Features
This project includes two sample applications:

#### 1. Weather Check LED (wc-led)
- Application that checks weather information and notifies via LED
- Voice synthesis functionality using AWS Lambda, Amazon Polly, and Amazon Bedrock
- Device control via IoT Core

#### 2. AI Driving Partner (ai-dp)
- AI-driven partner application
- Interactive functionality using AWS Lambda, Amazon Polly, and Amazon Bedrock
- Real-time communication via IoT Core

### Architecture
- **Device Layer**: AWS IoT Greengrass V2 running on Raspberry Pi
- **Edge Layer**: Dockerized Greengrass components
- **Cloud Layer**: AWS managed services including Lambda, IoT Core, S3, DynamoDB, Bedrock
- **IaC**: Infrastructure management with Terraform (under infra/)
- **CI/CD**: Automated Docker image build and deployment with GitHub Actions

### Technology Stack
- **Device Provisioning**: Ansible, systemd services
- **Containerization**: Docker, Docker Compose
- **Infrastructure**: Terraform
- **Language**: Python 3.13
- **CI/CD**: GitHub Actions (OIDC authentication)
- **AWS Services**: IoT Greengrass V2, IoT Core, Lambda, Bedrock, Polly, S3, DynamoDB

## Required GitHub Repository Configuration After Fork
### Parameters Used for Device Provisioning
Refer to the following for configuration instructions:
https://docs.github.com/en/actions/security-guides/using-secrets-in-github-actions

#### - Secrets
- `IMAGES_RELEASE_ROLE_ARN`: Role for placing images used by GitHub Actions in S3
  - `arn:aws:iam::${account_name}:role/aws-gg-handson-images-release-gha-role`
- `GG_COMPONENT_RELEASE_ROLE_ARN`: Role for releasing Greengrass components via GitHub Actions
  - `arn:aws:iam::${account_name}:role/aws-gg-handson-gg-component-release-gha-role`
- `GG_COMPONENT_DEPLOY_ROLE_ARN`: Role for deploying Greengrass components via GitHub Actions
  - `arn:aws:iam::${account_name}:role/aws-gg-handson-gg-component-deploy-gha-role`
- `IOT_DATA_ENDPOINT`: IoT Data endpoint
  - See `How to Check IOT_DATA_ENDPOINT` for verification method
- `IOT_CRED_ENDPOINT`: IoT Credential endpoint
  - See `How to Check IOT_CRED_ENDPOINT` for verification method
- `IMAGES_PUT_S3_BUCKET_NAME`: S3 bucket name (for image storage)

### How to Check IOT_DATA_ENDPOINT

Check the IoT Data endpoint using AWS CLI:

```bash
aws iot describe-endpoint --endpoint-type iot:Data-ATS --region ap-northeast-1
```

Set the `endpointAddress` value from the result as `IOT_DATA_ENDPOINT`.

### How to Check IOT_CRED_ENDPOINT

Check the IoT Credential endpoint using AWS CLI:

```bash
aws iot describe-endpoint --endpoint-type iot:CredentialProvider --region ap-northeast-1
```

Set the `endpointAddress` value from the result as `IOT_CRED_ENDPOINT`.

### Creating OpenID Connect
Please refer to the following for creation:

https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/configuring-openid-connect-in-amazon-web-services
