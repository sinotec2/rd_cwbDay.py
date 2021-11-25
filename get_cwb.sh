#!/bin/bash
dir=/home/backup/data/cwb/e-service/read_web
today=$( date "+%Y%m%d" )
yesd=$( date -ud "$today -1days" +%Y%m%d )
y=$( date -ud $yesd +%Y )
DATE=$yesd
mkdir -p $dir/../$y
cd $dir/../$y
last=$(ls -rt *csv|tail -n1|cut -c 4-11)
if [ -z $last ];then
  last=$yesd
  days=1
else
  cmd="from datetime import date;from datetime import datetime as dt;a=dt.strptime('"$yesd"','%Y%m%d');b=dt.strptime('"$last"','%Y%m%d');print ((a-b).days)"
  days=`python -c "$cmd"`
fi
for ((day=0;day<=$days;day++));do
  cmd="import datetime;bdate=datetime.datetime.strptime('"$last"','%Y%m%d');print(str(bdate+datetime.timedelta(days="$day")).split()[0])"
  DATE=`python -c "$cmd"`
  echo $DATE $days
  $dir/rd_cwbDay.py -d $DATE
done
  

