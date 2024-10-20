# Automation Of PostgreSQL Primary-Read-Replica 

This project provides automated infrastructure management using Terraform and Ansible to deploy a PostgreSQL primary-read-replica architecture. It returns success or error messages at each step, follows best practices in security, code modularity, and ensures idempotency.


## Features
**Dynamic code generation** -  Terraform configurations and Ansible playbooks are generated dynamically.

**API endpoints**  to manage infrastructure provisioning and configuration.

****Error handling****-  Returns success or error messages for every operation.

****Security** ** - Follows best practices at the networking and vault levels.

### Prerequisites
- Installed Python, flask, Terraform , Ansible and AWS configure 

### Installation Guide
```
Flask -     pip3 install flask  #Installing Flask
Terraform - https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli 
ansible -   https://www.digitalocean.com/community/tutorials/how-to-install-and-configure-ansible-on-ubuntu-20-04
```

# For Automation please follow these steps
### Crate a vault_password file and export the environment variable with full path 
```
echo "write_vault_password" > /<your dir path>/vault_pass.txt
chmod 600 vault_pass.txt   #for owner has access
export ANSIBLE_VAULT_PASSWORD_FILE=/workspaces/automation_with_flask/ansible/vault_pass.txt
```

### Now run the API -  so execute the below command

```
python main.py
```

# Endpoints 
### 1. POST /generate: Generate Terraform and Ansible configs with custom parameters.
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

### 2. POST /terraform/apply: Provision infrastructure.
```
curl -X POST http://localhost:5000/terraform/apply
```

### 3. POST /ansible/setup: Configure PostgreSQL with replication
```
chmod 400 ~/.ssh/chalo   #pem file
curl -X POST http://localhost:5000/ansible/setup
```
