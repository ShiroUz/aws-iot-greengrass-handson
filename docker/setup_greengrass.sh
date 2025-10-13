#!/bin/bash

# Add the repository to Apt sources:
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/debian/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/debian \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update

# Install Docker Engine, containerd, and Docker Compose
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y
echo "Docker installation completed successfully."

sudo mkdir -p "$HOME/greengrass/v2"
sudo chmod 755 "$HOME/greengrass"

sudo apt install default-jdk -y
java -version

sudo useradd --system --create-home ggc_user
sudo groupadd --system ggc_group

sudo sh -c "echo cgroup_enable=memory cgroup_memory=1 systemd.unified_cgroup_hierarchy=0 >> /boot/cmdline.txt"

curl -s https://d2s8p88vqu9w66.cloudfront.net/releases/greengrass-2.15.0.zip > greengrass-nucleus-2.15.0.zip
jarsigner -verify -certs -verbose greengrass-nucleus-2.15.0.zip
unzip greengrass-nucleus-2.15.0.zip -d GreengrassInstaller && rm greengrass-nucleus-2.15.0.zip
java -jar $HOME/GreengrassInstaller/lib/Greengrass.jar --version

# TODO: Needs Reconsider
# 手動プロビジョニング
sudo -E java -Droot="$HOME/greengrass/v2" -Dlog.store=FILE \
  -jar $HOME/GreengrassInstaller/lib/Greengrass.jar \
  --deploy-dev-tools true \
  --aws-region ap-northeast-1 \
  --provision false \
  --component-default-user ggc_user:ggc_group \
  --init-config $HOME/GreengrassInstaller/config.yaml \
  --setup-system-service true

# 自動プロビジョニング
# sudo -E java -Droot="$HOME/greengrass/v2" -Dlog.store=FILE \
#   -jar $HOME/GreengrassInstaller/lib/Greengrass.jar \
#   --deploy-dev-tools true \
#   --aws-region ap-northeast-1 \
#   --thing-name dev-ci-shirai-thing-0 \
#   --thing-group-name dev-ci-shirai-child \
#   --tes-role-name dev-ci-shirai-iot-test-greengrass-core-role \
#   --tes-role-alias-name dev-ci-shirai-iot-test-role-alias \
#   --provision true \
#   --component-default-user ggc_user:ggc_group \
#   --init-config $HOME/GreengrassInstaller/config.yaml \
#   --setup-system-service true

# sudo systemctl enable greengrass.service