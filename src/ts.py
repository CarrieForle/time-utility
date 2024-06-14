from datetime import *
from zoneinfo import ZoneInfo
import sys
from pathlib import Path

DATETIME_FORMAT = '%Z (UTC%z) %A %Y-%m-%d %H:%M:%S'

def print_datetime(dt: datetime, with_timestamp: bool = False):
    print(f'{dt.strftime(DATETIME_FORMAT)}', end='')
    if with_timestamp:
        print(f' | {int(dt.timestamp())}')
    else:
        print()
def read_tzabbreviation(filepath: str):
    tz_abbreviation = {}
    try:
        with open(filepath, 'r') as f:
            for line in f.readlines():
                key, value = line.split('=')
                tz_abbreviation[key.strip()] = value.strip()
    except FileNotFoundError:
        with open(filepath, 'w') as f:
            f.write('''PT=US/Pacific
PST=US/Pacific
PDT=US/Pacific
CT=US/Central
MT=US/Mountain
MST=MST
MDT=US/Mountain
AET=Australia/ACT
AEST=Australia/North
AEDT=Australia/ACT
CET=CET
CEST=CET
MET=MET
MEST=MET
ET=US/Eastern
EST=EST
EDT=US/Eastern
WET=WET
WEST=WET
NZ=NZ
NZST=NZ
NZDT=NZ
WAT=Africa/Porto-Novo
CAT=Africa/Maputo
MSK=Europe/Kirov
IST=Europe/Dublin
EEST=Europe/Tallinn
AST=America/Montserrat
ACST=Australia/Adelaide
IDT=Asia/Jerusalem
ADT=Canada/Atlantic
SAST=Africa/Johannesburg
EAT=Africa/Nairobi
SST=US/Samoa
AKDT=America/Yakutat
HST=US/Hawaii
BST=Europe/Isle_of_Man
ChST=Pacific/Guam
EET=Libya
HDT=America/Adak
NDT=America/St_Johns
WIB=Asia/Jakarta
WITA=Asia/Makassar
KST=Asia/Seoul
WIT=Asia/Jayapura
AWST=Australia/West
HKT=Asia/Hong_Kong
JST=Asia/Tokyo
PKT=Asia/Karachi''')
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
        print('-h | --help: Print this help message and exit')
        print('entry: [timezone] <timestamp>')
        print('    timezone: The name of a timezone, e.g., UTC, US/Hawaii. The local timezone is automatically presented.')
        print('    timestamp: An integer of timestamp from Epoch (UTC 1970-01-01 00:00:00)')
        print('    If no entry is presented. Current timestamp is printed and the program exits.')
        print('    You may supply with multiple entries separated by \',\'.')
        print('')
        print('NOTE')
        print('')
        print('The utility depends on \'tz.txt\' to work with timezone abbreviations, e.g., PT, ET. If it\'s not found in the working directory a default \'tz.txt\' will be generated on the spot.')
        sys.exit()
    
    tz_abbreviations = read_tzabbreviation(Path(sys.argv[0]).parent / 'tz.txt')
    
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
            
        print()