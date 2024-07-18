from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
from datetime import *
import sys
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

def split_on_delimiters(pattern: str, delimiters: str=' ', maxsplit=None):
    if maxsplit != None and (maxsplit < 0):
        raise ValueError('Invalid maxsplit')
    
    result = []
    split = 0
    
    while split != maxsplit:
        indexes = tuple(filter(lambda ind: ind != -1, (pattern.find(ch) for ch in delimiters)))
        
        if not indexes:
            break
        
        index = min(indexes)
        result.append(pattern[:index])
        pattern = pattern[index + 1:]
        split += 1
    
    result.append(pattern)
        
    return result

def parse_date(date_str: str, dt: datetime) -> datetime:
    if date_str == '___':
        return dt
    
    if '_' in date_str:
        fields = date_str.split('_')
        
        for i in range(len(fields)):
            if any(fields[i].startswith(ch) for ch in '-/'):
                fields[i] = fields[i][1:]
            if any(fields[i].endswith(ch) for ch in '-/'):
                fields[i] = fields[i][:-1]
             
        if len(fields) == 3:
            for i in range(len(fields)):
                if fields[i]:
                    match i:
                        case 0:
                            dt = dt.replace(year=int(fields[i]))
                        case 1:
                            dt = dt.replace(month=int(fields[i]))
                        case 2:
                            dt = dt.replace(day=int(fields[i]))
                    break
            else:
                raise ValueError('Invalid date')
        elif len(fields) == 2:
            if date_str.startswith('_'):
                month, day = split_on_delimiters(fields[1], '-/', maxsplit=1)
                dt = dt.replace(month=int(month), day=int(day))
            elif date_str.endswith('_'):
                year, month = split_on_delimiters(fields[0], '-/', maxsplit=1)
                dt = dt.replace(year=int(year), month=int(month))
            else:
                dt = dt.replace(year=int(fields[0]), day=int(fields[1]))
        else:
            raise ValueError('Invalid date')
            
    else:
        fields = tuple(int(f) for f in split_on_delimiters(date_str, r'-/'))

        match len(fields):
            case 3:
                dt = dt.replace(year=fields[0], month=fields[1], day=fields[2])
            case 2:
                dt = dt.replace(month=fields[0], day=fields[1])
            case 1:
                dt = dt.replace(day=fields[0])
            case _:
                raise ValueError(f'Invalid date: too many fields')
    
    return dt
def parse_time(time_str: str, dt: datetime) -> datetime:
    if '_' in time_str:
        fields = time_str.split('_')
        
        for i in range(len(fields)):
            if fields[i].startswith(':'):
                fields[i] = fields[i][1:]
            if fields[i].endswith(':'):
                fields[i] = fields[i][:-1]
             
        if len(fields) == 3:
            for i in range(len(fields)):
                if fields[i]:
                    match i:
                        case 0:
                            dt = dt.replace(hour=int(fields[i]))
                        case 1:
                            dt = dt.replace(minute=int(fields[i]))
                        case 2:
                            dt = dt.replace(second=int(fields[i]))
                    break
            else:
                raise ValueError('Invalid time')
        elif len(fields) == 2:
            if time_str.startswith('_'):
                minute, second = fields[1].split(':', maxsplit=1)
                dt = dt.replace(minute=int(minute), second=int(second))
            elif time_str.endswith('_'):
                hour, second = fields[0].split(':', maxsplit=1)
                dt = dt.replace(hour=int(hour), second=int(second))
            else:
                dt = dt.replace(hour=int(fields[0]), second=int(fields[1]))
        else:
            raise ValueError('Invalid time')
            
    else:
        fields = tuple(int(f) for f in time_str.split(':'))

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
    tz_abbreviations = read_tzabbreviation(Path(sys.argv[0]).parent / 'tz.txt')
    
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
            
            def init_tz(name: str) -> ZoneInfo | None:
                def try_init_tz(name: str):
                    try:
                        return get_zoneinfo(name, tz_abbreviations)
                    except:
                        pass
                    
                if tz := try_init_tz(name.upper()):
                    return tz
                elif tz := try_init_tz(name):
                    return tz
                elif (tz_sep := name.find('/')) != -1:
                    tz_big_region = name[0].upper() + name[1:tz_sep].lower()
                    tz_small_region = name[tz_sep+1].upper() + name[tz_sep+2:].lower()

                    return try_init_tz(f'{tz_big_region}/{tz_small_region}')
            
            try:
                while (end_of_timezone_index := entry.find(' ')) != -1:
                    tzname = entry[:end_of_timezone_index]
                    
                    if tz := init_tz(tzname):
                        timezones.append(tz)
                    else:
                        break
                        
                    entry = entry[end_of_timezone_index+1:]
            except:
                pass
            
            if tz := init_tz(entry):
                timezones.append(tz)
                
                print_datetime(datetime.now(timezones[0]))
                for tz in timezones[1:]:
                    dt = datetime.now(tz)
                    print_datetime(dt, with_timestamp=False)
                print()
                continue
            
            args = entry.split(maxsplit=1)
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
            datetime_entry = datetime_token.split(maxsplit=1)
            
            if mode == 'f':
                dts = map(lambda dt: dt.astimezone(), [datetime.now()] * len(timezones))
            else:
                dts = map(lambda tz: datetime.now(tz=tz), timezones)
            
            if len(datetime_entry) == 1:
                datetime_entry[0] = datetime_entry[0].strip()
                
                if datetime_entry[0] != '_':
                    if any(ch in datetime_entry[0] for ch in r'-/'):
                        dts = map(lambda dt: parse_date(datetime_entry[0], dt), dts)
                    elif ':' in datetime_entry[0]:
                        dts = map(lambda dt: parse_time(datetime_entry[0], dt), dts)
                    else:    
                        match datetime_entry[0][-1].upper():
                            case 'T':
                                dts = map(lambda dt: parse_time(datetime_entry[0][:-1], dt), dts)
                            case 'D':
                                dts = map(lambda dt: parse_date(datetime_entry[0][:-1], dt), dts)
                            case _:
                                dts = map(lambda dt: parse_date(datetime_entry[0], dt), dts)
                                
            else:
                entry_date, entry_time = datetime_entry
                entry_date = entry_date.strip()
                entry_time = entry_time.strip()
                dts = map(lambda dt: parse_date(entry_date, dt), dts)
                dts = map(lambda dt: parse_time(entry_time, dt), dts)
            
            dts = list(dts)
            dts[0].astimezone()
            
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