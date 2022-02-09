import time
import multiprocessing as mp


from utils import (
    get_chrome_driver,
    wait_for_element,
    check_exists_by_xpath,
    ElementNotInteractableException
)


def main():
    username = "test@test.com"
    password = "test123"
    form_wait = 19 # mins

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

    # Open Test Language dropdown
    test_language_dropdowns = driver.find_elements_by_xpath(
        '//span[contains(text(), "Prepare for the")]//.. | //span[contains(text(), "Je m\'entraîne au ")]//..')
    for btn in test_language_dropdowns:
        if btn.is_displayed():
            btn.click()
            time.sleep(2)
            break

    # Select English
    test_language_btns = driver.find_elements_by_xpath(
        '//span[@data-title="English"] | //span[@data-title="Anglais"]')
    for btn in test_language_btns:
        if btn.is_displayed():
            btn.click()
            time.sleep(2)
            break

    # Select Linguaskill Business option
    try:
        dalf_c1_btn = driver.find_element_by_xpath(
            '//span[text()="Linguaskill Business"]')
        dalf_c1_btn.click()
        time.sleep(5)
    except ElementNotInteractableException:
        pass

    # Training
    excercises_url = "https://exam.global-exam.com/library/trainings"

    driver.get(excercises_url)

    # Select Listening block
    wait_for_element(driver, '//font[text()="listening"] | //span[text()="Listening"]')

    written_comprehension = driver.find_element_by_xpath(
        '//font[text()="listening"] | //span[text()="Listening"]')
    written_comprehension.click()


    # Select Extended registeration
    wait_for_element(driver, '//font[text()="Extended registration"] | //span[text()="Enregistrement étendu"] | //span[text()="Extended listening"]')

    extended_registration = driver.find_element_by_xpath(
        '//font[text()="Extended registration"] | //span[text()="Enregistrement étendu"] | //span[text()="Extended listening"]')
    extended_registration.click()

    time.sleep(10)

    wait_for_element(driver, '//button[text()="Continuer"] | //button[text()="Relancer"] | //button[text()="Lancer"] | //font[text()="To throw"] | //font[text()="To restart"] | //button[text()="Try again"] | //button[text()="Continue"]')

    all_start_buttons = driver.find_elements_by_xpath(
        '//button[text()="Continuer"] | //button[text()="Relancer"] | //button[text()="Lancer"] | //font[text()="To throw"] | //font[text()="To restart"] | //button[text()="Try again"] | //button[text()="Continue"]')

    # Excercise Loop
    i = 0
    while i < len(all_start_buttons):
        # Go to Form
        start_btn = driver.find_elements_by_xpath(
        '//button[text()="Continuer"] | //button[text()="Relancer"] | //button[text()="Lancer"] | //font[text()="To throw"] | //font[text()="To restart"] | //button[text()="Try again"] | //button[text()="Continue"]')[i]
        start_btn.click()

        # close if popup is present
        try:
            wait_for_element(driver, '//button[text()="Démarrer"] | //button[text()="Start"]', timeout=20)
            popup_cancel_btn = driver.find_element_by_xpath('//button[text()="Démarrer"] | //button[text()="Start"]')
            popup_cancel_btn.click()
        except Exception as e:
            pass

        wait_for_element(driver, '//*[@data-icon="clock"]')

        # Excercise Pages loop
        next_page = True
        while next_page:
            # Fill up form for current excercise page
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

            try:
                # Click on To validate if present
                wait_for_element(driver, '//font[text()="To validate"] | //button[text()="Valider"] | //button[text()="Confirm"]')

                to_validate = driver.find_element_by_xpath(
                    '//font[text()="To validate"] | //button[text()="Valider"] | //button[text()="Confirm"]')
                to_validate.click()
                time.sleep(5)
            except:
                next_page = False
                # Click on To end if present
                wait_for_element(driver, '//font[text()="To end"] | //button[text()="Terminer"] | //button[text()="Finish"]')

                # wait to log for the form
                time.sleep(form_wait * 60)

                to_end = driver.find_element_by_xpath(
                    '//font[text()="To end"] | //button[text()="Terminer"] | //button[text()="Finish"]')
                to_end.click()
                time.sleep(5)

        # Go back to list
        wait_for_element(driver, '//font[text()="back to the list"] | //span[text()="Retour à la liste"] | //span[text()="Back to the list"]')

        back_btn = driver.find_element_by_xpath('//font[text()="back to the list"] | //span[text()="Retour à la liste"] | //span[text()="Back to the list"]')
        back_btn.click()

        wait_for_element(driver, '//button[text()="Relancer"] | //button[text()="Lancer"] | //font[text()="To throw"] | //font[text()="To restart"] | //button[text()="Try again"] | //button[text()="Continue"]')

        i += 1

    driver.quit()


if __name__ == "__main__":
    p = mp.Process(target=main)
    p.start()
    p.join()
