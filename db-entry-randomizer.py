#created by Tim Laeufer

import random
from datetime import timedelta, datetime, date


#format templates
insert_profile = "INSERT INTO profil (profilnummer) "
insert_profile +="VALUES ({pr_id});"

insert_beitrag = "INSERT INTO beitrag (beitragsnummer, autor_profilnummer) "
insert_beitrag +="VALUES ({beitr_id}, {pr_id});"

insert_gefaellt = "INSERT INTO gefaellt (profilnummer, beitragsnummer, zeit) "
insert_gefaellt +='VALUES ({pr_id}, {beitr_id}, "{time}");'

#dictionary: keys as integers are profile_ids
dic = {}

#to keep track of the beitrag_ids
beitrag_ids = []

#general start date set for easy management
start_date = datetime(year = 2020, month = 10, day = 1, hour = 0, second = 0)
end_date = datetime(year = 2020, month = 10, day = 14, hour = 14, second = 0)

#from: https://stackoverflow.com/questions/553303/generate-a-random-date-between-two-other-dates
def random_date(start, end):
    """
    This function will return a random datetime between two datetime
    objects.
    """
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    return start + timedelta(seconds=random_second)
#end

"""
every function returns full sentence arrays and describes a type of user
and how they act
"""
def obsess(prof_id, target_id):
    #likes a lot of posts of one person

    gefaellt_strings = []
    s = ""
    for i in dic[target_id]: #iterate over every post the target made
        randtime = random_date(start_date, end_date)#get a random time

        #get new times while randtime is out of boundaries
        while(randtime.hour < 7 or randtime.hour > 23):
            randtime = random_date(start_date, end_date)

        #insert data into a gefaellt_string
        s = insert_gefaellt.format(
            beitr_id = i,
            pr_id = prof_id,
            time = str(randtime)
        )
        gefaellt_strings.append(s) #append gefaellt_string into list
    return gefaellt_strings

def twelvie(prof_id, target_id):
    #always likes a targets post on 12:00, bot
    gefaellt_strings = []

    #determine how many days ago the first post of the target has to be liked
    time = end_date.replace(hour = 12)#time for last post like
    delta = timedelta(days=1)
    time = time -(len(dic[target_id])* delta)#go back x days to start date
    s = ""
    for i in dic[target_id]: #iterate over every post of the target
        s = insert_gefaellt.format(
            beitr_id = i,
            pr_id = prof_id,
            time = time
        )
        time = time + delta #go one day forward
        gefaellt_strings.append(s) #append gefaellt_string into list
    return gefaellt_strings

def likesall(prof_id):
    #likes every post
    gefaellt_strings = []
    s = ""

    for key in dic.keys(): #for every profil in the dictionary
        for i in dic[key]:  #for every beitrag of the profil
            randtime = random_date(start_date, end_date) #determine random time
            while(randtime.hour < 9 or randtime.hour >= 19):#keep time in bound
                randtime = random_date(start_date, end_date)
            s = insert_gefaellt.format(
                beitr_id = i,
                pr_id = prof_id,
                time = str(randtime)
            )
            gefaellt_strings.append(s) #append gefaellt_string into list
    return gefaellt_strings

def nolikes(prof_id):
    #likes no post
    pass

def onlyown(prof_id):
    #only likes his own posts
    gefaellt_strings = []
    s = ""
    for i in dic[prof_id]:#iterate over every own post
        randtime = random_date(start_date, end_date) #get random time
        while(randtime.hour < 9 or randtime.hour >= 19): #keep time in bound
            randtime = random_date(start_date, end_date)
        s = insert_gefaellt.format(
            beitr_id = i,
            pr_id = prof_id,
            time = str(randtime)
        )
        gefaellt_strings.append(s) #append gefaellt_string into list
    return gefaellt_strings

def lunchbreak(prof_id):
    #always likes between 12:00 and 13:00 on a workday
    gefaellt_strings = []
    s = ""

    #count all beitragsnummer in dictionary
    length = 0
    items = []#list of all beitragsnummer
    for key in dic.keys():
        length += len(dic[key])
        items += dic[key]
    amount = 5 * int(length/7) #calculate an amount to like

    for i in random.sample(items, amount):#iterate over a sample out of items
        randtime = random_date(start_date, end_date) #get a random time

        #keep time in bounds and date in weekdays
        while((randtime.hour < 12 or randtime.hour > 12) and
        (randtime.weekday not in [0, 1, 2, 3, 4])):
            randtime = random_date(start_date, end_date)
        s = insert_gefaellt.format(
            beitr_id = i,
            pr_id = prof_id,
            time = str(randtime)
        )
        gefaellt_strings.append(s)#append gefaellt_string into list
    return gefaellt_strings

def commuter(prof_id):
    #always likes between 07:30-8:30 and 17:30-18:30 on weekdays
    gefaellt_strings = []
    s = ""

    #count all beitragsnummer in dictionary
    length = 0
    items = []#list of all beitragsnummer
    for key in dic.keys():
        length += len(dic[key])
        items += dic[key]
    amount = 4 * int(length/7) #calculate an amount to like

    for i in random.sample(items, amount):#iterate over a sample out of items

        #keep time in bounds and date in weekdays
        randtime = random_date(start_date, end_date)
        while((randtime.hour < 7 or randtime.hour > 8) and
            (randtime.hour < 17 or randtime.hour > 18) and
            (randtime.weekday not in [0, 1, 2, 3, 4])):
            randtime = random_date(start_date, end_date)
        s = insert_gefaellt.format(
            beitr_id = i,
            pr_id = prof_id,
            time = str(randtime)
        )
        gefaellt_strings.append(s)#append gefaellt_string into list
    return gefaellt_strings

def firstfive(prof_id):
    #always likes within the first 5 min of an hour
    gefaellt_strings = []
    s = ""

    #count all beitragsnummer in dictionary
    length = 0
    items = []#list of all beitragsnummer
    for key in dic.keys():
        length += len(dic[key])
        items += dic[key]
    amount = 4 * int(length/7)#calculate an amount to like

    #keep time in bounds and date in weekdays
    for i in random.sample(items, amount):
        randtime = random_date(start_date, end_date)
        while((randtime.hour < 13 or randtime.hour > 19) and
        (randtime.weekday not in [0, 1, 2, 3, 4])):
            randtime = random_date(start_date, end_date)

        randtime = randtime.replace(minute = random.randrange(0, 5))
        s = insert_gefaellt.format(
            beitr_id = i,
            pr_id = prof_id,
            time = str(randtime)
        )
        gefaellt_strings.append(s)#append gefaellt_string into list
    return gefaellt_strings

def sweethome(prof_id):
    #always likes between 19:00-23:00 on weekdays, every 5 min of the hr
    gefaellt_strings = []
    s = ""

    #count all beitragsnummer in dictionary
    length = 0
    items = []#list of all beitragsnummer
    for key in dic.keys():
        length += len(dic[key])
        items += dic[key]
    amount = 3 * int(length/7)#calculate an amount to like
    for i in random.sample(items, amount):#iterate over a sample out of items
        randtime = random_date(start_date, end_date)

        #keep time in bounds and date in weekdays
        while((randtime.hour < 19) and
        (randtime.weekday not in [0, 1, 2, 3, 4])):
            randtime = random_date(start_date, end_date)

        #replace minute with a value 0 <= x <= 5
        randtime = randtime.replace(minute = random.randrange(0, 5))
        s = insert_gefaellt.format(
            beitr_id = i,
            pr_id = prof_id,
            time = str(randtime)
        )
        gefaellt_strings.append(s)#append gefaellt_string into list
    return gefaellt_strings

def rapidlike(prof_id, target_ids):
    #likes two users post in rapid succession:
    #a: on monday 15:02-15:08
    #b: on tuesday 03:02-03:08
    #a bot
    gefaellt_strings = []

    onesecond = timedelta(seconds = 1)#one second timedelta
    for j in target_ids: #iterate over both target_ids
        randtime = random_date(start_date, end_date)#get random time
        for i in dic[j]:#iterate over all beitragsnummer by the target j
            s = insert_gefaellt.format(
                beitr_id = i,
                pr_id = prof_id,
                time = str(randtime)
            )
            randtime += onesecond # get one second ahead of the previous like
            gefaellt_strings.append(s) #append gefaellt_string into list
    return gefaellt_strings

def post(profile_id, min, max):
    #posts posts and returns SQL strings
    strings = []
    #get random amount between the min and max amount of posts
    for i in range(random.randrange(min, max)):

        #generate beitrag_id
        beitrag_id = random.randrange(1000, 5000)
        while(beitrag_id in beitrag_ids): #keep id in bounds
            beitrag_id = random.randrange(1000, 5000)

        beitrag_ids.append(beitrag_id)#append id to list of ids
        if(profile_id not in dic.keys()):
            dic[profile_id] = []#if the profile is not in the dic, add it

        dic[profile_id].append(beitrag_id)
        strings.append(insert_beitrag.format(
            beitr_id = beitrag_id,
            pr_id = profile_id
        ))
    return strings


#creates the sql
def randomize(prof_ids, insert_profile_strings):
    beitrag_sum = [] #amount of all beitraege
    gefaellt_sum = [] #amount of gefaellt entries

    for j in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']:#group names

        names_list = []
        for el in dic.keys():
            dic[el] = []
        insert_beitrag_strings = []
        insert_gefaellt_strings= []

        #generate posts
        names_list.append(("obsess", prof_ids[0]))
        insert_beitrag_strings += post(prof_ids[0], 5, 15)
        names_list.append(("twelvie", prof_ids[1]))
        insert_beitrag_strings += post(prof_ids[1], 1, 3)
        names_list.append(("likesall", prof_ids[2]))
        insert_beitrag_strings += post(prof_ids[2], 5, 15)
        names_list.append(("nolikes", prof_ids[3]))
        insert_beitrag_strings += post(prof_ids[3], 20, 45)
        names_list.append(("onlyown", prof_ids[4]))
        insert_beitrag_strings += post(prof_ids[4], 10, 30)
        names_list.append(("lunchbreak", prof_ids[5]))
        insert_beitrag_strings += post(prof_ids[5], 4, 8)
        names_list.append(("commuter", prof_ids[6]))
        insert_beitrag_strings += post(prof_ids[6], 9, 15)
        names_list.append(("firstfive", prof_ids[7]))
        insert_beitrag_strings += post(prof_ids[7], 10, 25)
        names_list.append(("sweethome", prof_ids[8]))
        insert_beitrag_strings += post(prof_ids[8], 6, 12)
        names_list.append(("rapidlike", prof_ids[9]))
        insert_beitrag_strings += post(prof_ids[9], 1, 3)

        #generate gefaellt_strings:    
        insert_gefaellt_strings += obsess(prof_ids[0], prof_ids[3])
        insert_gefaellt_strings += twelvie(prof_ids[1], prof_ids[3])
        insert_gefaellt_strings += likesall(prof_ids[2])
        insert_gefaellt_strings += onlyown(prof_ids[4])
        insert_gefaellt_strings += lunchbreak(prof_ids[5])
        insert_gefaellt_strings += commuter(prof_ids[6])
        insert_gefaellt_strings += firstfive(prof_ids[7])
        insert_gefaellt_strings += sweethome(prof_ids[8])
        targets = [prof_ids[7], prof_ids[3]]
        insert_gefaellt_strings += rapidlike(prof_ids[9], targets)

        print("beitraege: " + str(len(insert_beitrag_strings)))
        print(len(insert_profile_strings))
        print(len(insert_beitrag_strings))
        print(len(insert_gefaellt_strings))
        #write individual files:
        #absolute for making sure it works
        with open("C:/Users/timla/OneDrive/WHA/arbeit/anlagen/datenbanken/python-randomizer/aufgaben/gruppe_" + j + ".sql", "w+") as f:
            f.write("DELETE FROM profil; \n")
            f.write("DELETE FROM beitrag; \n")
            f.write("DELETE FROM gefaellt; \n")
            for el in insert_profile_strings:
                f.write(el + '\n')
            for el in insert_beitrag_strings:
                f.write(el + '\n')
            for el in insert_gefaellt_strings:
                f.write(el + '\n')
        print("Wrote C:/Users/timla/OneDrive/WHA/arbeit/anlagen/datenbanken/python-randomizer/aufgaben/gruppe_" + j + ".sql !")
        beitrag_sum += insert_beitrag_strings
        gefaellt_sum += insert_gefaellt_strings

    #write a complete file that incorporates everything generated
    #absolute for making sure it works
    with open("C:/Users/timla/OneDrive/WHA/arbeit/anlagen/datenbanken/python-randomizer/aufgaben/complete.sql", "w+") as f:
        for el in names_list:
            f.write("--" + str(el) + '\n')
        f.write("DELETE FROM profil; \n")
        f.write("DELETE FROM beitrag; \n")
        f.write("DELETE FROM gefaellt; \n")
        for el in insert_profile_strings:
            f.write(el + '\n')
        for el in beitrag_sum:
            f.write(el + '\n')
        for el in gefaellt_sum:
            f.write(el + '\n')
    print("Wrote C:/Users/timla/OneDrive/WHA/arbeit/anlagen/datenbanken/python-randomizer/aufgaben/complete.sql !")
    return names_list

prof_ids = []
insert_profile_strings = []

#create 10 profile_ids
for i in range(10):
    prof_id = random.randrange(1, 200)

    while(prof_id in prof_ids):
        prof_id = random.randrange(1, 200)

    prof_ids.append(prof_id)
    s = insert_profile.format(
        pr_id = prof_id
    )
    insert_profile_strings.append(s)
#start the randomization with the given profile ids and insert strings
print(randomize(prof_ids, insert_profile_strings))