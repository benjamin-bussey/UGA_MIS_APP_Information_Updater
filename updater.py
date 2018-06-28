from bs4 import BeautifulSoup
import requests
import json

#Storing the html in the MIS homepage as page
page = requests.get('http://www.terry.uga.edu/directory/dept/11/').content

#Loading the page as a BeautifulSoup object for further parsing
soup = BeautifulSoup(page, 'lxml')

#Getting a list of all faculty entries
faculty = soup.find('div', {'class': 'directory-list'}).find_all('article')

#Creating a list to store faculty data
data = []

#Looping through each faculty member and extracting their name, title, office, and email
for entry in faculty:
    #Navigating towards the relevant section of the
    information = entry.find('div', {'class': 'media-body'})

    #Name section
    name = ''
    nameParts = information.find('a', {'class': 'fn'}).find_all('span')
    for namePart in nameParts:
        name += namePart.text + ' '

    #Trimming whitespace and formatting string
    name = str.rstrip(name)
    name = name.replace('  ', ' ')
    print(name)

    #Title section
    title = information.find('ul', {'class': 'title'}).text

    #Trimming leading whitespace and formatting string
    title = str.lstrip(title)
    title = title.strip('\n')
    print(title)

    #Office section
    office = ''
    try:
        office = information.find('div', {'class': 'extended-address'}).text

    except AttributeError:
        office = 'None'

    #trimming whitespaces in office
    office = office.lstrip().rstrip()
    print(office)

    #Email Section
    try:
        email = information.find('a', {'class': 'email'}).text
    except AttributeError:
        email = 'None'
    email = email.strip('\n')
    print(email)

    #Adding each entry (type dictionary) into the data list
    data.append(dict([('name', name), ('title', title), ('office', office), ('email', email)]))

    #Printing visual divider
    print('-------------------------------------------------------------')

#Writing json to file
with open('faculty_information.txt', 'w') as outfile:
    json.dump(data, outfile)