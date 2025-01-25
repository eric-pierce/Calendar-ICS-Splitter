# Calendar-ICS-Splitter
Sorts and breaks up very large ICS files into chunks by year

Most cloud based calendars today utilize CalDAV as a sync service, which struggles with importing large ics files (typically larger than 500k to 1MB). 

This python script sorts events for a given large file by year, and breaks it up into < 1MB chunks for import to a cloud service.

There are several other similar scripts out there, but in testing they all resulted in dropped events.

Requires the following python libraries:
os
icalendar
datetime
math
