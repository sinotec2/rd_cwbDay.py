#!/cluster/miniconda/envs/py37/bin/python
# -*- coding: UTF-8
from pandas import *
from bs4 import BeautifulSoup
import os,sys, subprocess, time


def getarg():
  """ read time period and station name from argument(std input)
  rd_cwbDay.py -d 2017-12-31 """
  import argparse
  ap = argparse.ArgumentParser()
  ap.add_argument("-d", "--DATE", required=True, type=str, help="yyyy-mm-dd")
  args = vars(ap.parse_args())
  return args['DATE']

def is_date_valid(date):
#    this_date = '%d/%d/%d' % (month, day, year)
    try:
        time.strptime(date, '%Y-%m-%d')
    except ValueError:
        return False
    else:
        return True

date = getarg()
if not  is_date_valid(date):sys.exit('not invalid:'+date)
ymd = int(date.replace('-', ''))
dir = '/autofs/master/backup/data/cwb/e-service/read_web/'
dir1 = dir + '../' + date[:4] + '/'
fnameO=dir1 + 'cwb' + str(ymd) + '.csv'
if os.path.isfile(fnameO):sys.exit('file_exit:'+date)
#touch and open for keeping from writing by others
os.system('touch '+fnameO)
ftext=open(fnameO,'w')

batcmd="date +%H"
ymdh = int(subprocess.check_output(batcmd, shell=True)[:-1])
dayt=0
if ymdh<19 and ymdh>=8:dayt=10
mal = ['T', 'V', '/', 'X']
dfS = read_csv(dir + 'stats_tab.csv')
h0 = 'https://e-service.cwb.gov.tw/HistoryDataQuery/'
h1 = 'DayDataController.do\?command=viewMain\&station\='
h2 = '\&stname\='
h3 = '\&datepicker\='

ib = 0
for ii in range(ib, len(dfS)):
  orig = h1 + dfS.loc[ii, 'stno'] + h2 + dfS.loc[ii, 'url_nam25'] + h3 + date
  os.system('wget ' + h0 + orig + ' -O cwbDay.html')
  fname = 'cwbDay.html'
  fn = open(fname, 'r',encoding='utf8')
  soup = BeautifulSoup(fn, 'html.parser')

  if ii == ib:
    col_tr = soup.find_all("tr", class_="third_tr")
    col_th = col_tr[0].find_all('th')
    col = ['stno_name'] + \
        [str(col_th[i]).split('>')[1].split('<')[0] for i in range(len(col_th))]
    df = DataFrame({i: [] for i in col})
    df.columns = col

  dfi = DataFrame({i: [] for i in col})
  dfi.columns = col
  tr = soup.find_all('tr')
  if len(tr) < 28: continue
  stno_name = str(tr[0].find_all('td')[1]).split('>')[1].split('<')[0] \
    .replace('\xc2', '').replace('\xa0', '').split(':')[1]
  ymd = str(tr[0].find_all('td')[4]).split('>')[1].split('<')[0] \
    .replace('\xc2', '').replace('\xa0', '').split(':')[1]
  ymd = int(ymd.replace('-', ''))
  for i in range(4, len(tr)):
    a = tr[i].find_all('td')
    col_val = []
    for j in range(len(a)):
      val = str(a[j]).split('>')[1].split('<')[0].replace('\xc2', '').replace('\xa0', '')
      if len(val) == 0:
        val = 0.
      else:
        if '.' not in val and val not in mal:
          try:
            val = float(val)
          except:
            val = ''
        elif val in mal:
          val = 0.
      if val == '...': val = ''
      col_val.append(val)
    col_val[0] = int(ymd * 100 + col_val[0])
    col_val = [stno_name] + col_val
    dfi.loc[i - 4, :] = col_val

  if ii == ib:
    df = dfi
  else:
    df = df.append(dfi, ignore_index=True)
  print(ii)
  sec=str(round(np.random.rand(1)[0]*dayt,2))
  os.system('sleep '+sec+'s')
  #  ifname+=1

os.system('mkdir -p ' + dir1)
df.set_index('stno_name').to_csv(ftext)
ftext.close()
sec=str(round(np.random.rand(1)[0]*dayt*12,2))
os.system('sleep '+sec+'s')
