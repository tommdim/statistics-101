import csv


def calctime(start,curr):
    c = [int(x) for x in curr.split(":")]
    s = [int(x) for x in start.split(":")]
    return ((c[0] - s[0]) * 60 + (c[1] - s[1])) * 60 + (c[2] - s[2])

with open('heartbeats/rocco3.txt') as f:
    lines = f.readlines()
    hr = []
    time = []
    for s in lines:
        if "<Value>" in s:
            hr.append(s.strip()[s.strip().find(">") + 1:s.strip().rfind("<")])
        if "<Time>" in s:
            s = s.strip()[3:]
            if not time:
                start = s.strip()[s.strip().find("T") + 1:s.strip().rfind(".")]
                
            time.append(calctime(start, s.strip()[s.strip().find("T") + 1:s.strip().rfind(".")]))
    hr = hr[2:]
    
    
with open('rocco3.csv', 'w', encoding='UTF8', newline='') as c:
    #Header
    writer = csv.writer(c)
    writer.writerow(["HR", "Delta", "Time"])

    start = hr[0]
    for i in range(len(time)):
        writer.writerow([hr[i], int(hr[i]) - int(start), time[i]])


    
    
