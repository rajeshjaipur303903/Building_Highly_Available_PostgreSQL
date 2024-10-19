# automation_with_flask
We take care security also in server's allow in vpc cide 
databases server in private subnet

curl -X POST http://localhost:5000/generate \
-H "Content-Type: application/json" \
-d '{
  "postgres_version": "13",
  "instance_type": "t3.micro",
  "replicas": 2,
  "max_connections": 200,
  "shared_buffers": "256MB"
}'




curl -X POST http://localhost:5000/terraform/apply \
-H "Content-Type: application/json" \
-d '{"key_path": "/path/to/private_key.pem"}'



curl -X POST http://localhost:5000/ansible/setup
