# rd_cwbDay.py
Reading CWB Daily Report csv-files from Surface Automatic Station System

## dependency
- python 3
- modules used
  - pandas
  - bs4
- station definition csv: stats_tab.csv

## batch scripts
- filename: get_cwb.sh
- purpose: perform python and naming the resultant csv file as "cwbYYYYMMDD.csv"

## crontab
- perform the scritp every day noon time
```
  0 12  *  *  * kuang /home/backup/data/cwb/e-service/get_cwb.sh >& /home/backup/data/cwb/e-service/get_cwb.out
```  
