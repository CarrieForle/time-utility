# Time utilities
2 Python scripts to get timestamps and convert datetime between timezones.  

You need Python>=3.10 to run the scripts.  

You may edit `tz.txt` to have the scripts recognize certain or custom timezone abbreviations.  

The scripts are written and tested on Windows 11 64-bit.

```
Convert datetime to another timezone
Usage: tz.py [-h|--help] [entry1], [entry2]...

-h | --help: Print this help message and exit
entry: <timezone...> [-f|--from|-t|--to] [datetime]
    timezone: The name of a timezone, e.g., UTC, US/Hawaii
    datetime: In format "date time"
        date: [[Y][M][date_delim]<D>['d']] is composed of 3 integers 'Y', 'M', 'D' seperated by date_delim. Up to one integer must presented as day and the remaining fields are subtituted with localtime by default.
            date_delim: one of '/', '-'.
        time: [<H>[time_delim][M][time_delim][S]] is composed of 3 integers 'H', 'M', 'S' seperated by time_delim. Up to one integer must be presented as hours and the remaining fields are subtituted with localtime by default.
            time_delim: one of ':'.
        If one number is presented, you may write 'd' or 't' to dictate date or time. If none are presented, 'd' is assumed.
        You may substitute 'Y', 'M', 'D' in date and 'H', 'M', 'S' in time with '_' to skip the field. For example: "20:_:45" skips minute field and minute remained to be of localtime. Note that "_d" and "_t" are errors.
        You may substitute the entire datetime with '_'. I don't know the use case of this but yes you can.

    If datetime is not presented. It would return return the localtime of timezone.
    If datetime is presented. The operation have 2 modes based on the options before it.
        -f | --from: Convert datetime of localtime to the timezone equivalent.
        -t | --to:   Convert datetime of timezone to the localtime equivalent.
        If neither options are presented. -f is assumed.
    If no entries are supplied. It supplies with a default entry "UTC PT ET CT".
    You may supply with multiple entries separated by ','.
```
  
```
Get datetime of timezone from timestamp
Usage: ts.py [-h|--help] [entry1], [entry2]...

-h | --help: Print this help message and exit
entry: [timezone] <timestamp>
    timezone: The name of a timezone, e.g., UTC, US/Hawaii. The local timezone is automatically presented.
    timestamp: An integer of timestamp from Epoch (UTC 1970-01-01 00:00:00)
    If no entry is presented. Current timestamp is printed and the program exits.
    You may supply with multiple entries separated by ','.
```
