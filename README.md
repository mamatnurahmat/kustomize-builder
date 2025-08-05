# 🚀 Kustomize Builder

A web-based tool for building and managing Kustomize YAML configurations with real-time validation and Kubernetes manifest generation.

## ✨ Features

- **📝 YAML Editor**: Syntax-highlighted editor with CodeMirror
- **🔍 Real-time Validation**: Validate Kustomize YAML syntax
- **⚡ Live Generation**: Generate Kubernetes manifests instantly
- **📋 Sample Management**: Dynamic sample loading from local files
- **🐚 Bash Script Generation**: Generate executable bash scripts with EOF
- **⚓ Helm Template Scripts**: Generate Helm template commands with dynamic set arguments
- **📋 Copy Output**: Copy generated manifests to clipboard
- **🎨 Modern UI**: Responsive design with beautiful interface
- **📊 Statistics**: Display line count and resource statistics
- **🔄 Flexible Layout**: Dynamic container sizing

## 🛠️ Installation

### Option 1: Docker (Recommended)

#### Quick Start
```bash
# Clone the repository
git clone <repository-url>
cd kustomization-builder

# Run with Docker Compose
docker-compose up -d

# Access the application
open http://localhost:5000
```

#### Development Mode
```bash
# Run in development mode with hot reloading
docker-compose -f docker-compose.dev.yml up -d

# View logs
docker-compose -f docker-compose.dev.yml logs -f
```

#### Production Mode with Nginx
```bash
# Run with nginx reverse proxy
docker-compose --profile production up -d

# Access via HTTPS (requires SSL certificates)
open https://localhost
```

### Option 2: Local Development

#### Prerequisites
- Python 3.9+
- Kustomize CLI
- Helm CLI

#### Setup
```bash
# Clone the repository
git clone <repository-url>
cd kustomization-builder

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py

# Access the application
open http://localhost:5000
```

## 🐳 Docker Commands

### Build and Run
```bash
# Build the image
docker build -t kustomize-builder .

# Run the container
docker run -p 5000:5000 kustomize-builder

# Run with volume mounts
docker run -p 5000:5000 -v $(pwd)/samples:/app/samples:ro kustomize-builder
```

### Docker Compose Commands
```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f kustomize-builder

# Rebuild and restart
docker-compose up -d --build

# Clean up
docker-compose down -v
```

## 📁 Project Structure

```
kustomization-builder/
├── app.py                 # Main Flask application
├── templates/
│   └── index.html        # Frontend template
├── samples/              # YAML sample files
│   ├── default.yaml
│   └── go-template.yaml
├── Dockerfile            # Docker image definition
├── docker-compose.yml    # Production compose file
├── docker-compose.dev.yml # Development compose file
├── requirements.txt      # Python dependencies
├── .dockerignore        # Docker ignore file
├── nginx/
│   └── nginx.conf       # Nginx configuration
├── add_sample.py        # Sample management utility
├── test_app.py          # Application tests
├── test_validate.py     # Validation tests
├── example_script.sh    # Example bash script
├── example_helm_script.sh # Example helm script
└── README.md           # This file
```

## 🔧 Configuration

### Environment Variables
- `FLASK_APP`: Application entry point (default: app.py)
- `FLASK_ENV`: Environment mode (development/production)
- `PYTHONUNBUFFERED`: Python output buffering (default: 1)

### Docker Environment
- `FLASK_APP=app.py`
- `FLASK_ENV=production`
- `PYTHONUNBUFFERED=1`

## 📋 Usage

### 1. Load Samples
- Use the dropdown to select from available samples
- Samples are loaded from the `samples/` directory
- Default template is automatically loaded

### 2. Edit YAML
- Edit the Kustomize YAML in the left panel
- Real-time syntax highlighting
- Auto-indentation and bracket matching

### 3. Validate
- Click "Validate" to check YAML syntax
- View generated bash and helm scripts
- See manual execution instructions

### 4. Generate
- Click "Generate" to build Kubernetes manifests
- View statistics (lines, resources)
- Copy output to clipboard

## 🐚 Generated Scripts

### Bash Script Features
- Creates directory structure
- Uses EOF heredoc for file creation
- Runs `kustomize build --enable-helm`
- Includes error handling

### Helm Template Script Features
- Adds Helm repository (`loyaltolpi`)
- Updates repositories
- Dynamic `--set` arguments from `valuesInline`
- Alternative `values.yaml` file option
- Uses `loyaltolpi/qoin` chart

## 🛠️ Development

### Adding Samples
```bash
# Use the utility script
python add_sample.py

# Or manually add files to samples/
echo "your-yaml-content" > samples/my-sample.yaml
```

### Testing
```bash
# Run application tests
python test_app.py

# Run validation tests
python test_validate.py
```

### Docker Development
```bash
# Start development environment
docker-compose -f docker-compose.dev.yml up -d

# View logs
docker-compose -f docker-compose.dev.yml logs -f

# Rebuild after changes
docker-compose -f docker-compose.dev.yml up -d --build
```

## 🔒 Security

### Production Deployment
- Use HTTPS with proper SSL certificates
- Configure nginx reverse proxy
- Set up rate limiting
- Use non-root user in containers
- Regular security updates

### Security Headers
- X-Frame-Options: DENY
- X-Content-Type-Options: nosniff
- X-XSS-Protection: 1; mode=block
- Strict-Transport-Security

## 📊 Monitoring

### Health Checks
- Application health check at `/`
- Docker health check with curl
- Nginx health check at `/health`

### Logging
- Application logs to stdout/stderr
- Nginx access and error logs
- Docker container logs

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For issues and questions:
1. Check the documentation
2. Review existing issues
3. Create a new issue with details

---

**Happy Kustomizing! 🚀** 