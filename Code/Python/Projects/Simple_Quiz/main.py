from quiz_question import QuizQuestion
from quiz_brain import QuizBrain
from quiz_data import QuizData

quiz_data=QuizData(int(input("Enter how many questions you want to face. The number of questions can be between 5 and 100. [eg: 5] --> ")))
questions=quiz_data.get_questions()
question_bank=[]
for item in questions:
    question_bank.append(QuizQuestion(item["question"],item["correct_answer"],item["category"],item["difficulty"]))
quiz = QuizBrain(question_bank)
while(quiz.still_has_questions()):
    quiz.next_question()
print(f"\nYour final score was {quiz.score}/{len(question_bank)}")
