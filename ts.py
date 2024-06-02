from traceback import print_exception
from datetime import *
from zoneinfo import ZoneInfo
import sys

DATETIME_FORMAT = '%Z (UTC%z) %A %Y-%m-%d %H:%M:%S'

def print_datetime(dt: datetime, with_timestamp: bool = False):
    print(f'{dt.strftime(DATETIME_FORMAT)}', end='')
    if with_timestamp:
        print(f' | {int(dt.timestamp())}')
    else:
        print()
def read_tzabbreviation(filepath: str):
    tz_abbreviation = {}
    
    with open(filepath, 'r') as f:
        for line in f.readlines():
            key, value = line.split('=')
            tz_abbreviation[key.strip()] = value.strip()
    
    return tz_abbreviation

def get_zoneinfo(timezone: str, tz_abbreviations):
    return ZoneInfo(tz_abbreviations.get(timezone, timezone))

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print(int(datetime.now().timestamp()))
    
    if len(sys.argv) == 2 and sys.argv[1] in ('-h', '--help'):
        filename = sys.argv[0].split('\\')[-1]
        print('Get datetime of timezone from timestamp')
        print(f'Usage: {filename} [-h|--help] [entry1], [entry2]...')
        print('')
        print('entry: [timezone] <timestamp>')
        print('  timezone: The name of a timezone, e.g., UTC, US/Hawaii. A localtime timezone is automatically presented')
        print('  timestamp: A integer of timestamp from Epoch (UTC 1970-01-01 00:00:00)')
        print('If no entry is presented. Current timestamp is printed and the program exit.')
        sys.exit()
    
    tz_abbreviations = read_tzabbreviation('tz.txt')
    
    entries = ' '.join(sys.argv[1:]).split(',')
    for entry in entries:
        try:
            entry = entry.strip()
            
            if not entry:
                continue
            
            *args, timestamp = entry.split()
            
            localtime = datetime.fromtimestamp(int(timestamp)).astimezone()
            print_datetime(localtime)
            
            if len(args) == 0:
                continue
            
            timezones = list(map(lambda tz: get_zoneinfo(tz.upper(), tz_abbreviations), args))
            for tz in timezones:
                print_datetime(datetime.fromtimestamp(int(timestamp), tz=tz))
        except Exception as e:
            print(f'Failed entry [{e}]')
            print_exception(e)
            
        print()