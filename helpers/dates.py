from datetime import datetime, timedelta

def month_add(dt, mths) -> str:
    '''Add 3 full calendar months'''
    _date = datetime.strptime(dt, '%Y-%m-%d')
    
    # day 28 exists in every month
    for _ in range(1, mths+1):
        _date = ((_date.replace(day=28) + timedelta(days=4)).replace(day=1))
    
    # day minus one will be previous month's last day
    return (_date - timedelta(days=1)).strftime('%Y-%m-%d')

def month_end(dt):
    '''Convert the date to end of the month'''
    return (dt.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)
    