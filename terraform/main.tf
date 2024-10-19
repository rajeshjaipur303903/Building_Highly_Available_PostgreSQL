resource "aws_instance" "primary" {
  ami           = "ami-0123456789abcdef0" 
  instance_type = var.instance_type

  tags = {
    Name = "PrimaryDB"
  }
}

resource "aws_instance" "replica" {
  count         = var.replica_count
  ami           = "ami-0123456789abcdef0"  
  instance_type = var.instance_type

  tags = {
    Name = "ReplicaDB-${count.index + 1}"
  }
}

