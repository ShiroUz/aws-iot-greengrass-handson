module "dynamodb_table" {
  source   = "terraform-aws-modules/dynamodb-table/aws"
  for_each = { for k, v in local.dynamodb : k => v }

  name = "${local.env.environment}-${local.env.project}-wc-led-${each.key}-dynamodb"

  hash_key                       = each.value.hash_key
  range_key                      = try(each.value.range_key, null)
  ttl_enabled                    = try(each.value.ttl.ttl_enabled, null)
  ttl_attribute_name             = try(each.value.ttl.ttl_attribute_name, null)
  server_side_encryption_enabled = try(each.value.server_side_encryption_enabled, false)

  attributes = each.value.attributes
}