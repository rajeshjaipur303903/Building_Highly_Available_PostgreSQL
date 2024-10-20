# automation_with_flask
We take care security also in server's allow in vpc cide 
databases server in private subnet

curl -X POST http://localhost:5000/generate \
-H "Content-Type: application/json" \
-d '{
  "postgres_version": "12",
  "instance_type": "t3.micro",
  "replicas": 2,
  "max_connections": 200,
  "shared_buffers": "256MB"
}'




curl -X POST http://localhost:5000/terraform/apply \
-H "Content-Type: application/json" \
-d '{"key_path": "/path/to/private_key.pem"}'



curl -X POST http://localhost:5000/ansible/setup


POST /generate: Generate Terraform and Ansible configs with custom parameters.
POST /terraform/apply: Provision infrastructure.
POST /ansible/setup: Configure PostgreSQL with replication.
GET /status: Check the status of infrastructure.


export ANSIBLE_VAULT_PASSWORD_FILE=/workspaces/automation_with_flask/ansible/vault_pass.txt

echo "your_vault_password_here" > /path/to/project/ansible/vault_pass.txt
chmod 600 vault_pass.txt for owner has access

install
flask - pip install flask
terraform, ansible 
terraform - https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli
ansible - https://www.digitalocean.com/community/tutorials/how-to-install-and-configure-ansible-on-ubuntu-20-04


When defining encrypted variables in an Ansible vault file, the values should not include commas. The values should be provided in plain text format (which will be encrypted when you create or edit the vault).


chmod 600 ~/.ssh/id_rsa #for pem file 

add your path vault path in vault_pass.txt and export the enviroment variable
