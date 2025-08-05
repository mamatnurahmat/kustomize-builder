from flask import Flask, render_template, request, jsonify
import subprocess
import tempfile
import os
import yaml
import json
import shutil

app = Flask(__name__)

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
        return jsonify({'valid': True, 'error': None})
    except yaml.YAMLError as e:
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