#!/usr/bin/env python3
"""
Calendar ICS Splitter by Eric Pierce
https://github.com/eric-pierce/Calendar-ICS-Splitter/

Sorts and splits very large ICS files into chunks by year for easy import into a cloud service (iClcoud, Google Calendar, etc)

Usage:
    python3 calsplity.py INPUT_CALENDAR

Arguments:
    INPUT_CALENDAR: Large ICS file


Requirements:
    os
    icalendar
    datetime
    math
"""

import os
from icalendar import Calendar
from datetime import datetime
import math

def get_event_date(event):
    """Extract the start date from an event for sorting"""
    for date_field in ['DTSTART', 'DTSTAMP', 'CREATED']:
        if date_field in event:
            dt = event[date_field].dt
            # Convert datetime to date if it's a datetime object
            if isinstance(dt, datetime):
                # Make naive if timezone aware
                if dt.tzinfo is not None:
                    dt = dt.replace(tzinfo=None)
                return dt
            # If it's just a date, convert to datetime
            return datetime.combine(dt, datetime.min.time())
    return datetime.min  # Default value if no date found

def split_ics_file(input_file, max_size_mb=1):
    """
    Split an ICS file into multiple files of specified maximum size
    Events are sorted by date before splitting
    """
    # Convert MB to bytes (use slightly smaller target to ensure we don't exceed limit)
    max_size = int(max_size_mb * 1024 * 1024 * 0.95)  # 95% of max size as safety margin

    # Read the input file
    with open(input_file, 'rb') as f:
        cal = Calendar.from_ical(f.read())

    # Get all events and sort them by date
    events = [comp for comp in cal.walk() if comp.name == 'VEVENT']
    if not events:
        print("No events found in the calendar file.")
        return

    # Sort events by date
    events.sort(key=get_event_date)

    # Pre-calculate calendar properties
    cal_properties = {}
    for attr in ['VERSION', 'PRODID', 'CALSCALE', 'METHOD']:
        if attr in cal:
            cal_properties[attr] = cal[attr]

    def create_calendar_with_events(event_list):
        """Helper function to create a calendar with given events"""
        new_cal = Calendar()
        for attr, value in cal_properties.items():
            new_cal.add(attr, value)
        for e in event_list:
            new_cal.add_component(e)
        return new_cal

    # Initialize variables
    current_events = []
    file_counter = 1
    base_name = os.path.splitext(input_file)[0]

    # Process events in batches
    for event in events:
        current_events.append(event)
        
        # Create test calendar and check size
        test_cal = create_calendar_with_events(current_events)
        current_size = len(test_cal.to_ical())
        
        if current_size >= max_size or event == events[-1]:
            # If we exceeded size, remove the last event
            if current_size >= max_size and len(current_events) > 1:
                current_events.pop()
                test_cal = create_calendar_with_events(current_events)
            
            # Write current batch to file
            output_file = f"{base_name}_part{file_counter}.ics"
            with open(output_file, 'wb') as f:
                f.write(test_cal.to_ical())
            
            actual_size_mb = os.path.getsize(output_file) / (1024 * 1024)
            print(f"Created {output_file} with {len(current_events)} events ({actual_size_mb:.2f} MB)")
            
            # Start new batch
            if current_size >= max_size and len(current_events) > 1:
                current_events = [event]
            else:
                current_events = []
            
            file_counter += 1

    # Handle any remaining events
    if current_events:
        output_file = f"{base_name}_part{file_counter}.ics"
        final_cal = create_calendar_with_events(current_events)
        
        with open(output_file, 'wb') as f:
            f.write(final_cal.to_ical())
        
        actual_size_mb = os.path.getsize(output_file) / (1024 * 1024)
        print(f"Created {output_file} with {len(current_events)} events ({actual_size_mb:.2f} MB)")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Split an ICS file into multiple smaller files')
    parser.add_argument('input_file', help='Input ICS file to split')
    parser.add_argument('--max-size', type=float, default=1.0,
                      help='Maximum size of each split file in MB (default: 1.0)')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.input_file):
        print(f"Error: Input file '{args.input_file}' does not exist.")
        return
    
    try:
        split_ics_file(args.input_file, args.max_size)
        print("Split operation completed successfully.")
    except Exception as e:
        print(f"Error occurred while splitting the file: {str(e)}")

if __name__ == "__main__":
    main()
