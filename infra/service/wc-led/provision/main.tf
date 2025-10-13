data "aws_caller_identity" "self" {}
module "gg_parent" {
  source  = "ShiroUz/iot-greengrass-setup/aws//parent"
  version = "~> 1.0"

  # Thing Group設定
  thing_group_parent_name = "${local.env.environment}-${local.env.project}-parent"
}

module "iot_greengrass" {
  source   = "ShiroUz/iot-greengrass-setup/aws"
  version  = "~> 1.0"
  
  for_each = { for k, v in try(local.greengrass, {}) : k => v }
  # Thing Group configuration
  thing_group_parent_name = "${local.env.environment}-${local.env.project}-parent"
  thing_group_child_name  = "${local.env.environment}-${local.env.project}-${each.key}-child"
  description             = "Weather monitoring Device Group"
  thing_group_attributes = {
    Environment = "dev"
    Project     = "aws-gg-handson"
    SubSID      = each.key
  }
  extra_policy_statement     = each.value.extra_policy_statement
  extra_iot_policy_statement = each.value.extra_iot_policy_statement

  # Things configuration
  things_base_name = "${local.env.environment}-${local.env.project}-${each.key}"
  things_amount    = 1

  # Greengrass configuration
  component_artifact_location = "arn:aws:s3:::dev-aws-gg-handson-gg-components-${data.aws_caller_identity.self.account_id}"
  # Environment configuration
  region = local.env.region
  env    = local.env.environment

  depends_on = [module.gg_parent]
}