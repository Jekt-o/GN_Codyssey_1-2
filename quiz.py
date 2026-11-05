
class Quiz:
    def __init__(self, question, choices, answer):
        self.question = question
        self.choices = choices
        self.answer = answer

    def show(self):
        print("\n" + self.question)

        for i in range(4):
            print(f"{i + 1}. {self.choices[i]}")

    def check_answer(self, user_answer):
        return self.answer == user_answer
