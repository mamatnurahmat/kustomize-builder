from flask import Flask, render_template, request, jsonify
import subprocess
import tempfile
import os
import yaml
import json
import shutil

app = Flask(__name__)

def _extract_helm_set_args(values_inline, prefix=''):
    """Extract helm --set arguments from valuesInline dictionary"""
    helm_args = []
    
    for key, value in values_inline.items():
        current_key = f"{prefix}.{key}" if prefix else key
        
        if isinstance(value, dict):
            # Recursively handle nested dictionaries
            helm_args.extend(_extract_helm_set_args(value, current_key))
        elif isinstance(value, bool):
            # Handle boolean values
            helm_args.append(f"--set {current_key}={str(value).lower()}")
        elif isinstance(value, (int, float)):
            # Handle numeric values
            helm_args.append(f"--set {current_key}={value}")
        else:
            # Handle string values
            helm_args.append(f"--set {current_key}={value}")
    
    return helm_args

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    try:
        # Get the YAML content from the request
        yaml_content = request.json.get('yaml_content', '')
        
        # Create a temporary directory for kustomize build
        temp_dir = tempfile.mkdtemp()
        kustomization_file = os.path.join(temp_dir, 'kustomization.yaml')
        
        # Write the YAML content to kustomization.yaml
        with open(kustomization_file, 'w') as f:
            f.write(yaml_content)
        
        # Run kustomize build command on the directory
        result = subprocess.run(
            ['kustomize', 'build', '--enable-helm', temp_dir],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        # Clean up the temporary directory
        shutil.rmtree(temp_dir)
        
        if result.returncode == 0:
            return jsonify({
                'success': True,
                'output': result.stdout,
                'error': None
            })
        else:
            return jsonify({
                'success': False,
                'output': None,
                'error': result.stderr
            })
            
    except subprocess.TimeoutExpired:
        return jsonify({
            'success': False,
            'output': None,
            'error': 'Build timed out. Please check your YAML configuration.'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'output': None,
            'error': str(e)
        })

@app.route('/validate', methods=['POST'])
def validate():
    try:
        yaml_content = request.json.get('yaml_content', '')
        yaml.safe_load(yaml_content)
        
        # Generate a sample directory name for display
        sample_dir = "my-kustomization"
        
        # Generate the kustomize build command
        build_command = f"kustomize build --enable-helm {sample_dir}"
        
        # Generate bash script with EOF
        bash_script = f"""#!/bin/bash

# Create directory
mkdir -p {sample_dir}

# Create kustomization.yaml using EOF
cat > {sample_dir}/kustomization.yaml << 'EOF'
{yaml_content}
EOF

# Run kustomize build
kustomize build --enable-helm {sample_dir}
"""

        # Parse YAML to extract valuesInline for dynamic helm template
        try:
            yaml_data = yaml.safe_load(yaml_content)
            helm_set_args = []
            
            # Extract valuesInline from the first helmChart
            if 'helmCharts' in yaml_data and len(yaml_data['helmCharts']) > 0:
                first_chart = yaml_data['helmCharts'][0]
                if 'valuesInline' in first_chart:
                    values_inline = first_chart['valuesInline']
                    helm_set_args = _extract_helm_set_args(values_inline)
            
            # Generate helm template script with dynamic set arguments
            helm_set_string = ' '.join(helm_set_args) if helm_set_args else '--set name=qoin-be-client-manager --set port=8086 --set image.repo=loyaltolpi/qoin-be-client-manager --set image.tag=2e6d963 --set privateReg.enabled=true --set secretName=regcred --set selector.enabled=true --set nodeSelector.nodetype=front'
            
            # Generate values.yaml content from valuesInline
            values_yaml = yaml.dump(values_inline, default_flow_style=False, indent=2) if 'valuesInline' in first_chart else ""
            
            helm_script = f"""#!/bin/bash

# Add helm repository
helm repo add loyaltolpi https://newrahmat.bitbucket.io

# Update helm repositories
helm repo update

# Option 1: Run helm template with dynamic set arguments
helm template loyaltolpi/qoin {helm_set_string}

# Option 2: Create values.yaml and run helm template
cat > values.yaml << 'EOF'
{values_yaml}
EOF

helm template loyaltolpi/qoin -f values.yaml
"""
        except Exception as e:
            # Fallback to default values if parsing fails
            default_values_yaml = """name: qoin-be-client-manager
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
  nodetype: front"""
            
            helm_script = f"""#!/bin/bash

# Add helm repository
helm repo add loyaltolpi https://newrahmat.bitbucket.io

# Update helm repositories
helm repo update

# Option 1: Run helm template with set arguments
helm template loyaltolpi/qoin --set name=qoin-be-client-manager --set port=8086 --set image.repo=loyaltolpi/qoin-be-client-manager --set image.tag=2e6d963 --set privateReg.enabled=true --set secretName=regcred --set selector.enabled=true --set nodeSelector.nodetype=front

# Option 2: Create values.yaml and run helm template
cat > values.yaml << 'EOF'
{default_values_yaml}
EOF

helm template loyaltolpi/qoin -f values.yaml
"""
        
        return jsonify({
            'valid': True, 
            'error': None,
            'build_command': build_command,
            'sample_dir': sample_dir,
            'bash_script': bash_script,
            'helm_script': helm_script
        })
    except yaml.YAMLError as e:
        return jsonify({'valid': False, 'error': str(e)})
    except Exception as e:
        return jsonify({'valid': False, 'error': str(e)})

@app.route('/samples', methods=['GET'])
def get_samples():
    """Get list of available sample files"""
    try:
        samples_dir = 'samples'
        if not os.path.exists(samples_dir):
            return jsonify({'samples': []})
        
        samples = []
        for filename in os.listdir(samples_dir):
            if filename.endswith('.yaml') or filename.endswith('.yml'):
                # Remove extension for display name
                display_name = filename.replace('.yaml', '').replace('.yml', '')
                # Convert to readable format (e.g., qoin-helm -> Qoin Helm)
                display_name = display_name.replace('-', ' ').replace('_', ' ').title()
                samples.append({
                    'filename': filename,
                    'display_name': display_name
                })
        
        return jsonify({'samples': samples})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/samples/<filename>', methods=['GET'])
def get_sample(filename):
    """Get content of a specific sample file"""
    try:
        # Security: only allow .yaml and .yml files
        if not filename.endswith(('.yaml', '.yml')):
            return jsonify({'error': 'Invalid file type'}), 400
        
        file_path = os.path.join('samples', filename)
        if not os.path.exists(file_path):
            return jsonify({'error': 'Sample not found'}), 404
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return jsonify({'content': content})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 