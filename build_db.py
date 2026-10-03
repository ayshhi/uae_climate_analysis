import sqlite3, pandas as pd
df=pd.read_csv('data/uae_climate_raw.csv',parse_dates=['date'])
df['year']=df.date.dt.year; df['month']=df.date.dt.month
df['date']=df.date.dt.strftime('%Y-%m-%d')
con=sqlite3.connect('data/uae_climate.db'); df.to_sql('climate_daily',con,if_exists='replace',index=False)
sql=open('sql/analysis_queries.sql').read()
qs=[q for q in sql.split(';') if 'SELECT' in q]
for i,q in enumerate(qs,1):
    name=[l for l in q.splitlines() if l.startswith('-- Q')][0]
    r=pd.read_sql(q,con); print('\n',name, '| rows:',len(r))
    if i==10: print(r.tail(3).to_string(index=False)); continue
    print(r.to_string(index=False))
