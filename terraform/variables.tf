variable "region" {
  default     = "us-east-1"
}

variable "vpc_id"{
  default = " "
}

variable "vpc_cidr" {
  default     = "10.0.0.0/16"
}

variable "private_subnet_cidr" {
  default     = "10.0.1.0/24"
}

variable "ami" {
  default     = "ami-0c55b159cbfafe1f0" 
}