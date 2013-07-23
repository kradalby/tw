# -*- coding: utf-8 -*-


# Consultant format:
# {9001 : ('Kristine', 'Breiland Dalby', ....)}


IN_FILE = "TEST58"
VCARD_DIR = "vcard"

def parse_consultants(twfile):
    file = open(twfile,'rb').read()
    file = file.replace('\",\"',';').replace('\",','').replace(',\"', ';').replace(',',';').replace('\"',';')
    file = file.split('\n')
    list = []

    for i in file:
        list.append(i.split(';'))

    del list[-1]
    del list[-1]
    
    for j in list:
        for i in range(len(j)):
            j[i] = fix_whitespace(j[i])
            j[i] = clean_names(j[i])
        
        # Ugly, need to change when we have a more stable input list
        j[5] = j[5].lower()
        if 'club' in j[1].lower() or 'startbag' in j[1].lower():
            del list[list.index(j)]

    dict = {}
    for i in list:
        dict[i[0]] = (i[1],i[2],i[3],i[4],i[5],i[7],i[8])

    return dict


def clean_names(string):
    string = str(string)
    if not string.isdigit() and string != '':
        string = string.lower()
        if ' ' in string:
            lstring = string.split(' ')
            string = ""
            for i in lstring:
                if i != '':
                    string += i[0].upper() + i[1:] + ' '
        else:
            print string
            string = string[0].upper() + string[1:]
        return string
    else:
        return string

def fix_whitespace(string):
    string = str(string)
    list = []
    for i in range(len(string)):
        if i == 0:
            if string[i] != " ":
                list.append(string[i])
        elif i >= 1  and i <= (len(string)-2):
            if string[i-1] != " " or string[i+1] != " ":
                list.append(string[i])
        elif i == (len(string)-1):
            if string[i] != " ":
                list.append(string[i])
    try: 
        if list[0] == " ":
            del list[0]
        if list[-1] == " ":
            del list[-1]
    except IndexError:
        pass

    string = ""
    for i in list:
        string += i
    return string

def get_active_consultants(dic):
    active = {}
    for key, value in dic.iteritems():
        if len(key) == 4:
            active[key] = value
    #del active[-1]
    return active

def generate_vcard(**kwargs):
    #
    #Fields: firstname, lastname, org, title, phone, mobile, address, email.
    #

    vcard = ['BEGIN:VCARD','VERSION:3.0']
    
    if 'firstname' in kwargs:
        vcard.append('N:%s;%s' % (kwargs.get('lastname'), kwargs.get('firstname')))
        vcard.append('FN:%s %s' % (kwargs.get('firstname'), kwargs.get('lastname')))
    if 'org' in kwargs:
        vcard.append('ORG:%s' % kwargs.get('org'))
    if 'title' in kwargs:
        vcard.append('TITLE:%s' % kwargs.get('title'))
    if 'phone' in kwargs:
        vcard.append('TEL;type=HOME;type=VOICE:%s' % kwargs.get('phone'))
    if 'mobile' in kwargs:
        vcard.append('TEL;type=CELL;type=VOICE:%s' % kwargs.get('mobile'))
    if 'address' in kwargs:
        vcard.append('ADR;TYPE=HOME:%s' % kwargs.get('address'))
    if 'email' in kwargs:
        vcard.append('EMAIL;TYPE=PREF,INTERNET:%s' % kwargs.get('email'))
    vcard.append('END:VCARD')

    card = ""
    for i in vcard:
        card += i + "\n"
    print card    
    return card


def sort_teams(dic):
    teams = {}
    for key, value in dic.iteritems():
        team = key[:2]
        if team not in teams:
            teams[team] = {}
            teams[team][key] = value
        else:
            teams[team][key] = value
    return teams

def save_vcards(dic):
    for key, value in dic.iteritems():
        f = open('vcard/%s_%s_%s.vcf' % (key, value[0], value[1]), 'wb')
        vcard = generate_vcard(firstname=cons[1], lastname=cons[2], 
                               title="TW konsulent " + cons[0], phone=cons[3],
                               address=cons[6] + ";" + cons[7] + ";" + cons[8], email=cons[5]) 
        f.write(vcard)
        


def main():
    
    active_consultants = get_active_consultants(parse_consultants(IN_FILE))
    sorted_consultants = sort_teams(active_consultants)
    save_vcards(active_consultants)
    


main()









