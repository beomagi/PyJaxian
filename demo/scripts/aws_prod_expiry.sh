cat ~/.aws/credentials | egrep "^\[|expires" |tr -d "\n"|sed 's_\[_\n\[_g'| grep 'tr-central-prod' | awk -F '=' '{print $2}'
