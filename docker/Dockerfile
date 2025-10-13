FROM ubuntu:focal

RUN apt-get update -qq \
 && DEBIAN_FRONTEND=noninteractive apt-get install -qqy \
  qemu-user-static \
  kpartx \
  unzip \
  wget \
  curl \
  sudo \
  ansible \
 && rm -rf /var/lib/apt/lists/*

# ansible galaxyで必要なモジュールのインストール
RUN ansible-galaxy collection install ansible.posix


# ENV PACKER_VERSION 1.6.0
ENV PACKER_VERSION 1.6.6

RUN wget https://releases.hashicorp.com/packer/${PACKER_VERSION}/packer_${PACKER_VERSION}_linux_amd64.zip -O /tmp/packer.zip && \
  unzip /tmp/packer.zip -d /bin && \
  rm /tmp/packer.zip
WORKDIR /build

# RUN wget https://github.com/solo-io/packer-builder-arm-image/releases/download/v0.1.6/packer-builder-arm-image -O /usr/bin/packer-builder-arm-image
RUN wget https://github.com/solo-io/packer-builder-arm-image/releases/download/v0.1.6/packer-builder-arm-image -O /usr/bin/packer-builder-arm-image

COPY entrypoint.sh /entrypoint.sh
# 環境変数設定用のファイルを持ってくる。
# modify file name
# COPY set_iot_env.sh /set_iot_env.sh
# COPY setup_greengrass_device.sh /setup_greengrass_device.sh
# COPY setup_greengrass_device.service /setup_greengrass_device.service
COPY wpa_supplicant.conf /wpa_supplicant.conf
COPY certs/ /

RUN chmod +x /entrypoint.sh && \
  # chmod +x /set_iot_env.sh && \
  # chmod +x /setup_greengrass_device.sh && \
  # chmod +x /setup_greengrass_device.service
  chmod +x /wpa_supplicant.conf && \
  chmod +x /usr/bin/packer-builder-arm-image

# RUN chmod +x /usr/bin/packer-builder-arm-image
ENTRYPOINT ["/entrypoint.sh"]
