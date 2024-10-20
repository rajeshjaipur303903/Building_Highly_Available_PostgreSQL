# Automation Of PostgreSQL Primary-Read-Replica 

This automation provides infrastructure management using Terraform and Ansible to deploy a PostgreSQL primary-read-replica architecture. It returns success or error messages at each step, follows best practices in security, code modularity, and ensures idempotency.


## Features
**Dynamic code generation**   Terraform configurations and Ansible playbooks are generated dynamically.

**API endpoints**  to manage infrastructure provisioning and configuration.

****Error handling****  Returns success or error messages for every operation.

****Security****  Follows best practices at the networking and vault levels.

### Prerequisites
- Python(flask)
- Terraform
- Ansible
- AWS configure 

### Installation Guide
1. Install Flask
 ```
pip3 install flask 
```
2. Terraform
```
https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli 
```
3. Ansible
```
https://www.digitalocean.com/community/tutorials/how-to-install-and-configure-ansible-on-ubuntu-20-04
```

# Setup Instructions
### 1. Create a Vault Password File
```
echo "write_vault_password" > /<your-dir-path>/vault_pass.txt
chmod 600 /<your-dir-path>/vault_pass.txt  # Restrict access to the owner
export ANSIBLE_VAULT_PASSWORD_FILE=/workspaces/automation_with_flask/ansible/vault_pass.txt

```

### 2. Run the Flask API
Make sure the Flask application (main.py) is in the current directory
```
python main.py
```

# API Endpoints 
### 1. POST /generate
This endpoint dynamically generates Terraform and Ansible configurations with the provided parameters.

You Can Configure values here
```
curl -X POST http://localhost:5000/generate \
-H "Content-Type: application/json" \
-d '{
  "postgres_version": "12",
  "instance_type": "t4g.small",
  "replicas": 2,
  "max_connections": 200,
  "shared_buffers": "500MB"
}'
```

### 2. POST /terraform/apply
This endpoint provisions infrastructure using the generated Terraform code.

```
curl -X POST http://localhost:5000/terraform/apply
```

### 3. POST /ansible/setup
This endpoint configures PostgreSQL on the provisioned infrastructure and sets up replication.

**Before making the request,** ensure your private key file (.pem) has the correct permissions:
```
chmod 400 ~/.ssh/chalo   #pem file
```

**Request**
```
curl -X POST http://localhost:5000/ansible/setup
```

# Best Practices Followed 
**Security**
- Vault integration to secure sensitive information.
- SSH key permissions configured to ensure proper access control.

**Code Modularity**
- Terraform and Ansible code is modular, making it easy to extend and maintain.

**Idempotency**
- Ensures repeated executions result in the same state without unintended side effects.

**Error Handling**
- Provides meaningful error messages for failed operations and confirms success at each step.
