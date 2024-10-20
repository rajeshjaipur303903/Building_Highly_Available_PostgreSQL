# Automation PostgreSQL Primary-Read-Replica Architecture

#In this project, Every stage we have Response system and we maintain the error handling followed all security aspec

## Features
- Dynamic generation of Terraform code and Ansible playbooks.
- Endpoints for generating code, running Terraform plan/apply, and executing Ansible playbooks.
- Handles success and error messages at each step.
- Best practices in security, code modularity, and idempotency.

### Prerequisites
- Installed Python, flask, Terraform , Ansible and AWS configure 

### Installation Guide
```
flask - "pip install flask" 
terraform - https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli
ansible - https://www.digitalocean.com/community/tutorials/how-to-install-and-configure-ansible-on-ubuntu-20-04
```

### For Automation please follow these steps
# First crate a vault_password file and export the environment variable with full path
```
echo "your_vault_password" > /<your dir path>/vault_pass.txt
chmod 600 vault_pass.txt   #for owner has access
export ANSIBLE_VAULT_PASSWORD_FILE=/workspaces/automation_with_flask/ansible/vault_pass.txt
```

# Now run the API -  so execute the below command

```
python main.py
```

# Endpoints 
# 1. POST /generate: Generate Terraform and Ansible configs with custom parameters.
```
curl -X POST http://localhost:5000/generate \
-H "Content-Type: application/json" \
-d '{
  "postgres_version": "12",
  "instance_type": "t3.micro",
  "replicas": 2,
  "max_connections": 200,
  "shared_buffers": "256MB"
}'
```

# 2. POST /terraform/apply: Provision infrastructure.
```
curl -X POST http://localhost:5000/terraform/apply \
-H "Content-Type: application/json" \
-d '{"key_path": "/path/to/private_key.pem"}'
```

# 3. POST /ansible/setup: Configure PostgreSQL with replication
```
chmod 400 ~/.ssh/chalo   #pem file
curl -X POST http://localhost:5000/ansible/setup
```


We take care security also in server's allow in vpc cide 
databases server in private subnet











.curl -X POST http://localhost:5000/terraform/apply \
-H "Content-Type: application/json" \
-d '{"key_path": "/path/to/private_key.pem"}'
GET /status: Check the status of infrastructure.







When defining encrypted variables in an Ansible vault file, the values should not include commas. The values should be provided in plain text format (which will be encrypted when you create or edit the vault).



