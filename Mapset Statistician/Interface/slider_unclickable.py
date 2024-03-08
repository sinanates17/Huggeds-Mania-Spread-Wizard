"""Contains class definition for SliderUnclickable"""

# pylint: disable=all
from PyQt5.QtWidgets import QSlider, QStyleOptionSlider, QStyle

class SliderUnclickable(QSlider):
    """A QSlider where you can't click the groove."""
    def mousePressEvent(self, event):
        opt = QStyleOptionSlider()
        self.initStyleOption(opt)
        pressedControl = self.style().hitTestComplexControl(QStyle.CC_Slider, opt, event.pos(), self)
        if pressedControl != QStyle.SC_SliderGroove:
            super(SliderUnclickable, self).mousePressEvent(event)