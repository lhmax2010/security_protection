#!/bin/sh
# The helper's stdout goes directly to OpenSSH; credentials are never logged.
exec /usr/bin/zenity --password --title='Tizen 板 SSH 凭据（仅本机输入）' --text="${1:-请输入 SSH 密码或私钥口令}"
