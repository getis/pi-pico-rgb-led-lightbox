# class to handle a collection of buttons

from Button import Button


class ButtonHandler:
    
    # buttons
    buttons = {
        'btn_menu': Button(22, 0),
        'btn_up': Button(21, 0),
        'btn_left': Button(20, 0),
        'btn_down': Button(19, 0),
        'btn_right': Button(18, 0),
        'btn_ok': Button(17, 0)
    }

    @classmethod
    def scanButtons(cls):
        for name, button in cls.buttons.items():
            button.scan()

