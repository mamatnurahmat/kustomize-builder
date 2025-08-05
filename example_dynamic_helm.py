#!/usr/bin/env python3
"""
Example script to demonstrate dynamic helm set arguments extraction
"""

import yaml

def extract_helm_set_args(values_inline, prefix=''):
    """Extract helm --set arguments from valuesInline dictionary"""
    helm_args = []
    
    for key, value in values_inline.items():
        current_key = f"{prefix}.{key}" if prefix else key
        
        if isinstance(value, dict):
            # Recursively handle nested dictionaries
            helm_args.extend(extract_helm_set_args(value, current_key))
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

# Example YAML content
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

# Parse YAML and extract helm arguments
yaml_data = yaml.safe_load(sample_yaml)

if 'helmCharts' in yaml_data and len(yaml_data['helmCharts']) > 0:
    first_chart = yaml_data['helmCharts'][0]
    if 'valuesInline' in first_chart:
        values_inline = first_chart['valuesInline']
        helm_args = extract_helm_set_args(values_inline)
        
        print("🧪 Dynamic Helm Set Arguments Extraction")
        print("=" * 50)
        print(f"Input YAML valuesInline:")
        print(yaml.dump(values_inline, default_flow_style=False, indent=2))
        print("\nGenerated helm --set arguments:")
        for arg in helm_args:
            print(f"  {arg}")
        
        print(f"\nComplete helm command:")
        helm_set_string = ' '.join(helm_args)
        print(f"helm template loyaltolpi/qoin {helm_set_string}")
else:
    print("❌ No helmCharts found in YAML") 