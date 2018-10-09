$1 # key 
$2 # instance
$3 # output filename 

aws ec2 describe-instances --filters "Name=key-name,Values="${1}"" "Name=instance-type,Values="${instance}"" "Name=instance-state-name,Values=running" --query "Reservations[*].Instances[*].PublicDnsName" --output text > "${3}".txt

