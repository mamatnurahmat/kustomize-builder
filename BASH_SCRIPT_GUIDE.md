# 🐚 Bash Script Guide

## Overview

The Kustomize Builder now generates complete bash scripts using EOF (heredoc) syntax, making it easy to run kustomize build commands manually.

## How It Works

When you click the "✅ Validate" button, the application generates:

1. **Build Command**: Simple `kustomize build --enable-helm` command
2. **Bash Script**: Complete script with EOF heredoc that:
   - Creates the directory
   - Writes the YAML content using EOF
   - Runs the kustomize build command
3. **Helm Template Script**: Complete script that:
   - Adds the loyaltolpi helm repository
   - Updates helm repositories
   - Extracts valuesInline dynamically from YAML
   - Provides two options:
     - Option 1: Run helm template with dynamic set arguments
     - Option 2: Create values.yaml file and run helm template with -f flag

## Example Generated Script

```bash
#!/bin/bash

# Create directory
mkdir -p my-kustomization

# Create kustomization.yaml using EOF
cat > my-kustomization/kustomization.yaml << 'EOF'
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

helmCharts:
- name: qoin
  repo: https://newrahmat.bitbucket.io
  releaseName: qoin
  namespace: admin
  version: 0.11.0
  valuesInline:
    name: qoin-be-client-manager
    port: 8086
    image:
      repo: loyaltolpi/qoin-be-client-manager
      tag: 2e6d963
    privateReg:
      enabled: true
    secretName: regcred
    selector:
      enabled: true
    nodeSelector:
      nodetype: front
EOF

# Run kustomize build
kustomize build --enable-helm my-kustomization
```

## Example Helm Template Script

```bash
#!/bin/bash

# Add helm repository
helm repo add loyaltolpi https://newrahmat.bitbucket.io

# Update helm repositories
helm repo update

# Option 1: Run helm template with dynamic set arguments (extracted from valuesInline)
helm template loyaltolpi/qoin --set name=qoin-be-client-manager --set port=8086 --set image.repo=loyaltolpi/qoin-be-client-manager --set image.tag=2e6d963 --set privateReg.enabled=true --set secretName=regcred --set selector.enabled=true --set nodeSelector.nodetype=front

# Option 2: Create values.yaml and run helm template
cat > values.yaml << 'EOF'
name: qoin-be-client-manager
port: 8086
image:
  repo: loyaltolpi/qoin-be-client-manager
  tag: 2e6d963
privateReg:
  enabled: true
secretName: regcred
selector:
  enabled: true
nodeSelector:
  nodetype: front
EOF

helm template loyaltolpi/qoin -f values.yaml
```

## How to Use

### Option 1: Copy and Run Bash Script
1. Click "✅ Validate" in the web app
2. Copy the bash script from the right panel
3. Save it as `run_kustomize.sh`
4. Make it executable: `chmod +x run_kustomize.sh`
5. Run it: `./run_kustomize.sh`

### Option 2: Copy and Run Helm Script
1. Click "✅ Validate" in the web app
2. Copy the helm template script from the right panel
3. Save it as `run_helm.sh`
4. Make it executable: `chmod +x run_helm.sh`
5. Run it: `./run_helm.sh`

### Option 3: Run Directly
1. Copy the script content
2. Paste it directly in your terminal
3. Press Enter to execute

### Option 4: One-liner
```bash
# Copy the bash script and run in one command
curl -s http://localhost:5000/validate -X POST -H "Content-Type: application/json" \
  -d '{"yaml_content":"your-yaml-here"}' | jq -r '.bash_script' | bash

# Copy the helm script and run in one command
curl -s http://localhost:5000/validate -X POST -H "Content-Type: application/json" \
  -d '{"yaml_content":"your-yaml-here"}' | jq -r '.helm_script' | bash
```

## Benefits

- **No manual file creation**: The script creates the directory and file automatically
- **EOF heredoc**: Preserves YAML formatting and special characters
- **Complete workflow**: From YAML to running kustomize build
- **Dynamic helm arguments**: Automatically extracts valuesInline from YAML for helm template
- **Two helm options**: Choose between set arguments or values.yaml file
- **Portable**: Works on any Unix-like system (Linux, macOS, WSL)
- **Safe**: Uses single quotes around EOF to prevent variable expansion

## Features

- ✅ **Automatic directory creation**
- ✅ **EOF heredoc for YAML content**
- ✅ **Preserves formatting and indentation**
- ✅ **Handles special characters safely**
- ✅ **Complete kustomize build command**
- ✅ **Complete helm template command with dynamic set arguments**
- ✅ **Static values.yaml file generation**
- ✅ **Automatic valuesInline extraction from YAML**
- ✅ **Copy-to-clipboard functionality**

## Troubleshooting

### Script Permission Denied
```bash
chmod +x your_script.sh
```

### EOF Not Found
Make sure you're using a Unix-like shell (bash, zsh, etc.)

### Windows Users
Use WSL (Windows Subsystem for Linux) or Git Bash to run the scripts.

## API Response

The `/validate` endpoint now returns:

```json
{
  "valid": true,
  "build_command": "kustomize build --enable-helm my-kustomization",
  "sample_dir": "my-kustomization",
  "bash_script": "#!/bin/bash\n\n# Create directory\nmkdir -p my-kustomization\n\n# Create kustomization.yaml using EOF\ncat > my-kustomization/kustomization.yaml << 'EOF'\n...\nEOF\n\n# Run kustomize build\nkustomize build --enable-helm my-kustomization",
  "helm_script": "#!/bin/bash\n\n# Add helm repository\nhelm repo add loyaltolpi https://newrahmat.bitbucket.io\n\n# Update helm repositories\nhelm repo update\n\n# Option 1: Run helm template with dynamic set arguments\nhelm template loyaltolpi/qoin --set name=qoin-be-client-manager --set port=8086 --set image.repo=loyaltolpi/qoin-be-client-manager --set image.tag=2e6d963 --set privateReg.enabled=true --set secretName=regcred --set selector.enabled=true --set nodeSelector.nodetype=front\n\n# Option 2: Create values.yaml and run helm template\ncat > values.yaml << 'EOF'\nname: qoin-be-client-manager\nport: 8086\nimage:\n  repo: loyaltolpi/qoin-be-client-manager\n  tag: 2e6d963\nprivateReg:\n  enabled: true\nsecretName: regcred\nselector:\n  enabled: true\nnodeSelector:\n  nodetype: front\nEOF\n\nhelm template loyaltolpi/qoin -f values.yaml"
}
``` 