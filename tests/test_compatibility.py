import pytest
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# import time


@pytest.mark.compatibility
def test_sample():
    print("rb status compatibility test was called.")
    return True


# def airflow_login(driver):
#     """
#     Login to airflow and go to reports page
#     """
#     #####################################
#     # Connect to Local Airflow instance #
#     #####################################
#     driver.get("localhost:8080/home")
#     #####################################
#     # Sign in                           #
#     #####################################
#     username = driver.find_element_by_name("username")
#     username.send_keys("admin")
#     password = driver.find_element_by_name("password")
#     password.send_keys("admin")
#     password.send_keys(Keys.RETURN)
#     #####################################
#     # Go to reports page                #
#     #####################################
#     driver.find_element_by_xpath(
#         "/html/body/header/div/div/div[2]/ul[1]/li[7]/a"
#     ).click()
#     driver.find_element_by_xpath(
#         "/html/body/header/div/div/div[2]/ul[1]/li[7]/ul/li[2]/a"
#     ).click()


# def create_report(driver, report_name):
#     """
#     Connects to a local instance of airflow and creates a sample report.
#     """

#     #####################################
#     # Create a new report               #
#     #####################################
#     # click create report buttom
#     driver.find_element_by_xpath('//*[@id="reports-heading"]/a').click()

#     # fill in the fields
#     field = driver.find_element_by_id("report_title")
#     field.send_keys(report_name)

#     field = driver.find_element_by_id("description")
#     field.send_keys("This is a description about the selenium report test.")

#     field = driver.find_element_by_id("owner_name")
#     field.send_keys("Mike Sadler")

#     field = driver.find_element_by_id("owner_email")
#     field.send_keys("msadler@raybeam.com")

#     field = driver.find_element_by_id("subscribers")
#     field.send_keys("cericson@raybeam.com")
#     # select the tests
#     driver.find_element_by_id("s2id_autogen3").click()
#     driver.find_element_by_id("select2-result-label-6").click()

#     # save form
#     driver.find_element_by_xpath('//*[@id="model_form"]/div[4]/button').click()


# def check_report_exists(driver, report_name):
#     """
#     Check that report was created in list of reports.
#     """
#     table = driver.find_element_by_id("reports")
#     for row in table.find_elements_by_xpath(".//tr"):
#         for cell in row.find_elements_by_tag_name("td"):
#             if report_name == cell.text:
#                 return True
#     return False


# def delete_report(driver, report_name):
#     """
#     Cleanup and delete the report.
#     """
#     table = driver.find_element_by_id("reports")
#     index = 0
#     for row in table.find_elements_by_xpath(".//tr"):
#         for cell in row.find_elements_by_tag_name("td"):
#             if report_name == cell.text:
#                 print("Deleting report: " + cell.text)
#                 driver.find_element_by_xpath(
#                     '//*[@id="reports"]/tbody/tr[%d]/td[8]/a[2]' % index
#                 ).click()
#                 obj = driver.switch_to.alert
#                 time.sleep(2)
#                 obj.accept()
#         index += 1


# report_name = "selenium report test"
# driver = webdriver.Chrome()
# airflow_login(driver)

# @pytest.mark.compatibility
# def test_report_creation():
#     create_report(driver, report_name)
#     return check_report_exists(driver, report_name)


# @pytest.mark.compatibility
# def test_report_deletion():
#     time.sleep(2)
#     delete_report(driver, report_name)
