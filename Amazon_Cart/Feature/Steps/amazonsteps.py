'''All Used Modules'''
import time
import re
from behave import *
from playwright.sync_api import sync_playwright

'''Opening Playwright And Chrome Browser To Perform The Task'''
p = sync_playwright().start()
browser = p.chromium.launch(headless=False)

'''After Completion of All Scenario Closing Windows And Page'''


def after_scenario(context):
    context.tab.close()
    context.page.close()
    browser.close()


'All Xpath Used In This Task'
xpath = {
    'product_search_input_box': "//input[@id='twotabsearchtextbox']",
    'searching_icon': "//input[@id='nav-search-submit-button']",
    'rating_filteration_box': "(//li[@id='p_72/1318476031']/ancestor::ul)/descendant::li",
    'all_visible_suggested_product_list': "//h2[@class='a-size-mini a-spacing-none a-color-base s-line-clamp-2']//a",
    'add_to_cart_button': "//input[@id='add-to-cart-button']",
    'cart_box': "//div[@id='nav-cart-count-container']",
    'product_actual_price': "//div[@class='sc-badge-price-to-pay']",
    'price_showing_to_cart': "(//span[@class='a-size-medium a-color-base sc-price sc-white-space-nowrap'])[1]",
    'search_text':"(//div[@class='sg-col-inner']//span)[3]",
    'new_page_title':"//span[@id='productTitle']",
    'successfully_added_icon':"//div[@id='attachDisplayAddBaseAlert']//div//i",
    'Cart_Value':"//span[@id='nav-cart-count']",

}


@given(u'User Is On Amazon Page')
def opening_amazon_page(context):
    '''Opening Amazon Page'''
    context.tab = browser.new_context()
    context.page = context.tab.new_page()
    context.page.goto("http://www.amazon.in/")


@when(u'He Search For Product "{product_name}" and filtering based on rating "{rating}"')
def searching_and_filtering_product_based_on_rating(context, product_name, rating):
    '''
    Searching For the product
    :param product_name:Holding Name of Product User Want To Search
    '''
    context.product_name = product_name
    context.page.locator(xpath['product_search_input_box']).fill(context.product_name)
    context.page.locator(xpath['searching_icon']).click()
    try:
        verifying_search_text=context.page.locator(xpath['search_text']).text_content()
        assert verifying_search_text == context.product_name,'Proper Result Is Not Coming'
    except AssertionError as msg:
        print(msg)
    rating_box = context.page.locator(xpath['rating_filteration_box'])
    Rating_Dict = {4: 0, 3: 1, 2: 2, 1: 3}
    for rating_key in Rating_Dict:
        if int(rating) == rating_key:
            rating_box.nth(Rating_Dict[rating_key]).click()
            try:
                assert context.page.title == f'Amazon.in: Lenovo Laptop - {int(rating)} Stars & Up','Rating Boxes Are Not Working'
            except AssertionError as msg:
                print(msg)
            time.sleep(8)
            break


@when('He add first "{number_of_product_want_to_add}" product to cart')
def adding_product_to_cart(context, number_of_product_want_to_add):
    '''
    Adding Those Product To cart which user searhced 
    :param number_of_product_want_to_add: Holds Value How Many User Want To Add To cart

    '''
    all_filtered_product = context.page.locator(xpath['all_visible_suggested_product_list'])
    added_to_cart = 1
    for i in range(0, all_filtered_product.count() + 1):
        if added_to_cart > int(number_of_product_want_to_add):
            break
        if re.search(context.product_name.split()[0], all_filtered_product.nth(i).text_content()):
            with context.tab.expect_page() as new_page_info:
                verification_product_title=all_filtered_product.nth(i).text_content()
                all_filtered_product.nth(i).click()
                time.sleep(2)  # Opens a new tab
            new_page = new_page_info.value
            try:
                assert new_page.locator(xpath['new_page_title']).text_content()==verification_product_title,'Not Able To Click On Correct Product'
            except AssertionError as msg:
                print(msg)
            new_page.locator(xpath['add_to_cart_button']).click()
            try:
                assert new_page.locator(xpath['successfully_added_icon']).is_visible(),'Add_To_Cart Is Not Working Properly'
            except AssertionError as msg:
                print(msg)
            time.sleep(3)
            new_page.close()
            context.page.reload()
            time.sleep(2)
            added_to_cart += 1
    try:
        assert context.page.locator(xpath['Cart_Value']).text_content()==number_of_product_want_to_add,'Not Added Properly'
    except AssertionError as msg:
        print(msg)


@then('the cart value should be sum of products')
def verifying_actual_price_with_summarised_price(context):
    '''
    Finally Verifying Whether The Total Price And Summarized Price Are Same Or Not
    '''
    actual_price = 0
    context.page.locator(xpath['cart_box']).click()
    time.sleep(3)
    time.sleep(3)
    price_list = context.page.locator(xpath['product_actual_price'])
    for i in range(0, price_list.count()):
        actual_price += float(price_list.nth(i).inner_text().replace(',', ''))
    summarized_price = context.page.locator(xpath['price_showing_to_cart']
                                            ).inner_text()

    try:
        assert float(summarized_price.replace(',', '')) == actual_price, 'Cart Is Not Performing'
    except AssertionError as msg:
        print(msg)
