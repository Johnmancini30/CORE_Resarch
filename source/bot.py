import time
import pyautogui
import clipboard


"""
bot.py: A bot to help me automate the process of running experiements in CORE. All pixel based, so would not work from computer to computer
You can set the pixel values yourself though\

"""


"""
this runs the bot.
 
:param tuple menu_pixel: pixel coordinate of traffic flow in menu
:param tuple start_pixel: pixel coordinate of start traffic flow button
:param tuple stop_pixel: pixel coordinate of stop traffic flow button
:param tuple gear_pixel: pixel coordinate of gear
:param tuple log_pixel: 
:param tuple apply_pixel: 
:param int num_runs: number of runs
:param string file_name: name of file to write to
"""
def bot(menu_pixel, start_pixel, stop_pixel, gear_pixel, log_pixel, apply_pixel, num_runs, file_name, run_time):
    for i in range(num_runs):
        pyautogui.click(menu_pixel[0], menu_pixel[1])


        pyautogui.click(gear_pixel[0], gear_pixel[1])
        time.sleep(.5)
        pyautogui.click(log_pixel[0], log_pixel[1], clicks=3)
        pyautogui.press("backspace")

        new_file_name = file_name + "traffic" + str(i) + ".log"
        clipboard.copy(new_file_name)
        time.sleep(.5)

        pyautogui.keyDown('ctrl')
        pyautogui.keyDown('v')
        pyautogui.keyUp('ctrl')
        pyautogui.keyUp('v')

        pyautogui.click(apply_pixel[0], apply_pixel[1])
        time.sleep(.5)

        pyautogui.click(menu_pixel[0], menu_pixel[1])

        pyautogui.click(start_pixel[0], stop_pixel[1])
        time.sleep(run_time + 2)
        pyautogui.click(stop_pixel[0], stop_pixel[1])




def run_all(ins, file_name):
    menu_pixel = (801, 300)
    start_pixel = (1042, 613)
    stop_pixel = (1142, 611)
    gear_pixel = (793, 499)
    log_pixel = (532, 280)
    apply_pixel = (394, 425)
    pattern_pixel = (306, 320)
    time_pixel = (646, 142)
    pattern = "POISSON ["

    packets_sent = 100
    num_runs = 5

    time.sleep(5)
    for key in ins.keys():
        file_to_write = file_name + str(key) + "/"
        pyautogui.click(menu_pixel[0], menu_pixel[1])
        pyautogui.click(menu_pixel[0], menu_pixel[1])
        pyautogui.click(gear_pixel[0], gear_pixel[1])
        time.sleep(.5)

        pattern_to_write = pattern + str(ins[key]) + " 1000]"
        clipboard.copy(pattern_to_write)

        time.sleep(.5)
        pyautogui.click(pattern_pixel[0], pattern_pixel[1], clicks=3)
        pyautogui.press("backspace")
        pyautogui.keyDown('ctrl')
        pyautogui.keyDown('v')
        pyautogui.keyUp('ctrl')
        pyautogui.keyUp('v')

        time_to_write = round(packets_sent/ins[key], 1)
        clipboard.copy(str(time_to_write))
        time.sleep(.5)

        pyautogui.click(time_pixel[0], time_pixel[1], clicks=3)
        pyautogui.press("backspace")
        pyautogui.keyDown('ctrl')
        pyautogui.keyDown('v')
        pyautogui.keyUp('ctrl')
        pyautogui.keyUp('v')

        pyautogui.click(apply_pixel[0], apply_pixel[1])
        time.sleep(.5)


        bot(menu_pixel, start_pixel, stop_pixel, gear_pixel, log_pixel, apply_pixel, num_runs, file_to_write, time_to_write)



if __name__=='__main__':
    f = "/home/jm/Desktop/CORE_Research/data3/data"

    ins = {0:.3, 1:.5, 2: 1.0, 3:2.0, 4:3.0, 5:4.0, 6:5.0, 7:6.0, 8:7.0, 9:8.0, 10:9.0, 11:9.5, 12:9.7}
    run_all(ins, f)


