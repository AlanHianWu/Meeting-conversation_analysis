import re
import csv

file = 'Recording.vtt'
opened_file = open(file,encoding='utf8')
content = opened_file.read()
segments = content.split('\n\n') # split on double line

# wrangle segments
m = re.compile(r"\<.*?\>") # strip/remove unwanted tags
o = re.compile(r"\.+\d+") # strip/remove miliseconds

def clean(content):
    new_content = m.sub('',content)
    new_content = o.sub('',new_content)
    new_content = new_content.replace('align:start position:0%','')
    new_content = new_content.replace('-->','')
    return new_content

new_segments = [clean(s) for s in segments if len(s)!=0][2:]

# trim time codes for g suite plain text formatting conversion to seconds w/ formula '=value(str*24*3600)'
def clean_time(time):
    time = time.split(':')
    if time[0]=='00':
        return time[1]+':'+time[2]
    if not time[0]=='00':
        return time[0]+':'+time[1]+':'+time[2]

trimmed_segments = []
for segment in new_segments:
    split_segment = segment.split()
    time_code = split_segment[0]
    text = ' '.join(segment.split()[2:])
    trimmed_segment = (time_code, text)
    trimmed_segments.append(trimmed_segment)

# write output as csv file
with open(str(file)[:-3]+'csv', 'w', encoding='utf8', newline='') as f:
    for line in trimmed_segments:
        thewriter = csv.writer(f)
        thewriter.writerow(line)