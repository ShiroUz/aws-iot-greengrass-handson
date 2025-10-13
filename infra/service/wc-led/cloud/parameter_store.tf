resource "aws_ssm_parameter" "SYSTEMPROMPT_WEATHER_CHECK" {
  name           = "/${local.env.environment}/${local.env.project}/wc-led/SYSTEMPROMPT_WEATHER_CHECK"
  type           = "String"
  insecure_value = "メッセージの本文の最後に記載されている住所の本日の天気予報を教えてください。3つの情報を提供してもらいたいです。1つ目は本日の午前中/午後/夜の気温がそれぞれ前日の気温より高いか低いかです。2つ目は本日のと傘が必要となるか否かです。3つ目は、1日が頑張れるよう付随情報もです。全体的に、ニュースのアナウンサーが話すような出力を意識してください。以下から、住所情報です。: "
}

resource "aws_ssm_parameter" "SYSTEMPROMPT_TRANSFER_LED_POW" {
  name           = "/${local.env.environment}/${local.env.project}/wc-led/SYSTEMPROMPT_TRANSFER_LED_POW"
  type           = "String"
  insecure_value = "以下の文章から厳密にjson形式に変換させてください。気温が低いか高いかについて、低い場合は0、高い場合は1を出力させます。また、傘の有無は必要ない場合は0、必要な場合は1を出力させます。以下は、templateとなります。{morning: 午前中の気温, evening: 午後の気温, night: 夜の気温, umbrella: 傘の有無}  以下は例となります。{morning: 1, evening: 1, night: 0, umbrella: 1}"
}