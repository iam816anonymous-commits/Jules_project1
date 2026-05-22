from jarvis.vision.capture import ScreenCapture
from jarvis.vision.ocr import OCR
from jarvis.vision.ui_tree import UITree

class VisionObserver:
    def __init__(self):
        self.capture = ScreenCapture()
        self.ocr = OCR()
        self.ui_tree = UITree()

    def observe(self):
        image = self.capture.capture()
        text = self.ocr.extract_text(image)
        tree = self.ui_tree.build(text)
        return {"raw_text": text, "ui_tree": tree}
