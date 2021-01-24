import sys
import argparse
import datetime


parser = argparse.ArgumentParser(description="""Generate svg from template file.""")
parser.add_argument('--group-id'    ,default='NULL')
parser.add_argument('--door-id'     ,default='NULL')
parser.add_argument('--begin-date'  ,required=True)
parser.add_argument('--end-date'    ,required=True)
parser.add_argument('--begin-time'  ,required=True)
parser.add_argument('--end-time'    ,required=True)
parser.add_argument('--days-of-week',required=True,nargs='+')
args = parser.parse_args()


begin_date = datetime.datetime.strptime(args.begin_date,'%Y%m%d')
end_date = datetime.datetime.strptime(args.end_date,'%Y%m%d')
begin_time = datetime.datetime.strptime(args.begin_time,'%H:%M')
end_time = datetime.datetime.strptime(args.end_time,'%H:%M')
days_of_week = list(map(int,args.days_of_week))

print(begin_date)
print(end_date)
print(begin_time)
print(end_time)
print(days_of_week)

#begin_delta = begin_time - datetime.datetime.fromtimestamp(0)
#end_delta = end_time - datetime.datetime.fromtimestamp(0)
#begin_delta = begin_time - datetime.datetime(1970,1,1)
#end_delta = end_time - datetime.datetime(1970,1,1)
begin_delta = begin_time - datetime.datetime.strptime('0:00','%H:%M')
end_delta = end_time - datetime.datetime.strptime('0:00','%H:%M')

print(begin_delta)
print(end_delta)

#exit()
while begin_date <= end_date:
    if begin_date.weekday() in days_of_week:
        print(begin_date+begin_delta,begin_date+end_delta,file=sys.stderr)
        print(f'INSERT INTO Tickets (group_id,door_id,begin,end) VALUES ({args.group_id},{args.door_id},{(begin_date+begin_delta).strftime("%s")},{(begin_date+end_delta).strftime("%s")});')
    begin_date += datetime.timedelta(days=1)
