# Calendar-ICS-Splitter
Sorts events by year and breaks up very large ICS files into smaller files.

## Background
Most cloud based calendars today utilize CalDAV as a sync service, which struggles with importing large ics files (typically larger than 500k to 1MB). 

This python script sorts events for a given large file by year, and breaks it up into < 1MB chunks for import to a cloud service. This was tested with a roughly 20MB ICS file spanning > 20 years of events exported from Google Calendar.

There are several other similar scripts out there, but in testing they all resulted in dropped events.

Note that this script can take some time to run for very large ICS files.

Requires the following python libraries:
```
os
icalendar
datetime
math
```
## Issues & Contributing

Both Issues and Contributions and Pull Requests are welcome and encouraged - please feel free to open either.

## License

This project is licensed under the [GNU AGPL 3 License](http://www.gnu.org/licenses/agpl-3.0.html)

## Disclaimer
Use at your own risk.
