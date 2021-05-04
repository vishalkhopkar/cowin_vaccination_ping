import playsound
import requests
import datetime
import json
import time

def process_output(json_output, region, dist_id):
    #output = json.loads(json_output)
    no_of_centres = 0
    output = json_output
    centres = output["centers"]
    for centre in centres:
        sessions = centre["sessions"]
        for session in sessions:
            min_age = session["min_age_limit"]
            avbl_cap = session["available_capacity"]
            if min_age == 18 and avbl_cap > 0:
                print("SLOTS AVAILABLE AT "+centre["name"])
                no_of_centres+=1

    if no_of_centres == 0:
        print("Sorry no centre available in at "+region+" dist_id " +str(dist_id)+" as on "+datetime.datetime.now().strftime("%d-%m-%y %H:%M:%S"))
    else:
        playsound.playsound("alarm.mp3")

districtCodes = [
    [294, 265],
    [395, 392, 393, 394],
    [363],
    [141, 145, 140, 146, 147, 143, 148, 149, 144, 150, 142, 199, 188, 207, 202, 650, 651],
    [581],
    [571, 565, 557]
]
region_arr = ["Bangalore", "Mumbai (MMR)", "Pune", "Delhi (NCR)", "Hyderabad", "Chennai"]
disp_str = "Enter city."
for i in range(0, len(region_arr)):
    disp_str += "\n"+str(i+1)+": "+region_arr[i]
reg_id = input(disp_str+"\n")
try:
    reg_id = int(reg_id)
    if reg_id < 1 or reg_id > 6:
        raise Exception("Invalid")
except:
    print("Invalid input exiting...")
    exit()
region = region_arr[reg_id - 1]
print("Your region is "+region)
dist_ids = districtCodes[reg_id - 1]
while 1:
    current_date = datetime.datetime.now()
    current_yr = current_date.year
    current_month = current_date.month
    current_day = current_date.day
    str_current_year = str(current_yr)
    str_current_month = str(current_month)
    str_current_day = str(current_day)
    if len(str_current_day) == 1:
        str_current_day = '0'+str_current_day
    if len(str_current_month) == 1:
        str_current_month = '0'+str_current_month

    total_date = str_current_day+"-"+str_current_month+"-"+str_current_year
    for dist_id in dist_ids:

        response = requests.get("https://cdn-api.co-vin.in/api/v2/appointment/sessions/calendarByDistrict?district_id="+str(dist_id)+"&date="+total_date)
        if response.status_code == 200:
            process_output(response.json(), region, dist_id)
        else:
            print("API call failed")

    time.sleep(60)
