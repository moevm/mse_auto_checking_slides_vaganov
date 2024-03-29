from ..base_check import answer, BasePresCriterion


class FindDefSld(BasePresCriterion):
    description = "Поиск ключевого слова в заголовках"
    id = 'find_slides'

    def __init__(self, file_info, key_slide):
        super().__init__(file_info)
        self.type_of_slide = key_slide
        self.found_idxs = []

    def check(self):
        found_slides = []
        for i, title in enumerate(self.file.get_titles(), 1):
            if str(title).lower().find(str(self.type_of_slide).lower()) != -1:
                found_slides.append(self.file.get_text_from_slides()[i - 1])
                self.found_idxs.append(i)
        if len(found_slides) == 0:
            self.file.found_index[str(self.type_of_slide)] = None
            return answer(False, 'Слайд не найден')
        else:
            self.file.found_index[str(self.type_of_slide)] = ''.join(str(item) for item in self.found_idxs)
            found_idxs_link = self.format_page_link(self.found_idxs)
            return answer(True, 'Найден под номером: {}'.format(', '.join(map(str, found_idxs_link))))

    @property
    def name(self):
        return f"Слайд: '{self.type_of_slide}'"
