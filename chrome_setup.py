from selenium import webdriver


def chrome_setup():
    # Keep Browser Open after Program Finishes
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=chrome_options)
    return driver
