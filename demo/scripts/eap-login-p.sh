cloudtoolopts=/home/jumper/cloudtool-opts.txt
ct_eappreprod=`cat $cloudtoolopts  | grep 060725138335 | grep "204821-PowerUser " | tr -d '[]:' | awk '{print $1}'`
ct_eapprod=`cat $cloudtoolopts  | grep 304853478528 | grep "204821-PowerUser " | tr -d '[]:' | awk '{print $1}'`

awsloginmanual () { #DEFN login to aws for cloudtool
  passwd=`cat ${HOME}/pass.txt`
  where=0
  export AWS_DEFAULT_REGION="us-east-1"
  unset AWS_PROFILE
  unset AWS_DEFAULT_PROFILE
  cloud-tool --region "$AWS_DEFAULT_REGION" login --username "mgmt\m0094748" --password "$passwd" | tee ${tmpfs}/ctlogin.txt
  sleep 0.1
  profileset=`cat ${tmpfs}/ctlogin.txt | grep "To use this cred" | sed 's_.*aws --profile __' | sed 's_ .*__'`
  echo "Set profile to $profileset. Region is $AWS_DEFAULT_REGION"
}

echo $ct_eapprod | awsloginmanual "amer"
export AWS_DEFAULT_REGION=us-east-1
export AWS_DEFAULT_PROFILE="`cat ${tmpfs}/AWS_PROFILE.txt`"
