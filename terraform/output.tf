output "private_key_path" {
  value = local_file.save_private_key.filename
}

output "private_key" {
  value     = tls_private_key.deployer_key.private_key_pem
  sensitive = true
}


output "instance_ips" {
  value = flatten([
    aws_instance.primary.private_ip,
    [for r in aws_instance.replica : r.private_ip]
  ])
}
