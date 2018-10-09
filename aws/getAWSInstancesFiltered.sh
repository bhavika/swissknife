$1 # key 
$2 # instance

aws ec2 describe-instances --filters "Name=key-name,Values="${1}"" "Name=instance-type,Values="${instance}"" "Name=instance-state-name,Values=running"