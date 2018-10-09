$1 # hosts file 
$2 # path to key file 
$3 # command 

parallel-ssh -i -h "${1}" -x "-oStrictHostKeyChecking=no -i "${2}"" "${3}"

