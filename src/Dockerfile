FROM python:3.9

MAINTAINER gtaiyou24 https://github.com/gtaiyou24

ENV TZ=Asia/Tokyo

# 基本ライブラリ インストール
RUN apt-get update -y &&  \
    apt-get install -y wget curl gcc git gnupg unzip gconf-gsettings-backend

# 最新のChrome インストール
RUN sh -c 'echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list'
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN apt-get update && apt-get install -y google-chrome-stable

# インストールしたChromeとPythonのchromedriver-binaryのバージョンが合わない
# 場合があるので、google-chromeのバージョン情報から バージョンの近いものを pip installする
RUN google-chrome --version | perl -pe 's/([^0-9]+)([0-9]+\.[0-9]+).+/$2/g' > chrome-version
RUN python -m pip install --upgrade pip && \
  pip install chromedriver-binary~=`cat chrome-version` && rm chrome-version

# 最新のChromeドライバ インストール
RUN CHROMEDRIVER_VERSION=`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE` \
  && curl -sS -o /tmp/chromedriver_linux64.zip http://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip \
  && unzip /tmp/chromedriver_linux64.zip \
  && mv chromedriver /usr/bin/


ARG project_dir=/app/
ADD . $project_dir
WORKDIR $project_dir

# ライブラリをインストール
RUN pip install --upgrade pip && pip install -r requirements.txt
