  bytesize=serial.EIGHTBITS,
  timeout=1
  )

# Variables
json_dictionary = {}
count=0

def parse(line):
  items ={} 
  attribute ={} 
  if ":" in line:
    line_list = line.split(":")
    print line_list
    if len(line_list) == 2 and line_list[0].isalpha():
      json_dictionary[line_list[0]] = line_list[1]
    elif line_list[0].isalpha():
      first_attribute = line_list[0]
      second_attribute = line_list[1].split()[-1]
      attribute[first_attribute] = line_list[1].rsplit(' ', 1)[0].strip()
      attribute[second_attribute] = line_list[2].strip()
      json_dictiionary['attributes'].append(attribute)
  if len(re.findall("\d+.\d+", line)) > 0:
    price = line.split()[-1]
    item = line.split()[:-1]
    items[item] = price
    json_dictionary['items'].append(items)
  print json_dictionary

while 1:
  line = ser.readline()
  while len(line) > 0:
    raw_line =repr(line).replace("\\", "")
    parse(line)
    if "x1bix1bv" in raw_line:
      print ("****** CUT PAPER *******")
    line = ser.readline()