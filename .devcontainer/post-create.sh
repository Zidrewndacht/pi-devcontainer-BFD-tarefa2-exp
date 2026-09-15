#!/bin/bash
set -e

mkdir -p ~/.pi/agent

cat > ~/.pi/agent/auth.json << 'EOF'
{
  "vllm-local": {
    "type": "api_key",
    "key": "vllm"
  }
}
EOF

cat > ~/.pi/agent/models.json << 'EOF'
{
  "providers": {
    "vllm-local": {
      "baseUrl": "http://host.docker.internal:8086/v1",
      "api": "openai-completions",
      "apiKey": "vllm",
      "compat": {
        "supportsDeveloperRole": false,
        "supportsReasoningEffort": false
      },
      "models": [
        {
          "id": "cyankiwi/Qwen3.8-27B-AWQ-INT4"
        }
      ]
    }
  }
}
EOF

cat > ~/.pi/agent/settings.json << 'EOF'
{
  "defaultProvider": "vllm-local",
  "defaultModel": "cyankiwi/Qwen3.8-27B-AWQ-INT4",
  "defaultThinkingLevel": "xhigh"
}
EOF

echo "Pi configured. Files in ~/.pi/agent:"
ls -la ~/.pi/agent/