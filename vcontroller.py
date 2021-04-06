import os,sys,re
import time
import signal
import windowfocus as focus
import vgamepad as vg
from enum import Enum

class Menu(Enum):
    # Should not be accessed by chat
    START = vg.XUSB_BUTTON.XUSB_GAMEPAD_START
    BACK = vg.XUSB_BUTTON.XUSB_GAMEPAD_BACK
    XBOX = vg.XUSB_BUTTON.XUSB_GAMEPAD_GUIDE

class Button(Enum):
    # buttons that will be used in a press and release
    # or a press and hold scenario
    LS = vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER
    RS = vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER

    # Direction
    D_U = vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP
    D_D = vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN
    D_L = vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT
    D_R = vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT

    # Standard Buttons
    A = vg.XUSB_BUTTON.XUSB_GAMEPAD_A
    B = vg.XUSB_BUTTON.XUSB_GAMEPAD_B
    X = vg.XUSB_BUTTON.XUSB_GAMEPAD_X
    Y = vg.XUSB_BUTTON.XUSB_GAMEPAD_Y

class Joystick(Enum):
    # Only dealing with left joystick
    pass
    #L = vg.left_joystick_float
    #R = vg.right_joystick_float
    #LT = vg.left_trigger_float
    #RT = vg.right_trigger_float


class Controller:
    def __init__(self, player=None):
        self.gamepad = vg.VX360Gamepad()
        self.name = player

        self.L = self.gamepad.left_joystick_float

    # Helper functions
    def stall(self):
        time.sleep(5)
        return

    def update(self):
        time.sleep(1)
        self.gamepad.update()
        return

    def reset(self):
        self.gamepad.reset()
        self.update()
        return

    # Player options
    def press_button(self, button: Button) -> None:
        self.gamepad.press_button(button)
        time.sleep(1)
        self.update()
        return

    def release_button(self, button: Button) -> None:
        self.gamepad.release_button(button)
        time.sleep(1)
        self.update()
        return

    def press_and_release(self, button: Button):
        """
        Press and release a Button (Enum Button class)
        User input ABA
        will press and release A then press and release B then A again
        """
        # TODO: Remove the stall/figure out how to detect that I'm in Steam
        self.press_button(button)
        self.release_button(button)
        return

    def press_multi(self, buttons):
        # max handle max input
        for button in buttons:
            self.press_button(button)

        time.sleep(2)
        self.reset()
        return

    # Joystick functions
    def move_left(self, float=0.5):
        self.gamepad.left_joystick_float(x_value_float=float, y_value_float=0.0)
        self.update()
        return

    def move_right(self, float=-0.5):
        self.gamepad.left_joystick_float(x_value_float=float, y_value_float=0.0)
        self.update()
        return

    def move_up(self, float=0.5):
        self.gamepad.left_joystick_float(x_value_float=0.0, y_value_float=float)
        self.update()
        return

    def move_down(self, float=-0.5):
        self.gamepad.left_joystick_float(x_value_float=0.0, y_value_float=float)
        self.update()
        return

    def parse_moveset(self, moveset: str):
        for movechar in moveset:
            if movechar == 'L':
                self.move_left()
            elif movechar == 'R':
                self.move_right()
            elif movechar == 'U':
                self.move_up()
            elif movechar == 'D':
                self.move_down()

            if movechar == 'A':
                self.press_and_release(vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
            elif movechar == 'B':
                self.press_and_release(vg.XUSB_BUTTON.XUSB_GAMEPAD_B)
            elif movechar == 'X':
                self.press_and_release(vg.XUSB_BUTTON.XUSB_GAMEPAD_X)
            elif movechar == 'Y':
                self.press_and_release(vg.XUSB_BUTTON.XUSB_GAMEPAD_Y)

        return

    def signal_handler(sig, frame):
        c.__del__()
        sys.exit(0)

if __name__ == '__main__':


signal.signal(signal.SIGINT, signal_handler)
    c = Controller('dani')
    time.sleep(1)

    focus.focus_window('Mortal Kombat 11')
    time.sleep(1)

    print("Unpausing hopefully!!!")
    c.press_and_release(vg.XUSB_BUTTON.XUSB_GAMEPAD_BACK) # Unpause
    print("Stalling a bit!!!")
    print("Move left")
    c.gamepad.left_joystick_float(x_value_float=-1.0, y_value_float=0.0)
    c.stall()
    print("Parsing the moveset hopefully!!!")
    c.parse_moveset('LUUUUUUUAAABABABABABB')
