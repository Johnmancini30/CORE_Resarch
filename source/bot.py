import time
import pyautogui
import clipboard

"""
bot.py: A bot to help me automate the process of running experiements in CORE. All pixel based, so would not work from computer to computer
You can set the pixel values yourself though

"""



#traffic flow menu
menu_pixel = (850, 296) #corresponds to the traffic flow in the traffic flow menu
start_pixel = (1055, 618) #corresponds to the start selected traffic flow button in the traffic flow menu
stop_pixel = (1153, 620) #corresponds to the stop selected traffic flow button in the traffic flow menu
gear_pixel = (794, 495) #corresponds to the wrench for editing traffic flows in the traffic flow menu


pattern_pixel = (282, 297) #corresponds to the place where you can input a pattern type in the edit traffic flow menu
log_pixel = (572, 259) #corresponds to the place where you can input a log file destination in the edit traffic flow menu
time_pixel = (627, 122) #corresponds ot the stop time box in the edit traffic flow menu
apply_pixel = (376, 408) #corresponds to the apply button in the edit traffic flow menu


pattern = "PERIODIC [" #specifies if the pattern will be periodic or poisson
packets_sent = 20 #specifies the number of packets to be sent per flow
num_runs = 2 #specifies the number of flows per parameter

file_name = "/home/jm/Desktop/data/data" #data is the directory it will go in, then each sub directory will be called data0, data1, ... , data12 where datai holds the traffic flows with parameter ins[i]
ins = {0: 5, 1:10} #corresponds to the interarrival rate in a given flow


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
        click(menu_pixel)
        click(gear_pixel, .5)

        new_file_name = file_name + "traffic" + str(i) + ".log"
        copy_and_paste(new_file_name, log_pixel)

        click(apply_pixel, .5)

        click(menu_pixel)

        click(start_pixel, run_time + 2)
        click(stop_pixel, 2)


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
        file_to_write = file_name + str(key) + "/"

        click(menu_pixel)
        click(gear_pixel, .5)

        pattern_to_write = pattern + str(ins[key]) + " 1000]"
        copy_and_paste(pattern_to_write, pattern_pixel)

        time_to_write = round(packets_sent / ins[key], 1)
        copy_and_paste(time_to_write, time_pixel)

        click(apply_pixel, .5)

        bot(file_to_write, time_to_write)


if __name__ == '__main__':
    run_all(ins, file_name)


