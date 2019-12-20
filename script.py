import ast
import csv

def strToDict(data):
  if (len(data) == 0):
    return {}
  output = data.replace("'","`").replace(",","").replace("||",",").replace("|",",").replace("::",":").replace(":",":'").replace(",","',")
  output = "{" + output + "'}"
  return ast.literal_eval(output)

incidents = open("data/incidents.csv","w+",encoding="UTF-8")
city_or_county = open("data/city_or_county.csv","w+")
state_senate = open("data/state_senate.csv","w+")
state = open("data/state.csv","w+")
incident_characteristics = open("data/incident_characteristics.csv","w+")
characteristics = open("data/characteristics.csv","w+")
state_house = open("data/state_house.csv","w+")
state_congressional_ditrict = open("data/state_congressional_ditrict.csv","w+")
incident_participant = open("data/incident_participant.csv","w+")
incident_gun = open("data/incident_gun.csv","w+")
#cityorcounty dependencies
city_list = []
state_list = []
senate_list = []
house_list = []
district_list = []
#incident characteristics dependencies
characteristics_list = []
inc_characteristics = []
#other
incident_gun_list = []
participant_list = []

rownum = 1
numberofLine = 268725
currPerc = 1
print("Reading file...")
with open('./data.1.csv',encoding="UTF-8") as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:

      ###### All about location datas 
      #state list
      if(row[2] not in state_list):
        state_list.append(row[2])
      #senate list
      if( ([ state_list.index(row[2]) + 1 , row[28] ] not in senate_list ) and len(row[28]) != 0 ):
        senate_list.append([ state_list.index(row[2]) + 1 , row[28] ])
      #house list
      if(( [ state_list.index(row[2]) + 1 , row[27] ] not in house_list ) and len(row[27]) != 0 ):
        house_list.append([ state_list.index(row[2]) + 1 , row[27] ])
      #congressional district
      if(( [ state_list.index(row[2]) + 1 , row[10] ] not in district_list ) and len(row[10]) != 0 ):
        district_list.append([ state_list.index(row[2]) + 1 , row[10] ])
      #city list
      if( [row[3], state_list.index(row[2]) + 1  ] not in city_list ):
        city_list.append([row[3], state_list.index(row[2]) + 1  ])

      incidentWrite = str(row[0]).strip()+"<"+str(row[1]).strip()+"<"+str(row[5]).strip()+"<"+str(row[6]).strip()+"<"+str(city_list.index([row[3], state_list.index(row[2])+1]) + 1).strip()+"<"+str(row[4]).strip()+"<"+str(row[8]).strip()+"<"+( str(row[14]).strip() if  (str(row[14])) !=  '' else  "0") +"<"+str(row[15]).strip()+"<"+(str(row[16]).strip() if (str(row[16])) != '' else "0")+"<"+str(row[18]).strip()+"<"+str(row[26]).strip()+"\n"

      incidents.write(incidentWrite)


      ##### All About incident characteristics
      for schar in row[13].split("||"):
        if ( schar not in characteristics_list ):
          characteristics_list.append(schar)
        inc_characteristics.append( [ row[0] , characteristics_list.index(schar) + 1 ] )

      ##### All about incident gun
      if (len(row[11]) != 0):
        for i in range(int(row[17])):
          incident_gun_single = []
          incident_gun_single.append(row[0])
          if(strToDict(row[11])[i] == "Unknown"):
            incident_gun_single.append("NULL")
          elif(strToDict(row[11])[i] == "Stolen"):
            incident_gun_single.append("1")
          elif(strToDict(row[11])[i] == "Not-Stolen" or strToDict(row[11])[i] == "Not-stolen"):
            incident_gun_single.append("0")
          incident_gun_single.append(strToDict(row[12])[i])
          incident_gun_list.append(incident_gun_single)

      ##### All about incident participant
      tmp_age_group = strToDict(row[20])
      tmp_gender = strToDict(row[21])
      tmp_name = strToDict(row[22])
      tmp_relationship = strToDict(row[23])
      tmp_status = strToDict(row[24])
      tmp_type = strToDict(row[25])
      maxLength = max(len(tmp_age_group),len(tmp_gender),len(tmp_name),len(tmp_relationship))

      for i in range(maxLength):
        participant_single = []
        participant_single.append(row[0])

        if(i in tmp_age_group):
          if( tmp_age_group[i] == "Teen 12-17"):
            participant_single.append("12")
            participant_single.append("17")
          elif( tmp_age_group[i] == "Adult 18+"):
            participant_single.append("18")
            participant_single.append("999")
          elif( tmp_age_group[i] == "Child 0-11"):
            participant_single.append("0")
            participant_single.append("11")
        else:
          participant_single.append("NULL")
          participant_single.append("NULL")

        if(i in tmp_name):
          participant_single.append(tmp_name[i])
        else:
          participant_single.append("NULL")

        if(i in tmp_gender):
          if( tmp_gender[i] == "Male"):
            participant_single.append("1")
          elif( tmp_gender[i] == "Female"):
            participant_single.append("0")
        else:
            participant_single.append("NULL")


        if(i in tmp_status):
          participant_single.append(tmp_status[i])
        else:
          participant_single.append("NULL")

        if(i in tmp_type):
          participant_single.append(tmp_type[i])
        else:
          participant_single.append("NULL")

        if(i in tmp_relationship):
          participant_single.append(tmp_relationship[i])
        else:
          participant_single.append("NULL")

        participant_list.append(participant_single)
      if(currPerc < rownum*100//numberofLine):
        currPerc = rownum*100//numberofLine
        print(currPerc , "% Completed")
      rownum += 1
print("Creating output files")
print("Creating state_list")
for i in state_list:
  toWrite = str(state_list.index(i)+1)+","+str(i)+"\n"
  state.write(toWrite)

print("Creating city_list")

for i in city_list:
  toWrite = str(city_list.index(i)+1)+","+str(i[0])+","+str(i[1])+"\n"
  city_or_county.write(toWrite)

print("Creating senate_list")

for i in senate_list:
  toWrite = str(i[0])+","+str(i[1])+"\n"
  state_senate.write(toWrite)

print("Creating house_list")

for i in house_list:
  toWrite = str(i[0])+","+str(i[1])+"\n"
  state_house.write(toWrite)

print("Creating district_list")

for i in district_list:
  toWrite = str(i[0])+","+str(i[1])+","+str(district_list.index(i)+1)+"\n"
  state_congressional_ditrict.write(toWrite)

print("Creating characteristics list")

for i in characteristics_list:
  toWrite = str(characteristics_list.index(i) + 1)+","+str(i).replace(",",";")+"\n"
  characteristics.write(toWrite)

print("Creating characteristics")

for i in inc_characteristics:
  toWrite = str(i[0])+","+str(i[1])+"\n"
  incident_characteristics.write(toWrite)

print("Creating gun list")

for i in incident_gun_list:
  toWrite = str(i[0])+","+str(i[1]) if (str(row[11])) != '' else "NULL"+","+str(i[2])+","+str(incident_gun_list.index(i)+1)+"\n"
  incident_gun.write(toWrite)

print("Creating participantlist")

for i in participant_list:
  toWrite = str(i[0])+","+str(participant_list.index(i)+1)+","+str(i[1])+","+str(i[2])+","+str(i[3])+","+str(i[4])+","+str(i[5])+","+str(i[6])+","+str(i[7])+"\n"
  incident_participant.write(toWrite.encode("utf-8").decode("utf-8"))

print("Completed")

incidents.close()
city_or_county.close()
state_senate.close()
state.close()
incident_characteristics.close()
characteristics.close()
state_house.close()
state_congressional_ditrict.close()
incident_participant.close()
incident_gun.close()
#0 incident_id,1 date,2 state,3 city_or_county,4 address,5 n_killed,6 n_injured,7 incident_url,8 source_url,9 incident_url_fields_missing
#10 congressional_district,11 gun_stolen,12 gun_type,13 incident_characteristics,14 latitude,15 location_description,16 longitude
#17 n_guns_involved,18 notes,19 participant_age,20 participant_age_group,21 participant_gender,22 participant_name,23 participant_relationship
#24 participant_status,25 participant_type,26 sources,27 state_house_district,28 state_senate_district

