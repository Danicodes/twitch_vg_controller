import os,sys,re
import time
import signal
import windowfocus as focus
import vgamepad as vg
import vgamepad.win.vigem_commons as vcom
import vgamepad.win.vigem_client as vcli
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
    def __init__(self):
        self.gamepad = vg.VX360Gamepad()

        # Not used yet
        self.L = self.gamepad.left_joystick_float
        self.R = self.gamepad.right_joystick_float



    """
    ------------------------------
    Helper functions
    ------------------------------
    """
    def stall(self):
        time.sleep(5)
        return

    def update(self, delay=None):
        self.gamepad.update()
        if not delay:
            time.sleep(0.25) # 0.25 second delay by default
        else:
            time.sleep(delay)

        return

    def reset(self):
        self.gamepad.reset()
        self.update()
        return

    """
    ------------------------------
    Possible player actions to abstract

    press and release a button
    press and hold a button
    press and hold multiple buttons

    ------------------------------
    """
    def press_button(self, button: Button) -> None:
        self.gamepad.press_button(button)
        self.update()
        return

    def release_button(self, button: Button) -> None:
        self.gamepad.release_button(button)
        self.update()
        return

    def press_and_release(self, button: Button):
        """
        Press and release a Button (Enum Button class)
        Will press and release a button with .25s between the press and release

        Eg: User input ABA
        will press and release A then press and release B then A again
        """

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
    # # TODO: Not sure if self.L and self.R work
    def move_right(self, float=0.5, reset=0):
        self.L(x_value_float=float, y_value_float=0.0)
        self.update()
        # Time between reseting the joystick to 0
        self.sleep(reset)
        self.L(x_value_float=0.0, y_value_float=0.0)
        return

    def move_left(self, float=-0.5, reset=0):
        self.L(x_value_float=float, y_value_float=0)
        self.update()
        # Time between reseting the joystick to 0
        self.sleep(reset)
        self.L(x_value_float=0.0, y_value_float=0.0)

        return

    def move_up(self, float=0.5, reset=0):
        self.L(x_value_float=0.0, y_value_float=float)
        self.update()
        # Time between reseting the joystick to 0
        self.sleep(reset)
        self.L(x_value_float=0.0, y_value_float=0.0)
        return

    def move_down(self, float=-0.5, reset=0):
        self.L(x_value_float=0.0, y_value_float=float)
        self.update()
        # Time between reseting the joystick to 0
        self.sleep(reset)
        self.L(x_value_float=0.0, y_value_float=0.0)
        return

    """
    ------------------------------
    Parse player actions from the chat
    (Regex)

    Examples:

    Chaining actions to press one after the other:
    moveset: LRABBAXY

    Pressing multiple buttons at once:
    moveset: A+B

    Press and hold a button or the joystick:
    moveset: B. or B..
    (Let's say each '.' adds 0.25s of holding the button)

    ------------------------------
    """

    def parse_moveset(self, moveset: str):
        # wip:
        movestack = []

        multi_button_regex = r"\w[\+\w]{1,4}" # Press a max of 5 buttons altogether
        press_hold_regex = r"[\w\.+]{1,}"
        chained_regex = r"[\w]{1,}"

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

    def shutdown(self):
        _busp = self.gamepad._busp
        _devicep = self.gamepad._devicep
        vcli.vigem_target_remove(_busp, _devicep)
        vcli.vigem_target_free(_devicep)
        print("Shutting down")
        sys.exit(0)

def signal_handler(vgobj, sig, frame):
    vgobj.shutdown()
    return

if __name__ == '__main__':


    #signal.signal(c, signal.SIGINT, signal_handler)

    focus.focus_window('Mortal Kombat 11')
    print("Waiting for an unpause")
    time.sleep(5)
    c = Controller('dani')
    #print("Unpausing hopefully!!!")
    #c.press_and_release(vg.XUSB_BUTTON.XUSB_GAMEPAD_GUIDE) # Unpause
    #c.update()
    #time.sleep(3)
    print("Move left")
    c.move_left()
    c.update()
    time.sleep(2)
    c.reset()
    print("Parse moves")
    c.parse_moveset("DUABRRRRABABABARRBBAABABABAAB")
    print("Waiting for shutdown")
    time.sleep(30)
    c.shutdown()
