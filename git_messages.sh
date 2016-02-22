DATE=$1

for i in {0..6}
do
    NEXT_DATE=$(date +%Y-%m-%d -d "$DATE + 1 day")
    echo "$DATE"

    git log --pretty="%s" --since="`date --date=$DATE`" --until="`date --date=$NEXT_DATE`" > tmp.git.log
    cat tmp.git.log
    rm tmp.git.log
    DATE=$NEXT_DATE
    echo
    echo
done
#git log --pretty="%s" --since="2016-02-17" --until="2016-02-18"
