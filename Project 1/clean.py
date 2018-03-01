import sys

if len(sys.argv) < 2:
    print("Enter filename as command line argument")
    exit()

filePath = sys.argv[1]
course_catalog = {}
temp = {}
with open(filePath) as fp:
    line = fp.readline()
    while line:
        prof = line.split('-')[0]
        prof = prof.strip()
        if "," in prof:
            last_name = prof.split(",")[0]
        elif "." in prof:
            if " " in prof:
                length = len(prof.split())-1
                last_name = prof.split()[length]
            else:
                last_name = prof.split('.')[1]
        else:
            if len(prof.split()) == 2:
                last_name = prof.split()[1]
            elif len(prof.split()) == 1:
                last_name = prof.split()[0]
            elif len(prof.split()) > 2:
                length = len(prof.split())
                last_name = prof.split()[length-1]
        courses = ("".join(line.split('-')[1:])).split("|")
        last_name = last_name.strip()
        last_name = last_name.capitalize()
        for c in courses:
            c = c.strip()
            c = c.capitalize()
            if last_name in temp:
                temp[last_name].append(c)
            else:
                temp[last_name] = [c]
        line = fp.readline()

for key, value in temp.items():
    value.sort()
    course_catalog[key] = value

f = open('cleaned.txt','w')
with f:
    for key, value in sorted(course_catalog.items()):
        s = key + " - "
        for e in value:
            s = s + str(e) + " | "
        s = s[:-3]
        f.write(s + "\n")
    f.close()
