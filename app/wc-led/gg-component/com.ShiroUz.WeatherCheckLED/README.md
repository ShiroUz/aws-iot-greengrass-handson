## My Project

TODO: Fill this README out!

Be sure to:

* Change the title in this README
* Edit your repository description

## License

Add License information here


## TOPIC仕様書

### Publish
#### cmd/aws_gg_handson/wc_led/${THING_NAME}/weather/req
<details>

<summary> payload </summary>

{
  "thing_name": "${THING_NAME}"
}

</details>


### Subscribe
#### cmd/aws_gg_handson/wc_led/${THING_NAME}/weather/res

<details>
<summary> payload </summary>

{
  "action": "play_sound",
  "s3_file_path": "${FILE_PATH}",
  "morning": "1",
  "evenning": "0",
  "night": "0",
  "umbrella": "1"
}

{
  "action": "change_led",
  "s3_file_path": "${FILE_PATH}",
  "morning": "1",
  "evenning": "0",
  "night": "0",
  "umbrella": "1"
}

{
  "action": "change_led",
  "morning": "1",
  "evenning": "0",
  "night": "0",
  "umbrella": "1"
}
</details>
