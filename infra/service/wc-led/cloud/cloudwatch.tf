module "log_group" {
  for_each          = { for k, v in try(local.cloudwatch.log_group, {}) : k => v }
  source            = "terraform-aws-modules/cloudwatch/aws//modules/log-group"
  version           = "~> 3.0"
  name              = each.value.name
  retention_in_days = each.value.retention_in_days
}

module "log_anomaly_detector" {
  for_each = { for k, v in try(local.cloudwatch.log_group, {}) : k => v }
  source   = "terraform-aws-modules/cloudwatch/aws//modules/log-anomaly-detector"

  detector_name           = "${local.env.environment}-${local.env.project}-${each.key}-log-anomaly-detector"
  log_group_arns          = [module.log_group[each.key].cloudwatch_log_group_arn]
  anomaly_visibility_time = 7
  enabled                 = true
  evaluation_frequency    = "FIVE_MIN"
}