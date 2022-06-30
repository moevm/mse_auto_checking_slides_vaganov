from ..base_check import BaseReportCriterion, answer


class ReportSimpleCheck(BaseReportCriterion):
    description = "Простая проверка на пустоту файла"
    id = 'simple_check'

    def __init__(self, file_info):
        super().__init__(file_info)

    def check(self):
        if self.file.paragraphs:
            return answer(True, "Пройдена!")
        else:
            return answer(False, f'Количество paragraphs в файле = 0')

    @property
    def name(self):
        return description
