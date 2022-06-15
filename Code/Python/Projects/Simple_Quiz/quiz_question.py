class QuizQuestion():
    def __init__(self,text,answer,category,difficulty) -> None:
        self.text = self._clean_text(text)
        self.answer = answer
        self.category = category
        self.difficulty = difficulty
    
    def _clean_text(self,text):
        return(text.replace('&#039;s','').replace('&quot;',''))