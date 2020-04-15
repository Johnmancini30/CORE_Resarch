import time
import pyautogui
import clipboard

menu_pixel = (801, 300)
start_pixel = (1042, 613)
stop_pixel = (1142, 611)
gear_pixel = (793, 499)
close_traffic = (1215, 244)


log_pixel = (645, 261)
apply_pixel = (374, 406)
pattern_pixel = (318, 297)
time_pixel = (625, 117)



start_net = (85, 143)
stop_net = (84, 143)
traffic_menu = (269, 73)
traffic = (286, 205)


pattern = "PERIODIC ["
packets_sent = 100
num_runs = 5

"""
bot.py: A bot to help me automate the process of running experiements in CORE. All pixel based, so would not work from computer to computer
You can set the pixel values yourself though

"""

"""
clicks

:param tuple pixel: pixel to click
:param float time_to_wait:
"""


def click(pixel, time_to_wait=0.0):
    pyautogui.click(pixel[0], pixel[1])
    time.sleep(time_to_wait)


"""
this runs the bot.

:param string file_name: name of file to write to
:param float run_time: time to run each traffic flow
"""


def bot(file_name, run_time):
    for i in range(num_runs):
        #start_virtual_net()

        open_traffic_menu()
        click(menu_pixel)
        click(gear_pixel, .5)

        new_file_name = file_name + "traffic" + str(i) + ".log"
        copy_and_paste(new_file_name, log_pixel)

        click(apply_pixel, .5)

        click(menu_pixel)

        click(start_pixel, run_time + 2)
        click(stop_pixel, 2)
        click(close_traffic, .5)

        #click(stop_net, 10)


"""
starts the virtual network
"""
def start_virtual_net():
    click(start_net, 30.0)


def open_traffic_menu():
    time.sleep(.5)
    click(traffic_menu)
    time.sleep(.5)
    click(traffic)


"""
copy and pastes

:param string copy_str:
:param tuple pixel:
"""
def copy_and_paste(copy_str, pixel):
    clipboard.copy(copy_str)
    time.sleep(.5)
    pyautogui.click(pixel[0], pixel[1], clicks=3)
    pyautogui.press("backspace")
    pyautogui.keyDown('ctrl')
    pyautogui.keyDown('v')
    pyautogui.keyUp('ctrl')
    pyautogui.keyUp('v')


def run_all(ins, file_name):
    time.sleep(5)

    for key in ins.keys():
        open_traffic_menu()
        file_to_write = file_name + str(key) + "/"

        click(menu_pixel)
        click(gear_pixel, .5)

        pattern_to_write = pattern + str(ins[key]) + " 1000]"
        copy_and_paste(pattern_to_write, pattern_pixel)

        time_to_write = round(packets_sent / ins[key], 1)
        copy_and_paste(time_to_write, time_pixel)

        click(apply_pixel, .5)
        click(close_traffic, .5)

        bot(file_to_write, time_to_write)


if __name__ == '__main__':
    f = "/home/jm/Desktop/CORE_Research/data/periodic/data"
    ins = {0:.3, 1: .5, 2: 1.0, 3: 2.0, 4: 3.0, 5: 4.0, 6: 5.0, 7: 6.0, 8: 7.0, 9: 8.0, 10: 9.0, 11: 9.5, 12: 9.7}
    run_all(ins, f)


