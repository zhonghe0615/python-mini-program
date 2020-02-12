#!/usr/bin/env python

# Make sure to install requests before running:
# > pip install requests
# Documentation for the requests library can be found here: http://docs.python-requests.org/en/master/
import requests
import json
from datetime import datetime
import pytz

#Class as container of food truck's Name / Address
class truck_row:
    def __init__(self, name, addr):
            self.name = name
            self.addr = addr

def convert24(time):
    arr = time.split(":")
    hour_time = arr[0]
    minute_time = arr[1]
    return hour_time + minute_time

def sortAndprintCurrentPage(rows):
    if(len(rows) == 0) : 
        return
    #Sort the list by name alphabetically
    rows.sort(key=lambda x: x.name)
    for row in rows:
        print(str(row.name) + "  <" + str(row.addr) + "> ")

def main():
    startQuiry = input("^ - ^ Hi there, would like to know any food trucks open now? (Y/N)")
    
    if(startQuiry != 'Y' and startQuiry != 'y'):
        print("Your look up FINISHES, Thank You for using me!")
        return
    
    url = "http://data.sfgov.org/resource/bbb8-hzi6.json"
    week_days = [ 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    response = requests.get(url)
    if response.status_code == 200:
        truck_objects = response.json()
        weekday_idx = datetime.today().weekday()
        hour_time = datetime.now().hour
        minute_time = datetime.now().minute
        weekday = week_days[weekday_idx]
        time_str = str(hour_time) + str(minute_time) # current time hour plus minute
        truck_set = {''} # Use this set to dedup food trucks by names;
        cnt = 0 # For current page, the number of distinct food trucks obtained;
        totalCnt = 0 # So far, the total number of distinct food trucks obtained;
        truck_rows = [] # For current page, the names and addresses saved in this list.

        for truck_object in truck_objects:
            #Convert input time range to 24hr time for easier comparison;
            start_24 = convert24(truck_object['start24'])
            end_24 = convert24(truck_object['end24'])
            if truck_object['dayofweekstr'] == weekday and time_str >= start_24 and time_str <= end_24:
                # Every time current page is full with size 10, we are asking if user want to display more, 
                # in the mean time, sort and print out trucks of current page
                if cnt == 10 :
                    sortAndprintCurrentPage(truck_rows)
                    print("On current page, the number of trucks loaded : " + str(cnt))
                    print("The total number of trucks loaded for you : " + str(totalCnt))   
                    truck_rows = []

                    loadMore = input("Would like to load more trucks? (Y/N)")
                    if loadMore != 'Y' and loadMore != 'y': 
                        break
                    else:
                        print("Loading new page......................................................................")
                        cnt = 0
                truck_name = truck_object['applicant']
                if truck_name in truck_set:
                    continue
                truck_addr = truck_object['location']
                truck_set.add(truck_name)
                truck_rows.append(truck_row(truck_name, truck_addr))
                cnt += 1
                totalCnt += 1

        #Post-process, in case there some remain users want to print out, which was not printed yet in above for loop;      
        sortAndprintCurrentPage(truck_rows)        
        print("Your look up FINISHES, thank you for using me!")
    
    else:
        print("Could not fetch data from SF Gov Website for some reasons ! ")


if __name__ == "__main__":
    main()