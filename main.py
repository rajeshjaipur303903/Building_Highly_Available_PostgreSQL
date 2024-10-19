from flask import Flask, request, jsonify
import subprocess
import os
import json

app = Flask(__name__)

# Directories for Terraform and Ansible
TERRAFORM_DIR = "./Terraform"  # Update this to your Terraform directory
ANSIBLE_DIR = "./Ansible"      # Update this to your Ansible directory
INVENTORY_FILE = "./Ansible/inventory.ini"  # Path to your Ansible inventory file

@app.route('/generate', methods=['POST'])
def generate_code():
    data = request.get_json()
    version = data.get('postgres_version', '13')
    instance_type = data.get('instance_type', 't3.micro')
    replicas = data.get('replicas', 1)
    max_connections = data.get('max_connections', 100)
    shared_buffers = data.get('shared_buffers', '128MB')

    # Generate Terraform variables
    with open(f"{TERRAFORM_DIR}/variables.tf", 'w') as f:
        f.write(f"""
variable "postgres_version" {{ default = "{version}" }}
variable "instance_type" {{ default = "{instance_type}" }}
variable "replica_count" {{ default = {replicas} }}
""")

    # Generate Ansible config
    with open(f"{ANSIBLE_DIR}/all.yml", 'w') as f:
        f.write(f"""
postgres_version: {version}
max_connections: {max_connections}
shared_buffers: {shared_buffers}
""")

    return jsonify({"message": "Terraform and Ansible configurations generated successfully."}), 200

@app.route('/terraform/apply', methods=['POST'])
def terraform_apply():
    try:
        os.chdir(TERRAFORM_DIR)
        # Initialize and apply Terraform to create infrastructure
        subprocess.run(["terraform", "init"], check=True)
        subprocess.run(["terraform", "plan"], check=True)

        # Extract the IP addresses of the instances
        output = subprocess.check_output(["terraform", "output", "-json"])
        instance_data = json.loads(output)
        instance_ips = instance_data.get("instance_ips", {}).get("value", [])

        # Update the Ansible inventory file with the instance IPs
        update_inventory(instance_ips)

        return jsonify({"message": "Infrastructure provisioned and inventory updated successfully."}), 200
    except subprocess.CalledProcessError as e:
        return jsonify({"error": str(e)}), 500

def update_inventory(instance_ips):
    """Update the Ansible inventory file with new instance IPs."""
    # Assuming the first instance is the primary and the rest are replicas
    primary_ip = instance_ips[0] if instance_ips else None
    replica_ips = instance_ips[1:] if len(instance_ips) > 1 else []

    with open(INVENTORY_FILE, 'w') as f:
        f.write("[primary]\n")  # Define the primary group
        if primary_ip:
            f.write(f"{primary_ip}\n")  # Write the primary IP

        f.write("\n[replica]\n")  # Define the replica group
        for ip in replica_ips:
            f.write(f"{ip}\n")  # Write each replica IP

@app.route('/ansible/setup', methods=['POST'])
def ansible_setup():
    try:
        os.chdir(ANSIBLE_DIR)
        subprocess.run(["ansible-playbook", "setup.yml"], check=True)
        return jsonify({"message": "PostgreSQL configured successfully."}), 200
    except subprocess.CalledProcessError as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug = True)
