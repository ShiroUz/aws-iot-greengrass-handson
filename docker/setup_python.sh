#!/bin/bash
set -x
echo "現在のPATH: $PATH" >> /tmp/debug.log
echo "実行ユーザ: $(whoami)" >> /tmp/debug.log
df -h >> /tmp/debug.log
echo "実行ユーザは: $USER"
user=$(whoami)
echo "実行ユーザは: $user"
echo "実行UIDは: $UID"

# sleep 1min, because of connect network
sleep 30

PI_HOME="/home/pi"
PYTHON_VERSION="3.12.8"
# .bashrcの再読み込み
# source $PI_HOME/.bashrc
export PATH="$HOME/.pyenv/plugins/pyenv-virtualenv/shims:$HOME/.pyenv/shims:$HOME/.pyenv/bin:$PATH"
echo "現在のPATH: $PATH" >> /tmp/debug.log

# poetry がうまくつかえられない対応
sudo apt update
sudo dpkg --configure -a
sudo apt install build-essential cmake libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev libffi-dev liblzma-dev libncurses5-dev libncursesw5-dev tk-dev python3-distutils python3-venv python3-dev -y 
sudo apt install wget curl llvm git libgdbm-dev openssl -y
# ライブラリのインストール
sudo apt install i2c-tools python3-gpiozero pigpio -y
sudo apt upgrade -y
sudo apt autoremove -y

# aws cliのインストール
# curl "https://awscli.amazonaws.com/awscli-exe-linux-aarch64.zip" -o "awscliv2.zip"
# unzip awscliv2.zip
# sudo ./aws/install

# Environment Setting
sleep 30
# if !(type "pyenv" > /dev/null 2>&1); then
# pyenvのインストール
curl -fsSL https://pyenv.run | bash
# pyenv env setting
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo '[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init - bash)"' >> ~/.bashrc
sleep 30
# df -h >> /tmp/debug.log
# sudo reboot
# fi

# pipxのインストール
sudo apt -y install pipx
pipx ensurepath
# echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc

# 再読み込み
# exec "$SHELL"
source $PI_HOME/.bashrc
pyenv install $PYTHON_VERSION -f
pyenv global $PYTHON_VERSION
alias python="python3"
echo 'alias python="python3"' >> ~/.bashrc

# if !(type "poetry" > /dev/null 2>&1); then
pipx install poetry --force
sleep 30
# df -h >> /tmp/debug.log
# sudo reboot
# fi

# poetry project config
poetry config virtualenvs.in-project true

# Greengrass用のsetup
source $HOME/setup_greengrass.sh

# Applicationを有効化
# sudo systemctl enable app.service
sudo service pigpiod start
sudo systemctl enable pigpiod

# audioデバイスの設定
cat > ~/.asoundrc << 'EOF'
pcm.!default {
    type hw
    card Headphones
    device 0
}

ctl.!default {
    type hw
    card Headphones
}
EOF
# ボリューム最大化
amixer -c Headphones set Headphone 100%

sudo cp ~/.asoundrc /etc/asound.conf

# サービスの自動起動無効
sudo systemctl disable setup_python.service

sleep 1m
df -h >> /tmp/debug.log

sudo reboot
