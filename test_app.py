#!/usr/bin/env python3
"""
Simple test script for Kustomize Builder Web App
"""

import requests
import json
import time

def test_app():
    """Test the Flask application endpoints"""
    
    # Test data
    test_yaml = """apiVersion: kustomize.config.k8s.io/v1beta1
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

    print("🚀 Testing Kustomize Builder Web App...")
    print("=" * 50)
    
    # Test validation endpoint
    print("\n1. Testing YAML validation...")
    try:
        response = requests.post('http://localhost:5000/validate', 
                               json={'yaml_content': test_yaml})
        if response.status_code == 200:
            result = response.json()
            if result['valid']:
                print("✅ YAML validation passed!")
            else:
                print(f"❌ YAML validation failed: {result['error']}")
        else:
            print(f"❌ Validation request failed: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the application. Make sure it's running on http://localhost:5000")
        return
    
    # Test generation endpoint
    print("\n2. Testing Kustomize generation...")
    try:
        response = requests.post('http://localhost:5000/generate', 
                               json={'yaml_content': test_yaml})
        if response.status_code == 200:
            result = response.json()
            if result['success']:
                print("✅ Kustomize generation successful!")
                print(f"📄 Output length: {len(result['output'])} characters")
                print("📋 First 200 characters of output:")
                print("-" * 40)
                print(result['output'][:200] + "..." if len(result['output']) > 200 else result['output'])
                print("-" * 40)
            else:
                print(f"❌ Generation failed: {result['error']}")
        else:
            print(f"❌ Generation request failed: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the application.")
    
    print("\n" + "=" * 50)
    print("🎉 Test completed!")

if __name__ == "__main__":
    test_app() 