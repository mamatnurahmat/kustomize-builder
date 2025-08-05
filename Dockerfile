# Use Python 3.9 slim image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Install Kustomize
RUN curl -s "https://raw.githubusercontent.com/kubernetes-sigs/kustomize/master/hack/install_kustomize.sh" | bash \
    && mv kustomize /usr/local/bin/

# Install Helm
RUN curl https://get.helm.sh/helm-v3.12.0-linux-amd64.tar.gz | tar xz \
    && mv linux-amd64/helm /usr/local/bin/ \
    && rm -rf linux-amd64

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create samples directory if it doesn't exist
RUN mkdir -p samples

# Create a default sample if samples directory is empty
RUN if [ ! "$(ls -A samples)" ]; then \
    echo "apiVersion: kustomize.config.k8s.io/v1beta1\nkind: Kustomization\n\nhelmCharts:\n- name: qoin\n  repo: https://newrahmat.bitbucket.io\n  releaseName: qoin\n  namespace: admin\n  version: 0.11.0\n  valuesInline:\n    name: qoin-be-client-manager\n    port: 8086\n    image:\n      repo: loyaltolpi/qoin-be-client-manager\n      tag: 2e6d963\n    privateReg:\n      enabled: true\n    secretName: regcred\n    selector:\n      enabled: true\n    nodeSelector:\n      nodetype: front" > samples/default.yaml; \
    fi

# Expose port
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/ || exit 1

# Run the application
CMD ["python", "app.py"] 