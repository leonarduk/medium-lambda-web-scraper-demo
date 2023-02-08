output "base_url" {
  value = aws_api_gateway_deployment.gateway_deployment.invoke_url
}