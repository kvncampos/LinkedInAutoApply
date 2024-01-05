from chrome_setup import chrome_setup
from creds import USERNAME, PASSWORD
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep

#  ------------ Setup Chrome Selenium ------------
driver = chrome_setup()

# ------------ Main Page ------------
driver.get('https://www.linkedin.com')

# ------------ SIGN IN INSTRUCTIONS ------------
username = driver.find_element(By.NAME, value='session_key')
username.send_keys(USERNAME)
password = driver.find_element(By.NAME, value='session_password')
password.send_keys(PASSWORD)
sleep(2)
sign_in_button = driver.find_element(By.XPATH, value='//*[@id="main-content"]/section[1]/div/div/form/div[2]/button')
sign_in_button.click()

# # You may be presented with a CAPTCHA - Solve the Puzzle Manually
input("Press Enter when you have solved the Captcha. ")


# ------------ Using Filters/PreSet ------------

driver.get('https://www.linkedin.com/jobs/search/?currentJobId=3794094647&distance=25.0&f_AL=true&f_TPR=r86400&f_WT=2'
           '&geoId=103644278&keywords=Python&origin=JOB_SEARCH_PAGE_JOB_FILTER')

sleep(3)

# ---------- GET ALL JOBS FIRST PAGE ----------
i = 0
while i < 4:
    jobs_list = driver.find_elements("css selector", ".job-card-container--clickable")
    print(len(jobs_list), " Jobs")
    driver.execute_script("arguments[0].scrollIntoView();", jobs_list[-1])
    sleep(2)
    i += 1

# ---------- INTERACT EACH JOB INDIVIDUALLY ----------
# ... (previous code)

# ---------- INTERACT EACH JOB INDIVIDUALLY ----------
for each in jobs_list:
    try:
        button = each.find_element(By.CSS_SELECTOR, 'li')
        button.click()
        sleep(2)

        # Check for the "Easy Apply" button
        apply_button = driver.find_element(By.CSS_SELECTOR, '.jobs-apply-button--top-card')
        if apply_button.text == 'Easy Apply':
            print('Confirming Easy Apply Button')
            apply_button.click()
            sleep(2)

            # Handle the Easy Apply process
            next_step = driver.find_element(By.XPATH,
                                            '/html/body/div[3]/div/div/div[2]/div/div[2]/form/footer/div[2]/button')
            if next_step.text == 'Next':
                print('Confirming Next Button')
                next_step.click()
                sleep(1)
            try:
                next_step2 = driver.find_element(By.XPATH,
                                                 '/html/body/div[3]/div/div/div[2]/div/div[2]/form/footer/div[2]/button[2]')
                if next_step2.text == 'Next':
                    print('Confirming Next Button')
                    next_step2.click()
                    sleep(2)

                questions = driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div[2]/div/div[2]/form/div/div/h3')
                if questions.text == 'Additional Questions':
                    print('Checking for Radio Button.')
                    try:
                        radio_button_field = WebDriverWait(driver, 5).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR,
                                                            'fieldset[data-test-form-builder-radio-button-form-component="true"]'))
                        )

                        # If the radio button field exists, you can skip the relevant part of the form
                        print("Radio button field exists, skipping this part of the form.")
                        quit = driver.find_element(By.XPATH, '/html/body/div[3]/div/div/button')
                        quit.click()
                        sleep(2)
                        discard = driver.find_element(By.XPATH, '/html/body/div[3]/div[2]/div/div[3]/button[1]')
                        discard.click()
                        continue
                    except TimeoutException:
                        # If the radio button field doesn't exist, proceed with filling in the form
                        print("Radio button field does not exist, continuing with the form.")

                    form = driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div[2]/div/div[2]/form')
                    # Find all div elements with the specified attribute inside the form
                    div_elements = form.find_elements(By.XPATH,
                                                              ".//div[@data-test-single-line-text-form-component='']")
                    # Iterate through each element and fill it with the number 2
                    for element in div_elements:
                        print('Filling out Blank Values with 2.')
                        try:
                            # Find the input element within the current structure
                            input_element = element.find_element(By.CSS_SELECTOR, 'input[aria-describedby*="numeric"]')

                            # Fill the input with the number 2
                            input_element.clear()
                            input_element.send_keys('2')

                            # Wait for the error message to disappear if it exists
                            WebDriverWait(driver, 3).until_not(
                                EC.visibility_of_element_located((By.CSS_SELECTOR,
                                                                  '[aria-describedby*="numeric-error"]')))

                        except Exception as e:
                            # Handle any exceptions as needed
                            print(f"Exception: {e}")

            except Exception as e:
                print("No Second Button.")


            print('Confirming Review Button')
            review = driver.find_element(By.XPATH,
                                         '/html/body/div[3]/div/div/div[2]/div/div[2]/form/footer/div[2]/button[2]')
            if review.text == 'Review':
                review.click()
                sleep(2)

            print('Confirming Submit Button')
            try:
                submit_button = driver.find_element(by=By.XPATH, value="/html/body/div[3]/div/div/div[2]/div/div[2]/div/footer/div[3]/button[2]")

            except:
                print("issue with Submit button")
            try:
                print('Second Attempt...')
                submit_button = driver.find_element(by=By.CSS_SELECTOR, value='footer button')
                sleep(2)

            except:
                print("issue with Submit button again")
                quit = driver.find_element(By.XPATH, '/html/body/div[3]/div/div/button')
                quit.click()
                sleep(2)
                discard = driver.find_element(By.XPATH, '/html/body/div[3]/div[2]/div/div[3]/button[1]')
                discard.click()
                sleep(2)
                continue

            else:
                if submit_button.text == 'Submit application':
                    submit_button.click()
                    sleep(2)

                print("Exiting Job Application")
                exit_button = driver.find_element(By.XPATH, value='/html/body/div[3]/div/div/button')
                exit_button.click()
                sleep(1)

    except Exception as e:
        print(f"Easy Apply Button Not Available. ")

# driver.quit()
