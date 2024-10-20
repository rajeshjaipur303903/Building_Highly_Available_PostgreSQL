from flask import Flask, request, jsonify
import subprocess
import os
import json

app = Flask(__name__)


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

TERRAFORM_DIR = os.path.join(BASE_DIR, "terraform")
ANSIBLE_DIR = os.path.join(BASE_DIR, "ansible")
INVENTORY_FILE_PATH = os.path.join(ANSIBLE_DIR, "inventory.ini")
VARIABLES_TF_PATH = os.path.join(TERRAFORM_DIR, "variables.tf")

# Helper: Check and append to variables.tf
def append_to_variables_tf(version, instance_type, replicas):
    """Append PostgreSQL-specific variables to variables.tf if not present."""
    with open(VARIABLES_TF_PATH, 'r') as f:
        content = f.read()

    new_content = f"""
variable "postgres_version" {{ default = "{version}" }}
variable "instance_type" {{ default = "{instance_type}" }}
variable "replica_count" {{ default = {replicas} }}
"""

    # Only append if the variables are not already defined
    if "postgres_version" not in content:
        with open(VARIABLES_TF_PATH, 'a') as f:
            f.write(new_content)

# Helper: Update Ansible inventory file
def update_inventory(instance_ips, key_path):
    """Update the Ansible inventory with instance IPs and SSH key path."""
    # Avoid adding duplicate IPs to the inventory file
    if os.path.exists(INVENTORY_FILE_PATH):
        with open(INVENTORY_FILE_PATH, 'r') as f:
            existing_content = f.read()
    else:
        existing_content = ""

    primary_ip = instance_ips[0] if instance_ips else None
    replica_ips = instance_ips[1:]

    # Prepare new inventory entries
    inventory = ""

    if primary_ip and primary_ip not in existing_content:
        inventory += f"[primary]\n{primary_ip} ansible_ssh_private_key_file={key_path}\n\n"

    if replica_ips:
        inventory += "[replica]\n"
        for ip in replica_ips:
            if ip not in existing_content:
                inventory += f"{ip} ansible_ssh_private_key_file={key_path}\n"

    # Append new IPs only if they are not already in the file
    if inventory:
        with open(INVENTORY_FILE_PATH, 'a') as f:
            f.write(inventory)

@app.route('/generate', methods=['POST'])
def generate_code():
    """Generate or update Terraform and Ansible configurations."""
    data = request.get_json()
    version = data.get('postgres_version', '13')
    instance_type = data.get('instance_type', 't3.micro')
    replicas = data.get('replicas', 1)

    append_to_variables_tf(version, instance_type, replicas)

    # Generate Ansible config
    with open(f"{ANSIBLE_DIR}/all.yml", 'w') as f:
        f.write(f"""
postgres_version: {version}
max_connections: {data.get('max_connections', 100)}
shared_buffers: {data.get('shared_buffers', '128MB')}
""")

    return jsonify({"message": "Terraform and Ansible configurations updated successfully."}), 200

@app.route('/terraform/apply', methods=['POST'])
def terraform_apply():
    """Run Terraform to provision the infrastructure."""
    try:
        os.chdir(TERRAFORM_DIR)
        subprocess.run(["terraform", "init"], check=True)
        subprocess.run(["terraform", "plan"], check=True)
        subprocess.run(["terraform", "apply", "-auto-approve"], check=True)

        # Get instance IPs from Terraform output
        output = subprocess.check_output(["terraform", "output", "-json"])
        instance_data = json.loads(output)
        instance_ips = instance_data.get("instance_ips", {}).get("value", [])

        # Update the inventory file with the instance IPs
        key_path = request.json.get('key_path', '/.ssh/chalo')
        update_inventory(instance_ips, key_path)

        return jsonify({"message": "Infrastructure provisioned and inventory updated successfully."}), 200
    except subprocess.CalledProcessError as e:
        return jsonify({"error": str(e)}), 500

@app.route('/ansible/setup', methods=['POST'])
def ansible_setup():
    """Run Ansible playbook to configure PostgreSQL."""
    try:
        os.chdir(ANSIBLE_DIR)
        subprocess.run(["ansible-playbook", "-i", "inventory.ini", "setup.yml"], check=True)
        return jsonify({"message": "PostgreSQL configured successfully."}), 200
    except subprocess.CalledProcessError as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

# if __name__ == '__main__':
#     app.run(debug = True)
