cat ~/.aws/credentials | egrep "^\[|expires" |tr -d "\n"|sed 's_\[_\n\[_g'| grep 'tr-central-preprod' | awk -F '=' '{print $2}'
