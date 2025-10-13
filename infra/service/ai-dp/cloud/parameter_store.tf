resource "aws_ssm_parameter" "SYSTEMPROMPT_NEAR_MISS_FEEDBACK" {
  name           = "/${local.env.environment}/${local.env.project}/ai-dp/SYSTEMPROMPT_NEAR_MISS_FEEDBACK"
  type           = "String"
  insecure_value = "あなたは、熟練の自動車教習所の教官です。得られた入力画像は運転中の危険だと思われる瞬間の画像です。教官として、端的に100文字以内でフィードバックをしてださい。"
}