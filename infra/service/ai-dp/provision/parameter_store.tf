# For First Connection Wifi Parameter
# Actually, Override by User

module "wifi_ssid_child" {
  source               = "terraform-aws-modules/ssm-parameter/aws"
  for_each             = { for k, v in try(local.greengrass, {}) : k => v }
  ignore_value_changes = true
  secure_type          = true
  name                 = "/${local.env.environment}/${local.env.project}/${each.key}/wifi/ssid"
  value                = "some-value"
}

module "wifi_password_child" {
  source               = "terraform-aws-modules/ssm-parameter/aws"
  for_each             = { for k, v in try(local.greengrass, {}) : k => v }
  ignore_value_changes = true
  secure_type          = true
  name                 = "/${local.env.environment}/${local.env.project}/${each.key}/wifi/password"
  value                = "some-value"
}