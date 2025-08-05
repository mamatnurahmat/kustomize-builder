#!/usr/bin/env python3
"""
Utility script to add new samples to the Kustomize Builder
"""

import os
import sys
import yaml

def validate_yaml(content):
    """Validate YAML content"""
    try:
        yaml.safe_load(content)
        return True
    except yaml.YAMLError as e:
        print(f"❌ Invalid YAML: {e}")
        return False

def add_sample():
    """Add a new sample to the samples directory"""
    print("📝 Add New Sample to Kustomize Builder")
    print("=" * 50)
    
    # Get sample name
    sample_name = input("Enter sample name (e.g., my-app-helm): ").strip()
    if not sample_name:
        print("❌ Sample name cannot be empty")
        return
    
    # Ensure proper extension
    if not sample_name.endswith('.yaml'):
        sample_name += '.yaml'
    
    # Check if file already exists
    file_path = os.path.join('samples', sample_name)
    if os.path.exists(file_path):
        print(f"❌ Sample '{sample_name}' already exists")
        return
    
    print(f"\n📄 Creating sample: {sample_name}")
    print("Enter your Kustomize YAML configuration (press Ctrl+D when finished):")
    print("-" * 50)
    
    # Read YAML content
    lines = []
    try:
        while True:
            line = input()
            lines.append(line)
    except EOFError:
        pass
    
    content = '\n'.join(lines)
    
    if not content.strip():
        print("❌ No content provided")
        return
    
    # Validate YAML
    if not validate_yaml(content):
        return
    
    # Create samples directory if it doesn't exist
    os.makedirs('samples', exist_ok=True)
    
    # Write the file
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Sample '{sample_name}' created successfully!")
        print(f"📁 Location: {file_path}")
    except Exception as e:
        print(f"❌ Failed to create sample: {e}")

def list_samples():
    """List all available samples"""
    samples_dir = 'samples'
    if not os.path.exists(samples_dir):
        print("❌ No samples directory found")
        return
    
    print("📋 Available Samples:")
    print("=" * 30)
    
    samples = []
    for filename in os.listdir(samples_dir):
        if filename.endswith(('.yaml', '.yml')):
            display_name = filename.replace('.yaml', '').replace('.yml', '')
            display_name = display_name.replace('-', ' ').replace('_', ' ').title()
            samples.append((filename, display_name))
    
    if not samples:
        print("No samples found")
        return
    
    for filename, display_name in sorted(samples):
        print(f"• {display_name} ({filename})")

def main():
    """Main function"""
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == 'list':
            list_samples()
        elif command == 'add':
            add_sample()
        else:
            print("Usage: python add_sample.py [list|add]")
    else:
        print("Kustomize Builder Sample Manager")
        print("=" * 40)
        print("Commands:")
        print("  list  - List all available samples")
        print("  add   - Add a new sample")
        print("\nUsage: python add_sample.py [list|add]")

if __name__ == "__main__":
    main() 