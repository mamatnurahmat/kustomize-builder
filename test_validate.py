#!/usr/bin/env python3
"""
Test script for the validate endpoint with build command feature
"""

import requests
import json

def test_validate_endpoint():
    """Test the validate endpoint with sample YAML"""
    
    # Sample valid YAML
    sample_yaml = """apiVersion: kustomize.config.k8s.io/v1beta1
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
      nodetype: front"""

    # Test valid YAML
    print("🧪 Testing validate endpoint with valid YAML...")
    try:
        response = requests.post('http://localhost:5000/validate', 
                               json={'yaml_content': sample_yaml})
        
        if response.status_code == 200:
            result = response.json()
            if result['valid']:
                print("✅ YAML validation successful!")
                print(f"🚀 Build command: {result['build_command']}")
                print(f"📁 Sample directory: {result['sample_dir']}")
                print(f"🐚 Bash script generated: {len(result['bash_script'])} characters")
                print(f"⚓ Helm script generated: {len(result['helm_script'])} characters")
            else:
                print(f"❌ YAML validation failed: {result['error']}")
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server. Make sure the app is running on http://localhost:5000")
    except Exception as e:
        print(f"❌ Error: {e}")

    # Test invalid YAML
    print("\n🧪 Testing validate endpoint with invalid YAML...")
    invalid_yaml = """apiVersion: kustomize.config.k8s.io/v1beta1
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
    invalid: [unclosed bracket"""

    try:
        response = requests.post('http://localhost:5000/validate', 
                               json={'yaml_content': invalid_yaml})
        
        if response.status_code == 200:
            result = response.json()
            if not result['valid']:
                print("✅ Invalid YAML correctly detected!")
                print(f"❌ Error: {result['error']}")
            else:
                print("❌ Invalid YAML was not detected!")
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server. Make sure the app is running on http://localhost:5000")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_validate_endpoint() 