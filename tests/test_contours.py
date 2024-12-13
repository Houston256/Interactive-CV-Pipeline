import numpy as np

from src.layer.contours import FindContours


class TestFindContours:
    def setup_method(self):
        self.findContours = FindContours(np.zeros((10, 10)))

    def test_evaluate(self):
        for i in range(3):
            self.findContours.set_image(np.random.rand(500, 500))
            result = self.findContours.evaluate()
            assert isinstance(result, FindContours)

    def test_interact(self):
        result = self.findContours.interact()
        assert isinstance(result, FindContours)

    def test_class_str(self):
        result = str(self.findContours)
        assert isinstance(result, str)
