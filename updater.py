from bs4 import BeautifulSoup
import requests
import json
import time

#Storing the html in the MIS homepage as page
page = requests.get('http://www.terry.uga.edu/directory/dept/11/').content

#Loading the page as a BeautifulSoup object for further parsing
soup = BeautifulSoup(page, 'lxml')

#Getting a list of all faculty entries
faculty = soup.find('div', {'class': 'directory-list'}).find_all('article')

#Creating a list to store faculty data
facultyData = []

#Looping through each faculty member and extracting their name, title, office, and email
for entry in faculty:
    #Navigating towards the relevant section of the
    information = entry.find('div', {'class': 'media-body'})

    #Name section
    nameParts = information.find('a', {'class': 'fn'}).find_all('span')
    for namePart in nameParts:
        name += namePart.text + ' '

    #Trimming whitespace and formatting string
    name = str.rstrip(name)
    name = name.replace('  ', ' ')
    print(name)

    #picture section

    #Title section
    title = information.find('ul', {'class': 'title'}).text

    #Trimming leading whitespace and formatting string
    title = str.lstrip(title)
    title = title.strip('\n')
    print(title)

    #Office section
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
    facultyData.append(dict([('name', name), ('picutre', picture), ('title', title), ('office', office), ('email', email)]))

    #Printing visual divider
    print('-------------------------------------------------------------')

#Writing json to file
with open('faculty_information.json', 'w') as outfile:
    json.dump(facultyData, outfile)


#Getting html of course listing page
page = requests.get('http://www.terry.uga.edu/courses/MIST/').content

#Turning html into BeautifulSoup4 object
soup = BeautifulSoup(page, 'lxml')

#Targeting the content section which houses undergrad and grad classes
content = soup.find('div', {'class': 'main-content'})

#Getting both grad and undergrad sections
programs = content.find_all('div', {'class':'span6'})

#Creating courseData dictionary to convert to json, and undergrad and grad to store information about respective levels
courseData = []
undergradData = []
gradData = []

#Creating the baselink to the website to build another request later
baselink = 'http://www.terry.uga.edu'

#Looping through both undergrad and grad levels
for program in programs:
    #Getting level text
    level = program.find('h2').text

    #Getting all course entries within this level
    courses = program.find('ul', {'class': 'list-ruled'}).find_all('li')

    #Iterating over each course
    for course in courses:
        #Delaying 1 second to prevent being caught in spam filter for later request
        time.sleep(1)

        #Pulling course link, abbrev, and name
        courseLink = course.find('a', href=True)['href']
        abbrev = course.find('span', {'class': 'course-number'}).text
        name = course.find('span', {'class': 'course-name'}).text

        #Breaking loop for bad data
        if(name == 'unavailable'):
            break

        #Getting information about course
        page = requests.get(baselink + courseLink).content
        soup = BeautifulSoup(page, 'lxml')

        #Pulling course info from the <p> tag it's housed in
        information = soup.find('div', {'class':'course-info'}).find_all('p')[1].text

        #Printing each course's information along with a divider
        print(level + ' ' + abbrev + ' ' + name + ' \nInformation: ' + information)
        print('--------------------------------------------------------------------------')

        #Adding course entry to respective dictionary
        if level == 'Undergraduate Level':
            undergradData.append(dict([('level', level), ('abbrev', abbrev), ('name', name), ('information', information)]))
        elif level == 'Graduate Level':
            gradData.append(dict([('level', level), ('abbrev', abbrev), ('name', name), ('information', information)]))

    #Printing separation per level
    print('#####################################################################################')

#Adding both dictionaries to larger dictionary of all courses
courseData.append(dict([('undergrad', undergradData)]))
courseData.append(dict([('grad', gradData)]))


#Writing json to file
with open('course_information.json', 'w') as outfile:
    json.dump(courseData, outfile)
