from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd 
import time
from openpyxl import load_workbook

driver = webdriver.Chrome()
homeUrl = 'https://clutch.co'
driver.get(homeUrl)


# extracting name and urls of divisions under group Development
groupDevelopment = driver.find_element(By.XPATH, '/html/body/main/article/section[2]/div/div[2]/div[1]/nav')
divisionsDevelopment = groupDevelopment.find_elements(By.CLASS_NAME, 'sitemap-nav__item' )
divisions = []
for division in divisionsDevelopment:
    divisionUrl = division.get_attribute('href')
    divisionName = division.get_attribute('innerText')
    divisions.append([divisionName, divisionUrl])
    totalDivisions = len(divisions)
driver.quit()

# excel sheet to store data 
pathExcel = 'C:/Users/jaint/OneDrive/Desktop/data.xlsx'
book = load_workbook(path)
writer = pd.ExcelWriter(pathExcel, engine = 'openpyxl')
writer.book = book



for i in range(totalDivisions):
    divisionUrl = divisions[i][1]
    divisionName = divisions[i][0]
    
    # getting total number of pages for one division
    driver = webdriver.Chrome()
    driver.get(divisionUrl)
    totalPages = driver.find_element(By.XPATH, '/html/body/main/section[1]/nav/ul/li[13]/a').get_attribute('data-page')
    driver.quit()
    
    for page in range(int(totalPages)):
        pgUrl = divisionUrl + '?page=' + str(page)
        driver = webdriver.Chrome()
        driver.get(pgUrl)   
        time.sleep(1)
            
        postings = driver.find_elements(By.CLASS_NAME, "provider.provider-row.sponsor")
        postingNum = len(postings)
        for i in range(1, postingNum + 1):
            
            path = '/html/body/main/section[1]/div[2]/ul/li['+str(i)+']'
            try:
                posting = driver.find_element(By.XPATH, path)
                clutchProfileLink = driver.find_element(By.XPATH, path + '/div/div[1]/div[1]/div/a').get_attribute('href')
                websiteLink = driver.find_element(By.XPATH, path + '/div/div[2]/ul/li[1]/a').get_attribute('href')
                companyName = driver.find_element(By.XPATH, path + '/div/div[1]/div[1]/div/h3').text
                rating = driver.find_element(By.XPATH, path + '/div/div[1]/div[1]/div/div[1]/span').text
                reviewCount = driver.find_element(By.XPATH, path + '/div/div[1]/div[1]/div/div[1]/a[2]').text
                
                try: 
                    posting.find_element(By.CLASS_NAME, 'verification_icon')
                    companyLocation = driver.find_element(By.XPATH, path + '/div/div[1]/div[2]/div[1]/div[2]/div[4]/span').text
                    hourlyRate = driver.find_element(By.XPATH, path + '/div/div[1]/div[2]/div[1]/div[2]/div[2]/span').text
                    minProjectSize = driver.find_element(By.XPATH, path + '/div/div[1]/div[2]/div[1]/div[2]/div[1]/span').text
                    employeeSize = posting.find_element(By.XPATH, path + '/div/div[1]/div[2]/div[1]/div[2]/div[3]/span').text
                except:
                    companyLocation = driver.find_element(By.XPATH, path + '/div/div[1]/div[2]/div[1]/div/div[4]').text
                    hourlyRate = driver.find_element(By.XPATH, path + '/div/div[1]/div[2]/div[1]/div/div[2]').text
                    minProjectSize = driver.find_element(By.XPATH, path + '/div/div[1]/div[2]/div[1]/div/div[1]').text
                    employeeSize = posting.find_element(By.XPATH, path + '/div/div[1]/div[2]/div[1]/div/div[3]').text
        
        
                posting_data = [companyName, clutchProfileLink, websiteLink, rating, reviewCount, hourlyRate, 
                              employeeSize, minProjectSize,companyLocation]
                
                data.append(posting_data)
               
            except:
                print('fail')
                break
        driver.quit()
        time.sleep(2)
    
    headers = ['Name', 'Clutch Profile Link', 'Website Link', 'Rating', 'Review Count', 
                'Hourly Rate', 'Employee Size', 'Minimum Project Size', 'Company Location']
    table = pd.DataFrame(data, columns = headers)
    table.to_excel(writer, sheet_name= divisionName)
    

    
    
    
    
    
    
    
    
   
