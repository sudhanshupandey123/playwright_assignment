from behave import *
from playwright.sync_api import sync_playwright
import time
import re
import csv
'''Opening Playwright And Chrome Browser To Perform The Task'''
p = sync_playwright().start()
browser = p.chromium.launch(headless=False)


'''After Completion of All Scenario Closing Windows And Page'''
def after_scenario(context):
    context.tab.close()
    context.page.close()
    browser.close()

'''
All Xpaths Used In This Test assignment'''
paths = {
    'search_box_xpath': "//input[@id='searchboxinput']",
    'search_icon':"//button[@id='searchbox-searchbutton']",
    'searched_interest_list_xpath': "//*[@class='Nv2PK THOPZb CpccDe ']/child::a",
    'restaurant_name_xpath': "//h1[@class='DUwDvf lfPIob']",
    'restaurant_rating_xpath': "//span[@class='ceNzKf']/preceding-sibling::span",
    'restaurants_address_xpath': "(//div[@class='rogA2c ']/child::div)[1]",
    'restaurant_review_xpath': "(//div[@class='F7nice ']/child::span)[2]",
}
@given(u'He Open Google Map')
def opening_google_map(context):
    '''Opening Amazon Page'''
    context.tab = browser.new_context()
    context.page = context.tab.new_page()
    context.page.goto("https://www.google.com/maps")


@when(u'He Search For "{user_searched_for}"')
def searching_for_inforamtion(context,user_searched_for):
    '''
    He is Searching For His Interest
    :param user_searched_for: Holds Value Of User Interest He Wants To Search
    :return:
    '''

    context.search_interest=user_searched_for
    context.page.locator(paths['search_box_xpath']).fill(context.search_interest)
    context.page.locator(paths['search_icon']).click()
    time.sleep(5)
    context.page.locator(paths['search_icon']).click()
    time.sleep(5)

@then(u'He Extract Information of Top "{user_requirement_value}" showing results')
def Extracting_Information(context,user_requirement_value):
    '''
    Extracting All Information Of Searched Items
    :param user_requirement_value: Holds Value Of How Much Items You want to extract
    :return:
    '''
    context.details=[]
    def info():
        '''It Extract All Information and store in List(context.details) so we can
        use that list to make csv file'''
        context.D={}
        try:
            context.D['name'] = context.page.locator(paths['restaurant_name_xpath']).text_content()
        except:
            context.D['name'] = 'NULL'

        try:
            context.D['rating'] = context.page.locator(paths['restaurant_rating_xpath']).text_content()
        except:
            context.D['rating'] = 'NULL'

        try:
            context.D['address'] = context.page.locator(paths['restaurants_address_xpath']).text_content()
        except:
            context.D['address'] = 'NULL'

        try:
            context.D['review'] = context.page.locator(paths['restaurant_review_xpath']).text_content()
        except:
            context.D['review'] = 'NULL'
        try:
            url = str(context.page.url)
            filtering_lat_and_long = re.search('@\d+\S{1}\d+,\d+\S{1}\d+', url)
            context.D['Log_and_Lat'] = filtering_lat_and_long.group()
            context.D['Log_and_Lat'] = context.D['Log_and_Lat'].replace('@', '')
        except:
            context.D['Log_and_Lat'] = 'NULL'
        context.details.append(context.D)

    while True:
        ele = context.page.locator("//a[@class='hfpxzc']").all()
        if len(ele)>int(user_requirement_value):
            break
        ele[1].click()
        time.sleep(2)
        context.page.keyboard.press('End')
    for i in range(0,int(user_requirement_value)):
        ele[i].click()
        time.sleep(5)
        info()

@then(u'He Make CSV File Of Those')
def Saving_Information_To_CSv(context):

    """
    Creating CSV File of the Searched_Item Details with the searched item name
    """

    field_names = ['name', 'rating', 'address', 'review', 'Log_and_Lat']
    with open(f'{context.search_interest}.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=list(context.D.keys()))
        writer.writeheader()
        writer.writerows(context.details)