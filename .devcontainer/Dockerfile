FROM python:3.11

# Create the user
RUN groupadd --gid 1000 vscode && useradd --uid 1000 --gid 1000 -m vscode

RUN apt-get update && export DEBIAN_FRONTEND=noninteractive && apt-get -y install vim git curl jq bash-completion
RUN apt-get update && apt-get install -y sudo && \
    echo "node ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/vscode && \
    chmod 0440 /etc/sudoers.d/vscode

COPY . /vimms-downloader

WORKDIR /vimms-downloader

RUN pip install -r requirements.txt
