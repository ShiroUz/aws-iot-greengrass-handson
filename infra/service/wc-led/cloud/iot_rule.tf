module "iot_rule" {
  source         = "ShiroUz/iot-rules/aws"
  version        = "~> 1.0"
  
  for_each       = { for k, v in try(local.iot.rule, {}) : k => v }
  rule_name      = replace("${local.env.environment}_${local.env.project}_${each.key}_rule", "-", "_")
  enabled        = try(each.value.enabled, true)
  sql            = each.value.sql
  sql_version    = try(each.value.sql_version, "2016-03-23")
  lambda         = try(each.value.lambda, [])
  sqs            = try(each.value.sqs, [])
  sns            = try(each.value.sns, [])
  step_functions = try(each.value.step_functions, [])
  iot_events     = try(each.value.iot_events, [])
  dynamodbv2     = try(each.value.dynamodbv2, [])
  kinesis        = try(each.value.kinesis, [])

}