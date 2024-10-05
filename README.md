## uploadgram

uploadgram uses your Telegram account to upload files up to 2GiB, from the Terminal.

- Heavily inspired by the [telegram-upload](https://github.com/Nekmo/telegram-upload)

- Installing:

`pip install uploadgram`

- Requirements:

a customized fork of `pyrogram`


# Sample Usage

```sh
$ uploadgram 7351948 /path/to/dir/or/file --delete_on_success True --fd True -t /path/to/custom/thumbnail --caption "A Custom Caption" --topic 1
```
