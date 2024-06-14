from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
from datetime import *
import sys
import re
from pathlib import Path

def print_datetime(dt: datetime, with_timestamp: bool = True):
    print(f'{dt:%Z (UTC%z) %A %Y-%m-%d %H:%M:%S}', end='')
    if with_timestamp:
        print(f' | {int(dt.timestamp())}')
    else:
        print()
def print_datetime_with_timezone_arrow(dt: datetime, tz: ZoneInfo, with_timestamp: bool = True):
    print(f'{datetime.now(tz):%Z (UTC%z)} -> {dt:%A %Y-%m-%d %H:%M:%S}', end='')
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

def get_zoneinfo(timezone: str, tz_abbreviations: dict):
    return ZoneInfo(tz_abbreviations.get(timezone, timezone))

def parse_date(date_str: str, dt: datetime) -> datetime:
    fields = re.split(r'[-\/]', date_str)

    match len(fields):
        case 3:
            for i in range(3):
                if fields[i] == '_':
                    match i:
                        case 0:
                            fields[i] = dt.year
                        case 1:
                            fields[i] = dt.month
                        case 2:
                            fields[i] = dt.day
                else:
                    fields[i] = int(fields[i])
            dt = dt.replace(year=fields[0], month=fields[1], day=fields[2])
        case 2:
            for i in range(2):
                if fields[i] == '_':
                    match i:
                        case 0:
                            fields[i] = dt.month
                        case 1:
                            fields[i] = dt.day
                else:
                    fields[i] = int(fields[i])
            dt = dt.replace(month=fields[0], day=fields[1])
        case 1:
            if fields[0] != '_':
                dt = dt.replace(day=int(fields[0]))
        case _:
           raise ValueError(f'Invalid date: too many fields')
    
    return dt
def parse_time(time_str: str, dt: datetime) -> datetime:
    fields = time_str.split(':')
    
    for i in range(len(fields)):
        if fields[i] == '_':
            match i:
                case 0:
                    fields[i] = dt.hour
                case 1:
                    fields[i] = dt.minute
                case 2:
                    fields[i] = dt.second
        else:
            fields[i] = int(fields[i])
    
    match len(fields):
        case 3:
            dt = dt.replace(hour=fields[0], minute=fields[1], second=fields[2])
        case 2:
            dt = dt.replace(hour=fields[0], minute=fields[1])
        case 1:
            dt = dt.replace(hour=fields[0])
        case _:
            raise ValueError(f'Invalid time: too many fields')
    
    return dt
if __name__ == '__main__':
    tz_abbreviations = read_tzabbreviation(f'{Path(sys.argv[0]).parent}/tz.txt')
    
    if len(sys.argv) == 1:
        dt_tz = (
            datetime.now(timezone.utc),
            datetime.now(get_zoneinfo('PT', tz_abbreviations)),
            datetime.now(get_zoneinfo('ET', tz_abbreviations)),
            datetime.now(get_zoneinfo('CT', tz_abbreviations)),
        )
        
        print_datetime(dt_tz[0])
        for dt in dt_tz[1:]:
            print_datetime(dt, with_timestamp=False)

        sys.exit()
    
    if len(sys.argv) == 2 and sys.argv[1] in ('-h', '--help'):
        filename = sys.argv[0].split('\\')[-1]
        print('Convert datetime to another timezone')
        print(f'Usage: {filename} [-h|--help] [entry1], [entry2]...')
        print('')
        print('-h | --help: Print this help message and exit')
        print('entry: <timezone...> [-f|--from|-t|--to|--ts] [datetime]')
        print('    timezone: The name of a timezone, e.g., UTC, US/Hawaii')
        print('    datetime: In format "date time"')
        print('        date: [[Y][M][date_delim]<D>[\'d\']] is composed of 3 integers \'Y\', \'M\', \'D\' seperated by date_delim. Up to one integer must presented as day and the remaining fields are subtituted with localtime by default.')
        print('            date_delim: one of \'/\', \'-\'.')
        print('        time: [<H>[time_delim][M][time_delim][S]] is composed of 3 integers \'H\', \'M\', \'S\' seperated by time_delim. Up to one integer must be presented as hours and the remaining fields are subtituted with localtime by default.')
        print('            time_delim: one of \':\'.')
        print('        If one number is presented, you may write \'d\' or \'t\' to dictate date or time. If none are presented, \'d\' is assumed.')
        print("        You may substitute 'Y', 'M', 'D' in date and 'H', 'M', 'S' in time with '_' to skip the field. For example: \"20:_:45\" skips minute field and minute remained to be of localtime. Note that \"_d\" and \"_t\" are errors.")
        print('        You may substitute the entire datetime with \'_\'. I don\'t know the use case of this but yes you can.')
        print('')
        print('    If datetime is not presented. It would return return the localtime of timezone.')
        print('    If datetime is presented. The operation have 2 modes based on the options before it.')
        print('        -f | --from: Convert datetime of localtime to the timezone equivalent.')
        print('        -t | --to:   Convert datetime of timezone to the localtime equivalent.')
        print('        --ts:        Same at -t but only print the timestamp.')
        print('        If no options are presented. -f is assumed.')
        print('    If no entries are supplied. It supplies with a default entry \"UTC PT ET CT\".')
        print('    You may supply with multiple entries separated by \',\'.')
        print('')
        print('NOTE')
        print('')
        print('The utility depends on \'tz.txt\' to work with timezone abbreviations, e.g., PT, ET. If it\'s not found in the working directory a default \'tz.txt\' will be generated on the spot.')
        sys.exit()
    
    entries = ' '.join(sys.argv[1:]).split(',')
    for entry in entries:
        try:
            entry = entry.strip()
            if not entry:
                continue
            
            timezones = []
            end_of_timezone_index = None
            try:
                while (end_of_timezone_index := entry.find(' ')) != -1:
                    timezones.append(get_zoneinfo(entry[:end_of_timezone_index].upper(), tz_abbreviations))
                    entry = entry[end_of_timezone_index+1:]
            except:
                pass
            
            try:
                timezones.append(get_zoneinfo(entry.upper(), tz_abbreviations))
                entry = None
                end_of_timezone_index = None
            except:
                pass
            
            if not entry:
                print_datetime(datetime.now(timezones[0]))
                for tz in timezones[1:]:
                    dt = datetime.now(tz)
                    print_datetime(dt, with_timestamp=False)
                print()
                continue
            
            args = entry.split(' ', 1)
            
            args[0] = args[0].strip()
            match args[0]:
                case '-t' | '--to':
                    mode = 't'
                    datetime_token = args[1]
                case '-f' | '--from':
                    mode = 'f'
                    datetime_token = args[1]
                case '--ts':
                    mode = 'ts'
                    datetime_token = args[1]
                case _:
                    mode = 'f'
                    datetime_token = ' '.join(args)
            
            datetime_token = datetime_token.strip()
            datetime_entry = datetime_token.split(' ', 1)
            
            if mode == 'f':
                dts = map(lambda dt: dt.astimezone(), [datetime.now()] * len(timezones))
            else:
                dts = map(lambda tz: datetime.now(tz=tz), timezones)
            
            if len(datetime_entry) == 1:
                datetime_entry[0] = datetime_entry[0].strip()
                
                if datetime_entry[0] != '_':
                    if any(datetime_entry[0].find(ch) != -1 for ch in '-/'):
                        dts = map(lambda dt: parse_date(datetime_entry[0], dt), dts)
                    elif datetime_entry[0].find(':') != -1:
                        dts = map(lambda dt: parse_time(datetime_entry[0], dt), dts)
                    else:    
                        match datetime_entry[0][-1]:
                            case 't' | 'T':
                                dts = map(lambda dt: dt.replace(hour=int(datetime_entry[0][:-1])), dts)
                            case 'd' | 'D':
                                dts = map(lambda dt: dt.replace(day=int(datetime_entry[0][:-1])), dts)
                            case _ if datetime_entry[0][-1].isnumeric():
                                dts = map(lambda dt: dt.replace(day=int(datetime_entry[0][:-1])), dts)
                            case _:
                                raise ValueError(f'Invalid datetime')
            else:
                print(datetime_entry)
                entry_date, entry_time = datetime_entry
                entry_date = entry_date.strip()
                entry_time = entry_time.strip()
                dts = map(lambda dt: parse_date(entry_date, dt), dts)
                dts = map(lambda dt: parse_time(entry_time, dt), dts)
            
            dts = list(dts)
            
            match mode:
                case 'f':
                    print_datetime(dts[0].astimezone())
                    for i in range(len(timezones)):
                        dts[i] = dts[i].astimezone(timezones[i])  
                        print_datetime(dts[i], with_timestamp=False)
                case 't':
                    dts = list(map(lambda dt: dt.astimezone(), dts))
                    print(f'Timezone: {dts[0]:%Z (UTC%z)}')
                    for i in range(len(timezones)):
                        print_datetime_with_timezone_arrow(dts[i], timezones[i])
                case 'ts':
                    dts = list(map(lambda dt: dt.astimezone(), dts))
                    print(f'Timezone: {dts[0]:%Z (UTC%z)}')
                    for i in range(len(timezones)):
                        print(f'{datetime.now(timezones[i]):%Z (UTC%z)} = {int(dts[i].timestamp())}')
                case _:
                    raise ValueError(f'Unknown mode. Please report it to the developers.')
        except Exception as e:
            print(f'Failed entry [{e}]')
            
        print()