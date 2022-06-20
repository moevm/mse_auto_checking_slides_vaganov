import re
from ..base_check import BaseCheck, answer


class ReportBannedWordsCheck(BaseCheck):
    def __init__(self, file, words, min_count, max_count):
        super().__init__(file)
        self.words = [word.lower() for word in words]
        self.min_count = min_count
        self.max_count = max_count

    def check(self):
        parsed_pdf = self.file.get_parsed_pdf()
        text = parsed_pdf.get_text_on_page().items()
        result_str = ''
        count = 0
        for k, v in text:
            lines_on_page = re.split(r'\n', v)
            # words_on_page = re.split(r'[^\w-]+', v)
            # words_on_page = list(map(str.lower, words_on_page))
            # for word in self.words:
            #     if word in words_on_page:
            #         count += 1
            #         result_str += f'Страница №{k}: слово - {word}. \n'
            for line in lines_on_page:
                words_on_line = re.split(r'[^\w-]+', line)
                words_on_line = list(map(str.lower, words_on_line))
                for word in self.words:
                    if word in words_on_line:
                        count += 1
                        result_str += f'Страница №{k}: {line}. \n'

        result_score = 1
        if count > self.min_count:
            if count <= self.max_count:
                result_score = 0.5
            else:
                result_score = 0
        return answer(True, result_str)