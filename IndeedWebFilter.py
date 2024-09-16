############################################################
'''
file: IndeedWebFilter.py

Description: 

Automatically search Indeed.com and hide certain job
postings based on job titles.

This program must be able to see the "IndeedFilters.json" file
to automatically fill in website search inputs and filter out
unwanted job titles.
'''
############################################################


############################################################
'''
Imports:
selenium    for automatically opening webpages and entering data
json        to read what filters to use on indeed.com
sys         to use exit code function
time        for manual pauses in program flow
'''
############################################################
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common import NoSuchElementException, TimeoutException
import json
import sys
import time


############################################################
'''
Function: explicitWaitByClass

Description: Given a class name as a parameter, find the
element by that class name on the webpage and return it 
but timeout after a certain amount of time if not found.

Parameters:
name            string of the class name

Return:
elem            element object
'''
############################################################
def explicitWaitByClass(name):
    elem = EC.presence_of_element_located((By.CLASS_NAME, name))
    wait = WebDriverWait(driver, timeout=5)
    return wait.until(elem)

############################################################
'''
Function: explicitWaitByID

Description: Given a ID name as a parameter, find the
element by that ID name on the webpage and return it 
but timeout after a certain amount of time if not found.

Parameters:
name            string of the ID name

Return:
elem            element object
'''
############################################################
def explicitWaitByID(name):
    elem = EC.presence_of_element_located((By.ID, name))
    wait = WebDriverWait(driver, timeout=5)
    return wait.until(elem)

############################################################
'''
Function: clearElementInputVal

Description: Given a search element input object as a parameter, 
find the element on the webpage and clear the input by
backspacing as many times as the length of characters.

Parameters:
elem            element object that is a search input

Return:
No return
'''
############################################################
def clearElementInputVal(elem):
        elemValLen = len(elem.get_attribute('value'))
        while(elemValLen > 0):
            elem.send_keys(Keys.BACK_SPACE)
            elemValLen = len(elem.get_attribute('value'))

############################################################
'''
Function: getIndeedFilters

Description: Find local .json file, read its content and
assign it to global variables. Lastly print out the content
to termainal to let user know what filters were found.

Parameters:
No parameters

Return:
No return
'''
############################################################
def getIndeedFilters():
    try:
        with open (filterFileName, 'r') as jsonFile:
            jsonFilters = json.load(jsonFile)
            print('Local JSON file found. Loading filters...')

        global jobInputVal
        global locationInputVal
        global workModelVal
        global jobTitleFilters
        
        filters = jsonFilters['filters']
        for filter in filters:
            for key in filter:
                #print('=>' + key + ': ' + str(filter[key]))
                if(key == "Job Title"):
                    jobInputVal = filter[key]
                if(key == "Location" and len(key) > 0):
                    locationInputVal = filter[key]
                if(key == "Work Model" and len(key) > 0):
                    workModelVal = filter[key]
                if(key == "Job Title Filters" and len(key) > 0):
                    jobTitleFilters = filter[key]
        print('''\n        The following filters will be used on Indeed.com:
         \u2022 Job Title: {0}
         \u2022 Location: {1}
         \u2022 Work Model: {2}
         \u2022 Job Title Filters: {3}
    '''.format(jobInputVal, locationInputVal, workModelVal, str(jobTitleFilters)))
        return True
    except FileNotFoundError:
        print('\nFile not found: "' + filterFileName + '"')
        print('\nPlease make sure "' + filterFileName + '" is in the same directory as this program')
        return False
    except Exception as e:
        print('\nAn uncaught error has occured:')
        print(type(e).__name__ + ' ' + e.__doc__)
        return False

############################################################
'''
Function: promptContinueProgram

Description: Pause the program when this function is called
then ask the end-user if they would like to continue or
enter a specitic character to properly close this program.

Parameters:
No parameters

Return:
No return
'''
############################################################
def promptContinueProgram():
    proceed = input('Enter any key to continue or "q" to close this program: ')
    if(proceed.lower() == 'q'):
        print('\nClosing program...\n')
        sys.exit(0)

############################################################
'''
Function: chkHumanVerification

Description: Once the Indeed.com website is initially loaded,
detect if Cloudflare is prompting for human verification.

Parameters:
No parameters

Return:
True/False          Boolean if verification is found
'''
############################################################
def chkHumanVerification():
    try:
        cfPagePresent = explicitWaitByID('challenge-form')
        if(cfPagePresent):
            return True
        else:
            return False
    except:
         return False

############################################################
'''
Function: searchInputTitleLocation

Description: Find the first two search text boxes on indeed.com,
erase any text currently in the text boxes, and then auto-type
in the Job Title and Location. Finally click on the submit button.

Parameters:
No parameters

Return:
True/False          Boolean if submit is successful or not
'''
############################################################
def searchInputTitleLocation():
    global jobInputVal
    global locationInputVal
    try:
        time.sleep(1)
        jobInputElem = explicitWaitByID('text-input-what')
        clearElementInputVal(jobInputElem)
        jobInputElem.send_keys(jobInputVal)
        locationInputElem = explicitWaitByID('text-input-where')
        clearElementInputVal(locationInputElem)
        locationInputElem.send_keys(locationInputVal)
        submitBtn = explicitWaitByClass('yosegi-InlineWhatWhere-primaryButton')
        submitBtn.click()
        return True
    except NoSuchElementException as e:
        #print(type(e).__name__ + ' ' + e.__doc__)
        return False
    except TimeoutException as e:
        print('Could not find inputs')
        #print(type(e).__name__ + ' ' + e.__doc__)
        return False
    except Exception as e:
        #print(type(e).__name__ + ' ' + e.__doc__)
        return False

############################################################
'''
Function: selectFilterPillList

Description: Auto-select Indeed's built-in filters on results page

Parameters:
No parameters

Return:
True/False          Boolean if sucessful or not
'''
############################################################
def selectFilterPillList():
    try:
        global workModelVal
        # Check if Remote filter should be selected
        if(workModelVal):
            workModelElem = explicitWaitByID('filter-remotejob')
            workModelElem.click()
            workModelOpetions = explicitWaitByID('filter-remotejob-menu')
            workModelElemOption = workModelOpetions.find_element(By.LINK_TEXT, workModelVal)
            workModelElemOption.click()
        return True
    except Exception as e:
        #print(type(e).__name__ + ' ' + e.__doc__)
        return False
    
############################################################
'''
Function: hideJobPostings

Description: Go through each job posting currently shown on
Indeed's search results. Check each Job Title and compare it
with the filters in the JSON file. If a keyword is found in
the job post title, inject Javascript that will add CSS to
hide the element job post.

Parameters:
No parameters

Return:
True/False          Boolean if hiding job posts is successful or not
'''
############################################################
def hideJobPostings():
    global jobTitleFilters
    if(len(jobTitleFilters) > 0):
        try:
            jobsUlElem = explicitWaitByClass('css-zu9cdh')
            jobsLiElems = jobsUlElem.find_elements(By.TAG_NAME, 'li')
        except:
            print('\tCould not find job posting results')
            return False
        # Go through each job posting container and inject CSS to certain jobs to hide them
        for li in jobsLiElems:
            try:
                jobTitleSpanEl = li.find_element(By.TAG_NAME, 'span')
                if(len(jobTitleSpanEl.text) > 0): # Some empty "li" elements are showing up. This "if" condiditon skips these tags
                    indeedJobTitle = jobTitleSpanEl.text
                    for jobTitleFilter in jobTitleFilters:
                        if(jobTitleFilter.lower() in indeedJobTitle.lower()):
                            print('\tHiding job post: "{}"'.format(indeedJobTitle))
                            try:
                                driver.execute_script("""
                                    let children = arguments[0].childNodes;
                                        for(let child of children){
                                            if(child.tagName == 'DIV'){
                                                child.hidden = true;
                                                child.style.display = 'none';
                                                child.style.visibility = 'hidden';
                                            }
                                }""", li)
                            except Exception:
                                pass
            except NoSuchElementException as e:
                pass
    return True
    
############################################################
'''
Function: getPaginationNumbers

Description: Use parameter to determine which page number
the end-user would like to load or close the program if a 
certain character is typed in.

Parameters:
userPage            Int of desired page number to load

Return:
True/False          Boolean if sucessful or not
'''
############################################################
def getPaginationNumbers(userPage):
    try:
        if(userPage.lower() == 'q'):
            print('Closing program...\n')
            driver.close()
            sys.exit(0)
        userPage = int(userPage)
        userPage = str(userPage)
    except Exception as e:
        print(type(e).__name__ + ' ' + e.__doc__)
        print('That was not a number. Please try again.\n')
        return False
    try:
        # Find Pagination navigation (at bottom of job posting results)
        pageNavUlElem = explicitWaitByClass('css-1g90gv6')
        pageNavLiElem = pageNavUlElem.find_elements(By.TAG_NAME, 'li')
        for li in pageNavLiElem:
            aElem = li.find_element(By.TAG_NAME, 'a')
            try:
                indeedPageNum = aElem.text
                if(indeedPageNum == userPage):
                    aElem.click()
                    return True
            except:
                pass
        print('Page number not found. Please try again.\n')
        return False
    except Exception as e:
        #print(type(e).__name__ + ' ' + e.__doc__)
        return False

############################################################
'''
Variables:
Global variables populated when local json file is read
'''
############################################################
filterFileName = "IndeedFilters.json"
jobInputVal = ""
locationInputVal = ""
workModelVal = ""
jobTitleFilters = ""

############################################################
'''
Main:
The following is the program's executions
'''
############################################################

# Read JSON file and load Indeed filters
print('\nReading local JSON file: "' + filterFileName + '"')
validIndeedFilters = getIndeedFilters()
if(validIndeedFilters == False):
    print('Closing program...\n')
    sys.exit(1)

promptContinueProgram()

# Load Indeed website using JSON values
print('\n\tPlease Wait. Indeed website is loading...')
service = Service('/usr/local/bin/chromedriver')
options = webdriver.ChromeOptions()
#options.add_argument('--headless')
driver = webdriver.Chrome(service=service, options=options)
url = "https://www.indeed.com"
driver.get(url)

# Check loaded webpage for CloudFlare verification
print('\tPlease Wait. Checking if there is a Human verification page...')
cfPagePreset = chkHumanVerification()
if(cfPagePreset):
    print('\t\tWarning: Human Verification page detected\n\t\tTry verifiying fist and then let the next page load before continuing.\n')
    promptContinueProgram()

# Get search and locaiton inputs. Selenium will auto-type in text and submit.
print('\tPlease wait. Job Title and Location will be automatically entered and submitted...')
validSearchTitleLocation = searchInputTitleLocation()
while(validSearchTitleLocation == False):
    print('\n\tAutomation or page could not load properly.\nWould you like to try to load the page again?\n')
    validSearchTitleLocation = searchInputTitleLocation()

# Once initial results page is loaded the built-in filters will be auto selected
print('\tPlease wait. Indeed built-in filters will be auto-selected...')
validFilterPillList = selectFilterPillList()
while(validFilterPillList == False):
    print('\t\tWarning: Issues found when auto-selecting Indeed built-in filters. Would you like to try again?\n')
    promptContinueProgram()
    validFilterPillList = selectFilterPillList()

# Go through job posting results and hide certain posts
print('\n\tPlease Wait. Attempting to filter out job postings...')
validJobPostings = hideJobPostings()
while(validJobPostings == False):
    print('\n\tWarning: Issues hiding job postings.\n')
    promptContinueProgram()
    validJobPostings = hideJobPostings()

# Ask which page number the user would like to load or quit the program
print('\nYou may now check your results.')
while(True):
    userPage = input('\nEnter a page number you would like to load or enter "q" to close this program: ')
    if(getPaginationNumbers(userPage)):
        print('\n\tPlease Wait. Attempting to load next page and filter out job postings...')
        hideJobPostings()
