import time
import multiprocessing as mp


from utils import (
    get_chrome_driver,
    wait_for_element,
    check_exists_by_xpath,
    write_to_txt,
    ElementNotInteractableException
)


def main():
    username = "test@test.com"
    password = "test123"
    form_wait = 50 # mins

    driver = get_chrome_driver()

    # Login
    driver.get("https://auth.global-exam.com/login")

    wait_for_element(
        driver, '//form[@id="login-form"]//button[@type="submit"]')

    email_input = driver.find_element_by_xpath(
        '//form[@id="login-form"]//input[@id="email"]')
    email_input.send_keys(username)

    password_input = driver.find_element_by_xpath(
        '//form[@id="login-form"]//input[@id="password"]')
    password_input.send_keys(password)

    loign_btn = driver.find_element_by_xpath(
        '//form[@id="login-form"]//button[@type="submit"]')
    loign_btn.click()

    wait_for_element(driver, '//h1[contains(@class, "leading-tighter")]')

    # close if cookies popup is present
    try:
        wait_for_element(driver, '//button[@id="axeptio_btn_acceptAll"] | //button[text()="Tout accepter"]', timeout=20)
        popup_cancel_btn = driver.find_element_by_xpath('//button[@id="axeptio_btn_acceptAll"] | //button[text()="Tout accepter"]')
        popup_cancel_btn.click()
    except Exception as e:
        pass

    # Open Test Language dropdown
    test_language_dropdowns = driver.find_elements_by_xpath(
        '//span[contains(text(), "Prepare for the")]//.. | //span[contains(text(), "Je m\'entraîne au ")]//..')
    for btn in test_language_dropdowns:
        if btn.is_displayed():
            btn.click()
            time.sleep(2)
            break

    # Select French
    test_language_btns = driver.find_elements_by_xpath(
        '//span[@data-title="French"] | //span[@data-title="Français"]')
    for btn in test_language_btns:
        if btn.is_displayed():
            btn.click()
            time.sleep(2)
            break

    # Select DALF C1 option
    try:
        dalf_c1_btn = driver.find_element_by_xpath(
            '//span[text()="DALF C1"]')
        dalf_c1_btn.click()
        time.sleep(5)
    except ElementNotInteractableException:
        pass

    # Training
    excercises_url = "https://exam.global-exam.com/library/trainings"

    driver.get(excercises_url)

    wait_for_element(driver, '//span[text()="Compréhension écrite"] | //span[text()="Reading"]')

    written_comprehension = driver.find_element_by_xpath(
        '//span[text()="Compréhension écrite"] | //span[text()="Reading"]')
    written_comprehension.click()

    time.sleep(10)

    wait_for_element(driver, '//button[text()="Relancer"] | //button[text()="Lancer"] | //button[text()="Start"] | //button[text()="Try again"]')

    all_start_buttons = driver.find_elements_by_xpath(
        '//button[text()="Relancer"] | //button[text()="Lancer"] | //button[text()="Start"] | //button[text()="Try again"]')

    i = 0
    while i < len(all_start_buttons):
        # Go to Form
        start_btn = driver.find_elements_by_xpath(
        '//button[text()="Relancer"] | //button[text()="Lancer"] | //button[text()="Start"] | //button[text()="Try again"]')[i]
        start_btn.click()

        # close if popup is present
        try:
            wait_for_element(driver, '//button[text()="Démarrer"] | //button[text()="Start"]')
            popup_cancel_btn = driver.find_element_by_xpath('//button[text()="Démarrer"] | //button[text()="Start"]')
            popup_cancel_btn.click()
        except:
            pass

        wait_for_element(driver, '//*[@data-icon="clock"]')

        # Fill up form
        all_questions = driver.find_elements_by_xpath('//p[contains(text(), "Question")]//..//..')
        for question in all_questions:

            # check if question has selection option
            if check_exists_by_xpath(question, './/input[@type="radio"]'):
                suggestion_btn = question.find_element_by_xpath('.//*[@data-icon="chevron-down"]')
                suggestion_btn.click()
                time.sleep(2)

                # answer radio option
                correct_radio_option = question.find_element_by_xpath('.//label[contains(@class, "success")]')
                correct_radio_option.click()
                time.sleep(2)
            elif check_exists_by_xpath(question, './/textarea'):
                # answer in text area
                suggestion_btn = question.find_element_by_xpath('.//*[@data-icon="chevron-down"]')
                suggestion_btn.click()
                time.sleep(2)

                # suggestion text
                suggestion_text = question.find_elements_by_xpath('.//span[text()="Suggestion"]//..//following-sibling::div//p')
                suggestion_text = [st.text for st in suggestion_text]
                suggestion_text = "\n".join([st for st in suggestion_text if st])

                suggestion_input = question.find_element_by_xpath('.//textarea')
                suggestion_input.send_keys(suggestion_text)
                time.sleep(2)

        # wait to log for the form
        time.sleep(form_wait * 60)

        # click on Finish buton
        terminate_btn = driver.find_element_by_xpath('//button[text()="Terminer"] | //button[text()="Finish"]')
        terminate_btn.click()

        # Go back to list
        wait_for_element(driver, '//span[text()="Back to the list"] | //span[text()="Retour à la liste"]')

        back_btn = driver.find_element_by_xpath('//span[text()="Back to the list"] | //span[text()="Retour à la liste"]')
        back_btn.click()

        wait_for_element(driver, '//button[text()="Relancer"] | //button[text()="Lancer"] | //button[text()="Start"] | //button[text()="Try again"]')

        i += 1

    driver.quit()


if __name__ == "__main__":
    p = mp.Process(target=main)
    p.start()
    p.join()
