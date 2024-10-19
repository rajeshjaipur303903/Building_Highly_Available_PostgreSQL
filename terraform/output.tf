output "instance_ips" {
  value = [
    aws_instance.primary.private_ip,
    for r in aws_instance.replica : r.private_ip
  ]
}