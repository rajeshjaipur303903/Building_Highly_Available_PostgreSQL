resource "aws_key_pair" "chalo_pem_key" {
  key_name   = "postgres-deployer-key"
  public_key = file("~/.ssh/chalo.pub")  
}

# Security Group for Primary and Replica Instances
resource "aws_security_group" "postgres_sg" {
  vpc_id = var.vpc_id
  name   = "postgres-security-group"

  ingress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = [var.vpc_cidr]
  }

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.vpc_cidr]
  }

  # Outbound rules (allow all traffic)
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "Postgres-Security-Group"
  }
}

# Primary PostgreSQL 
resource "aws_instance" "primary" {
  ami           = var.ami
  instance_type = var.instance_type
  subnet_id     = var.private_subnet_cidr 
  security_groups = [aws_security_group.postgres_sg.name]
  key_name = aws_key_pair.chalo_pem_key.key_name  
  
  depends_on = [aws_key_pair.chalo_pem_key]
  
  tags = {
    Name = "PrimaryDB"
  }
}

# Replica PostgreSQL
resource "aws_instance" "replica" {
  count         = var.replica_count
  ami           = var.ami
  instance_type = var.instance_type
  subnet_id     = var.private_subnet_cidr  
  security_groups = [aws_security_group.postgres_sg.name]
  key_name = aws_key_pair.chalo_pem_key.key_name  
  
  depends_on = [aws_key_pair.chalo_pem_key]
 
  tags = {
    Name = "ReplicaDB-${count.index + 1}"
  }
}
