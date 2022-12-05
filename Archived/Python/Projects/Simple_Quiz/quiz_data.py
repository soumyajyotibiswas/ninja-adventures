from urllib.request import urlopen
import json

class QuizData:
    def __init__(self,num_of_questions) -> None:
        self.num_of_questions = self._is_valid_number(num_of_questions)

    def _is_valid_number(self,num_of_questions):
        if num_of_questions > 100 or num_of_questions < 5:
            raise ValueError("The number of questions has to be between 5 and 100. Try again!")
        return num_of_questions

    def get_questions(self):
        url = f"https://opentdb.com/api.php?amount={self.num_of_questions}&type=boolean"
        response = urlopen(url)
        data_json = json.loads(response.read())
        response.close()
        return data_json['results']
