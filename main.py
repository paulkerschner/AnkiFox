# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import pickle
import time

from genanki import Note, Deck, Package
from selenium import webdriver
from selenium.common import WebDriverException, NoSuchElementException
from selenium.webdriver.common.by import By

from ModelDescribtions import MY_AllInOne_MODEL, MY_CLOZE_MODEL
from Note import Cloze, Selectable, Checkbox


def saveToAnkiDeck(clozeCards, checkBoxCards, selectableCards):
    notes = []

    print(f"Count of Cards to translate: {len(checkBoxCards) + len(clozeCards) + len(selectableCards)}")

    for clozeCard in clozeCards:
        fields = [clozeCard.clozeText, clozeCard.extra]
        tempNote = Note(model=MY_CLOZE_MODEL, fields=fields)
        notes.append(tempNote)

    for checkBoxCard in checkBoxCards:
        # Turn My Style in AllInOne
        Q = ["", "", "", "", ""]
        index = 0
        AnswerCard = ""

        for rightAnswer in checkBoxCard.RightAnswers:
            Q[index] = rightAnswer
            AnswerCard += "1 "
            index += 1
        for falseAnswer in checkBoxCard.FalseAnswers:
            Q[index] = falseAnswer
            AnswerCard += "0 "
            index += 1

        fields = [checkBoxCard.question, checkBoxCard.question, '1', Q[0], Q[1], Q[2], Q[3], Q[4], AnswerCard,
                  "KnowledgeFox", checkBoxCard.extra]
        tempNote = Note(model=MY_AllInOne_MODEL, fields=fields)
        notes.append(tempNote)

    for selectableCard in selectableCards:
        # Turn My Style in AllInOne
        Q = ["", "", "", "", ""]
        index = 0
        AnswerCard = ""

        print(f"Anzahl der antworten: {len(selectableCard.RightAnswers) + len(selectableCard.FalseAnswers)}")

        while True:
            anzahl = len(selectableCard.RightAnswers) + len(selectableCard.FalseAnswers)
            if (anzahl > 5):
                selectableCard.FalseAnswers.pop()
            else:
                break

        for rightAnswer in selectableCard.RightAnswers:
            Q[index] = rightAnswer
            AnswerCard += "1 "
            index += 1
        for falseAnswer in selectableCard.FalseAnswers:
            Q[index] = falseAnswer
            AnswerCard += "0 "
            index += 1

        fields = [selectableCard.question, selectableCard.question, '1', Q[0], Q[1], Q[2], Q[3], Q[4], AnswerCard,
                  "KnowledgeFox", selectableCard.extra]
        tempNote = Note(model=MY_AllInOne_MODEL, fields=fields)
        notes.append(tempNote)

    """Write cloze cards to an Anki apkg file"""
    deckname = 'AnkiFoxExport'
    deck = Deck(deck_id=3759375, name=deckname)
    for note in notes:
        deck.add_note(note)
    fout_anki = '{NAME}.apkg'.format(NAME=deckname)
    Package(deck).write_to_file(fout_anki)
    print('  {N} Notes WROTE: {APKG}'.format(N=len(notes), APKG=fout_anki))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    driver = None
    startURL = 'https://mlearning.medunigraz.at/KnowledgePulse/client/'
    setting = True

    try:
        with open("driver.txt", "r") as f:
            URL = f.readline().rstrip()
            ID = f.readline().rstrip()
    except FileNotFoundError:
        print("No Settings Found")
        setting = False

    if setting:
        try:
            driver = webdriver.Remote(command_executor=URL)
            driver.close()
            driver.session_id = ID
            driver.set_page_load_timeout(30)
        except Exception:

            print("Existing Instance not connectable")

    try:
        print(driver.session_id)
        # driver.get(startURL)
        print("Reusing old Instance")
        time.sleep(1)
    except (WebDriverException, AttributeError):
        print("Starting new Instance")
        driver = webdriver.Chrome()
        print(f"Executor: {driver.command_executor._url} Session_id: {driver.session_id}")
        driver.get(startURL)
        f = open("driver.txt", 'w')
        f.write(driver.command_executor._url)
        f.write('\n')
        f.write(driver.session_id)
        f.close()

    clozeCards = []
    selectableCards = []
    checkBoxCards = []

    while True:

        print("Are you on the index Page of your course?")
        if input("y = Yes, q = Quit:") == "q":
            break

        # Load all Links to the individual cards
        cardLinks = []
        indexlessons = driver.find_elements(By.CLASS_NAME, 'indexlesson')
        for index in indexlessons:
            cardObjects = index.find_elements(By.CLASS_NAME, 'indexcard')
            for cardObject in cardObjects:
                cardLinks.append(cardObject.get_attribute('href'))

        print(f"{len(cardLinks)} Links found")

        for link in cardLinks:

            driver.get(link)
            # Sometimes JS needs sonme time
            time.sleep(0.1)
            q = driver.find_element(By.CLASS_NAME, "question").text
            print(q)

            try:
                driver.find_element(By.CLASS_NAME, 'fill-in')
                print("Fill-In")

                # Try Choose

                driver.find_element(By.XPATH, '/html/body/div[5]/div/div/div/div[2]/a').click()

                seleniumObject = driver.find_element(By.CLASS_NAME, 'fill-in')
                temp = Cloze(seleniumObject)

                try:
                    temp.setExtra(driver.find_element(By.CLASS_NAME, 'context_text').text)
                except NoSuchElementException:
                    print("No Extra")
                clozeCards.append(temp)


            except NoSuchElementException:
                try:
                    driver.find_element(By.CLASS_NAME, 'checkbox')

                    print('Checkbox')
                    temp = Checkbox()
                    # Checkbox
                    driver.find_element(By.XPATH, '/html/body/div[5]/div/div/div/div[2]/a').click()

                    question = driver.find_element(By.CLASS_NAME, "question")
                    temp.setQuestion(question.text)
                    answers = driver.find_elements(By.CLASS_NAME, "answer")

                    extra = driver.find_element(By.CLASS_NAME, "answer_context")
                    for a in answers:
                        temp.addAnswer(a)

                    try:
                        temp.setExtra(driver.find_element(By.CLASS_NAME, 'context_text').text)
                    except NoSuchElementException:
                        print("No Extra")

                    checkBoxCards.append(temp)


                except NoSuchElementException:

                    try:
                        print("Selectable")
                        temp = Selectable()
                        # Choose one first
                        driver.find_element(By.CLASS_NAME, 'answer').click()
                        driver.find_element(By.XPATH, '/html/body/div[5]/div/div/div/div[2]/a').click()

                        question = driver.find_element(By.CLASS_NAME, "question")
                        temp.setQuestion(question.text)
                        answers = driver.find_elements(By.CLASS_NAME, "answer")
                        for a in answers:
                            temp.addAnswer(a)
                        try:
                            temp.setExtra(driver.find_element(By.CLASS_NAME, 'context_text').text)
                        except NoSuchElementException:
                            print("No Extra")
                        selectableCards.append(temp)
                    except NoSuchElementException:
                        # Final Error Handling, sometimes for empty card from KF
                        input("Something went wrong, please correct or check, Enter for next card")
            finally:
                #Return to start page, might be problem for debugging
                driver.get(startURL)

    # Finished Card collection, saving to Anki an pickle Backup
    print(f"Overview: Cloze:{len(clozeCards)}, Selectable:{len(selectableCards)}, CheckBox:{len(checkBoxCards)}")

    try:
        saveToAnkiDeck(clozeCards, checkBoxCards, selectableCards)
    finally:
        if len(clozeCards) + len(selectableCards) + len(checkBoxCards) > 0:
            file_to_store = open("ClozeObjects.pickle", "wb")
            pickle.dump(clozeCards, file_to_store)
            file_to_store.close()

            file_to_store = open("SelectableObjects.pickle", "wb")
            pickle.dump(selectableCards, file_to_store)
            file_to_store.close()

            file_to_store = open("CheckBoxObjects.pickle", "wb")
            pickle.dump(checkBoxCards, file_to_store)
            file_to_store.close()

            print("Saved to files")

    exit(0)
