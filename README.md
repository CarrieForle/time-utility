# Time utilities
Get timestamps and convert datetime between timezones.  

You need Python>=3.9 to run the scripts  

You may edit `tz.txt` to have the scripts recognize certain or custom timezone abbreviations.

```
Convert datetime to another timezone
Usage: tz.py [-h|--help] [entry1], [entry2]...

entry: <timezone...> [-f|--from|-t|--to] [datetime]
  timezone: The name of a timezone, e.g., UTC, US/Hawaii
  datetime: In format "[[Y][date_delim][M][date_delim]<D>['d']] [<H>['t'][time_delim][M][time_delim][S]]"
    [[Y][M][date_delim]<D>['d']] dictates date and is composed of 3 integers 'Y', 'M', 'D' seperated by date_delim. Up to one integer must presented as day and the remaining fields are subtituted with localtime by default. Leading zero is allowed.
         date_delim: one of '/', '-'.
    [<H>[time_delim][M][time_delim][S]] dictates time and is composed of 3 integers 'H', 'M', 'S' seperated by time_delim. Up to one integer must be presented as hours and the remaining fields are subtituted with localtime by default.
         time_delim: one of ':'.
  If one number is presented, you may write 'd' or 't' to dictate date or time. If both are presented, 'd' is assumed.

If datetime is not presented. It would return return the localtime of timezone.
If datetime is presented. The operation have 2 modes based on the options before it.
    -f | --from: Convert datetime of localtime to the timezone equivalent
    -t | --to:   Convert datetime of timezone to the localtime equivalent
  If neither options are presented. -f is assumed.
You may supply with multiple entries separated by ','.
```
  
```
Get datetime of timezone from timestamp
Usage: ts.py [-h|--help] [entry1], [entry2]...

entry: [timezone] <timestamp>
  timezone: The name of a timezone, e.g., UTC, US/Hawaii. A localtime timezone is automatically presented
  timestamp: An integer of timestamp from Epoch (UTC 1970-01-01 00:00:00)
If no entry is presented. Current timestamp is printed and the program exit.
You may supply with multiple entries separated by ','.
```
