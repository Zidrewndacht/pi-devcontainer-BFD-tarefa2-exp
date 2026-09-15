FROM mcr.microsoft.com/devcontainers/javascript-node:22

# Common tools the agent expects (git, ripgrep, fd, jq, curl)
RUN apt-get update && apt-get install -y \
    git ripgrep fd-find jq curl \
    && rm -rf /var/lib/apt/lists/* \
    && ln -s $(which fdfind) /usr/local/bin/fd

# Install the Pi coding agent globally
RUN npm install -g @earendil-works/pi-coding-agent

# Pre-create the pi config directory owned by the non-root user
RUN mkdir -p /home/node/.pi/agent && chown -R node:node /home/node/.pi

WORKDIR /workspace