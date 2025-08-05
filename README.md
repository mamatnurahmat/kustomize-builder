# 🚀 Kustomize Builder Web App

A modern web application for building and testing Kustomize YAML configurations with real-time preview.

## Features

- ✨ **Split-pane interface**: Edit YAML on the left, see generated output on the right
- 🎨 **Modern UI**: Beautiful gradient design with responsive layout
- 📝 **CodeMirror editor**: Syntax highlighting and auto-completion for YAML
- ⚡ **Real-time generation**: Generate Kubernetes manifests with `kustomize build --enable-helm`
- ✅ **YAML validation**: Built-in YAML syntax validation
- 📋 **Sample templates**: Pre-loaded sample Kustomize configurations
- 🔄 **Live preview**: Instant feedback on your Kustomize configurations
- 📋 **Copy Output**: Copy generated Kubernetes manifests after successful generation

## Prerequisites

- Python 3.7 or higher
- Kustomize CLI installed and available in PATH
- Helm (for Helm chart support)

### Installing Kustomize

#### Windows (PowerShell):
```powershell
# Using Chocolatey
choco install kustomize

# Or download from GitHub releases
# https://github.com/kubernetes-sigs/kustomize/releases
```

#### macOS:
```bash
# Using Homebrew
brew install kustomize

# Or using MacPorts
sudo port install kustomize
```

#### Linux:
```bash
# Using snap
sudo snap install kustomize

# Or download binary
curl -s "https://raw.githubusercontent.com/kubernetes-sigs/kustomize/master/hack/install_kustomize.sh" | bash
```

## Installation

1. **Clone or download the project files**

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python app.py
   ```

4. **Open your browser** and navigate to:
   ```
   http://localhost:5000
   ```

## Usage

### Basic Workflow

1. **Load Sample**: Select a sample from the dropdown to load a pre-configured Kustomize template
2. **Edit YAML**: Modify the YAML in the left panel using the syntax-highlighted editor
3. **Validate**: Click "✅ Validate" to check YAML syntax
4. **Generate**: Click "⚡ Generate" to build your Kustomize configuration
5. **View Output**: See the generated Kubernetes manifests in the right panel
6. **Copy Output**: Use the "📋 Copy Output" button that appears after successful generation

### Copy Features

- **📋 Copy Output**: Copy the generated Kubernetes manifests (appears after successful generation)

### Sample Configurations

The application comes with several pre-configured Kustomize samples:

- **Qoin Helm**: Custom Helm chart configuration for Qoin application
- **Nginx Basic**: Basic nginx deployment with patches and generators
- **WordPress Helm**: Complete WordPress setup with MariaDB and ingress
- **Redis Cluster**: Redis cluster with replication and monitoring

All samples are stored in the `samples/` directory and can be easily extended by adding new YAML files.

### Adding New Samples

You can add new samples using the utility script:

```bash
# List all available samples
python add_sample.py list

# Add a new sample
python add_sample.py add
```

Or simply add YAML files to the `samples/` directory with `.yaml` or `.yml` extension.

### Features Explained

- **YAML Editor**: Powered by CodeMirror with syntax highlighting, line numbers, and auto-indentation
- **Generate Button**: Executes `kustomize build --enable-helm` on your configuration
- **Validation**: Checks YAML syntax before generation
- **Error Handling**: Displays detailed error messages if generation fails
- **Responsive Design**: Works on desktop and mobile devices

## API Endpoints

- `GET /`: Main web interface
- `POST /generate`: Generate Kustomize output
- `POST /validate`: Validate YAML syntax
- `GET /samples`: Get list of available samples
- `GET /samples/<filename>`: Get content of a specific sample file

## Troubleshooting

### Common Issues

1. **"kustomize command not found"**
   - Ensure Kustomize is installed and available in your system PATH
   - Restart your terminal/command prompt after installation

2. **"Permission denied"**
   - On Windows, run PowerShell as Administrator
   - On Linux/macOS, ensure the script has execute permissions

3. **"Port 5000 already in use"**
   - Change the port in `app.py` line 67: `app.run(debug=True, host='0.0.0.0', port=5001)`

4. **Helm chart errors**
   - Ensure Helm is installed: `helm version`
   - Check that the Helm repository is accessible

### Debug Mode

The application runs in debug mode by default. For production deployment:

```python
# In app.py, change the last line to:
app.run(debug=False, host='0.0.0.0', port=5000)
```

## Development

### Project Structure

```
kustomization-builder/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── README.md          # This file
├── samples/           # Sample YAML configurations
│   ├── qoin-helm.yaml
│   ├── nginx-basic.yaml
│   ├── wordpress-helm.yaml
│   └── redis-cluster.yaml
└── templates/
    └── index.html     # Web interface template
```

### Adding Features

- **New Kustomize features**: Modify the `generate()` function in `app.py`
- **UI improvements**: Edit the CSS and JavaScript in `templates/index.html`
- **Additional validation**: Extend the `validate()` function

## Security Notes

- The application runs `kustomize build` commands with user-provided input
- In production, consider implementing input sanitization
- The debug mode should be disabled in production environments

## License

This project is open source and available under the MIT License.

## Contributing

Feel free to submit issues and enhancement requests! 