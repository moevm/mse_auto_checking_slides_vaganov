from app.parser.pptx.slide_pptx import SlidePPTX
from pptx import Presentation
from app.parser.presentation_basic import PresentationBasic


class PresentationPPTX(PresentationBasic):
    def __init__(self, presentation_name):
        PresentationBasic.__init__(self, presentation_name)
        self.prs = Presentation(presentation_name)
        self.add_slides()

    def add_slides(self):
        for slide in self.prs.slides:
            self.slides.append(SlidePPTX(slide))