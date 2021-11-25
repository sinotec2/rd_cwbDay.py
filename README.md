# [rd_cwbDay.py](https://github.com/sinotec2/rd_cwbDay.py/blob/main/rd_cwbDay.py)
Reading CWB Daily Report csv-files from Surface Automatic Station System

## dependency
- python 3
- modules used
  - pandas
  - bs4
- station definition csv: [stats_tab.csv](https://github.com/sinotec2/rd_cwbDay.py/blob/main/stats_tab.csv)

## batch scripts
- filename: [get_cwb.sh](https://github.com/sinotec2/rd_cwbDay.py/blob/main/get_cwb.sh)
- purpose: perform python and naming the resultant csv file as "cwbYYYYMMDD.csv"

## crontab
- perform the scritp every day noon time
```
  0 12  *  *  * kuang /home/backup/data/cwb/e-service/get_cwb.sh >& /home/backup/data/cwb/e-service/get_cwb.out
```

## more description
see [github.io](https://sinotec2.github.io/jtd/docs/wind_models/cwb_daily_download/)(in Chinese)

upload date: 2021-11-25 17:39:46