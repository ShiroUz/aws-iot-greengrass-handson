# AI Driving Partner

An AWS IoT Greengrass component that monitors driving status and provides feedback for near-miss incidents.

## Features

- Captures images every 5 seconds during driving
- Analyzes images using optical flow to detect near-miss incidents
- Uploads near-miss images to Amazon S3
- Receives feedback from cloud processing through IoT Core
- Plays audio feedback when the driving is stable again

## Requirements

- AWS IoT Greengrass v2
- Docker
- Camera device
- Audio output

## Configuration

The component can be configured through the `recipe.yaml` file:

- `LogLevel`: Logging level (default: INFO)
- `OpticalFlowThreshold`: Threshold for optical flow changes to detect near-miss incidents
- `CaptureInterval`: Interval in seconds for capturing images

## Development

For local development:

```bash
# Build and run the development container
docker compose -f compose-dev.yaml up --build
```

## Deployment

To build and deploy the component:

```bash
# Build and push Docker images
./build-and-push.sh

# Deploy the component using AWS IoT Greengrass CLI
aws greengrassv2 create-component-version --cli-input-json file://deployment.json
```

## Architecture

This component works in coordination with cloud services:

1. The device captures and analyzes driving images
2. Near-miss incidents are detected and images uploaded to S3
3. Cloud services process the image and generate feedback
4. Feedback is sent to the device via IoT Core
5. The device plays audio feedback when the driving is stable

## Topics

- Publish: `cmd/{thing_name}/near-miss/detected`
- Subscribe: `cmd/{thing_name}/near-miss/feedback`