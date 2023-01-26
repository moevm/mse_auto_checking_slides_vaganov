from ..base_check import BaseReportCriterion, answer


class ReportIntroduction(BaseReportCriterion):
    description = "Проверка наличия нужных слов во введении"
    id = 'intro'

    def __init__(self, file_info):
        super().__init__(file_info)
        self.intro = {}
        self.patterns = ["Цель", "Задачи", "Объект", "Предмет", "Практическая ценность работы"]

    def check(self):
        for intro in self.file.chapters:
            if intro["text"] == 'ВВЕДЕНИЕ':
                self.intro = intro
                break
        for intro_par in self.intro["child"]:
            for pattern in self.patterns:
                if intro_par["text"].lower().find(pattern.lower()) >= 0:
                    self.patterns.remove(pattern)

        result_score = 0
        if len(self.patterns) == 0:
            result_score = 1
        if result_score:
            return answer(result_score, "Все нужные слова обнаружены в тексте введения!")
        else:
            result_str = '</li><li>'.join([k for k in self.patterns])
            return answer(result_score,
                          f'Не найдены следующие слова: <ul><li>{result_str}</ul>')