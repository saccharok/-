import Commands
import pandas as pd
data = []

def get_data():
    global data
    device_management = 'device_management.xlsx'
    xl = pd.ExcelFile(device_management)
    df = xl.parse('Лист1')
    data = df.values

def gesture_management(gesture):
    global data
    df = pd.DataFrame(data, columns=['First', 'Second', 'Third'])
    return df[df['First'] == gesture]

def operation_management(line):
    command = any(line['Second'] == 'open_web_page')
    if command:
        link = line['Third'].values[0]
        Commands.open_web_page(link)
    command = any(line['Second'] == 'microfon_enabled')
    if command:
        Commands.microfon_enabled()
    command = any(line['Second'] == 'brightness_up')
    if command:
        Commands.brightness_up()
    command = any(line['Second'] == 'brightness_down')
    if command:
        Commands.brightness_down()  
    command = any(line['Second'] == 'volume_up')
    if command:
        Commands.volume_up()    
    command = any(line['Second'] == 'volume_down')
    if command:
        Commands.volume_down()    
    command = any(line['Second'] == 'run_word')
    if command:
        Commands.run_word()     
    command = any(line['Second'] == 'run_open_office')
    if command:
        Commands.run_open_office()      
    command = any(line['Second'] == 'volume_max')
    if command:
        Commands.volume_max()       
    command = any(line['Second'] == 'volume_min')
    if command:
        Commands.volume_min()   

def management(gesture):
    get_data()
    line = gesture_management(gesture)
    operation_management(line)