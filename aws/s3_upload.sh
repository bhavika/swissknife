
DIRECTORY=$1
S3_URL=$2

ls $DIRECTORY > $DIRECTORY.txt

while read ds; do ./gof3r cp $DIRECTORY/$ds $S3_URL/$ds && echo $ds ; done < $DIRECTORY.txt
