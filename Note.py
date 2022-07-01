from selenium.webdriver.common.by import By


class Checkbox():

    def __init__(self):
        self.question = ""
        self.extra = ""
        self.RightAnswers = []
        self.FalseAnswers = []

    def setQuestion(self, question):
        self.question = question

    def addAnswer(self, SeleniumObject):

        if(SeleniumObject.get_attribute("class")=='answer'):
            self.FalseAnswers.append(SeleniumObject.text)
        else:
            self.RightAnswers.append(SeleniumObject.text)

    def setExtra(self, Extra):
        self.extra = Extra

    def print(self):
        print (f"Q:{self.question}")
        for a in self.RightAnswers:
            print(f"Right Answer: {a}")

        for a in self.FalseAnswers:
            print(f"False Answer: {a}")

#TODO Should be redundant already, remove for Checkbox Class
class Selectable():

    def __init__(self):
        self.question = ""
        self.extra = ""
        self.RightAnswers = []
        self.FalseAnswers = []

    def setQuestion(self, question):
        self.question = question

    def addAnswer(self, SeleniumObject):
        classes = SeleniumObject.get_attribute("class")
        if classes == 'answer correct':
            self.RightAnswers.append(SeleniumObject.text)
        elif classes == 'answer missing':
            self.RightAnswers.append(SeleniumObject.text)
        else:
            self.FalseAnswers.append(SeleniumObject.text)

    def setExtra(self, Extra):
        self.extra = Extra

    def print(self):
        print(f"Q:{self.question}")
        for a in self.RightAnswers:
            print(f"Right Answer: {a}")

        for a in self.FalseAnswers:
            print(f"False Answer: {a}")


class Cloze():

    def __init__(self, SeleniumObject):
        self.clozeText = ""
        self.extra = ""
        htmlText = SeleniumObject.find_element(By.TAG_NAME, 'p').get_attribute('innerHTML')
        clean = htmlText.replace('\n', '').replace('<span class="fill-in-wrapper missing">', '').replace(
        '<span class="fill-in-editable answer-part">', '').replace("  ", '').replace('</span>', '').strip()
        clean = clean.replace('<i>', '{{c1::').replace('</i>', '}}')
        self.clozeText = clean
        print(f"Clozetext: {clean}")




    def setText(self, text):
        self.clozeText = text

    def setExtra(self, Extra):
        self.extra = Extra

    def print(self):
        print(f"Clozetext: {self.clozeText}")
