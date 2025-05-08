##
## Program: GetSpacePic.py
## Purpose: Read NASA's GateWay to Astronaut Photography of Earth
##          database for a particular ISS mission and frame
##          combination. First parameter is ISS Mission number,
##          a zero-filled 3-digit code. Second is frame number,
##          not zero-filled. Returns the focal length of the camera
##          used, along with the date and time the photo was taken.
## To Use: Open command prompt, set directory to location of this
##         file, call the file followed by the desired mission
##         and frame number
## Example: GetSpacePic.py 
## Programmer: Colin DeCoste
## Date: February 25, 2025
##

if __name__ == "__main__":

    # import time modules
    from time import gmtime, strftime, localtime
    import time

    # import other modules
    import sys
    import urllib.request
    import re
    import datetime

    strBeginTime = str(strftime("%a, %d %b %Y %X", localtime()))

    # arguments
    if len(sys.argv) > 1:
        strMission = sys.argv[1]
        strFrame = sys.argv[2]
        strFocalLength = "blank"
        strDate = "blank"
        strTime = "blank"
        strPhotoURL = "blank"

    else:   # defaults
        strMission = '001'
        strFrame = '5903'
        strFocalLength = "blank"
        strDate = "blank"
        strTime = "blank"
        strPhotoURL = "blank"
        print('No parameters entered. Default mission shown')

    try:
        # variable for the unique URL to this photo:
        strFindLatLongURL = "https://eol.jsc.nasa.gov/SearchPhotos/photo.pl?mission=ISS" + strMission + "&roll=E&frame=" + strFrame

        # open and read url:
        aResp = urllib.request.urlopen(strFindLatLongURL)
        # put characters into a variable:
        web_pg = str(aResp.read())

        # Search patterns
        focalPat = "Focal Length:" + "(.*?)" + "mm<"
        datePat = "Date taken" + "(.*?)" + " <"
        timePat = "Time taken" + "(.*?)" + " <"
        m = re.search(focalPat,web_pg)
        n = re.search(datePat, web_pg)
        o = re.search(timePat, web_pg)

        # if statements to find variables or error message
        if m:
            strFL = str(m.group(1))
            strFocalLength = strFL[(strFL.find("<td>")+4):len(strFL)] + "mm"
        else:
            print("Nothing found for Focal Length")
            strFocalLength = "blank"

        if n:
            strDT = str(n.group(1))
            strDate = strDT[(strDT.find('"table_pad">')+13):len(strDT)]
        else:
            print("Nothing found for Date")
            strDate = "blank"

        if o:
            strTM = str(o.group(1))
            strTime = strTM[(strTM.find('pad">')+6):len(strTM)]
        else:
            print("Nothing found for Time")
            strTime = "blank"

    except:
        print ("Exception!")
        
print (f"for {strMission} {strFrame}, the focal/date/time is: {strFocalLength} / {strDate} / {strTime}")
