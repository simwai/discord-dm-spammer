#!/usr/bin/env Python3
import PySimpleGUI as sg
import queue
import threading
import settings
import spammer

def long_operation_thread():
    spammer.start_spam()


# The UI
def the_gui():
    # sets theme
    sg.ChangeLookAndFeel('DarkBlue9')
    gui_queue = queue.Queue()

    # Output Console
    output = [
        [sg.Frame(layout=[
            [sg.Output(size=(42, 8), pad=(0, 0))],
        ], title='Output', title_color="#ffffff")], ]

    # Main Layout
    layout = [
        [sg.Frame(layout=[
            [sg.Text('Friend Names (separator = ;):', size=(17, 1), font=("Roboto", 8)),
             sg.Multiline('', key="friend_names", size=(24, 5)), ],
            # TODO add target servers
            # [sg.Text('Target servers (invite links):', size=(17, 1), font=("Roboto", 8)),
            #  sg.Multiline('', key="target_servers", size=(24, 5)), ],
            [sg.Text('Username/Email:', size=(17, 1), font=("Roboto", 8)),
             sg.InputText('', key="username_email", size=(27, 1))],
            [sg.Text('Password:', size=(17, 1), font=("Roboto", 8)),
             sg.InputText('', key="password", password_char='*', size=(27, 1))],
            [sg.Text('Delay (seconds):', size=(17, 1), font=("Roboto", 8)),
             sg.Spin(values=('0', '.5', '1','1.5','2','2.5','3'), key="delay", initial_value='1', size=(6, 1), tooltip="wait time between messages")],
        ],
            title='Login', title_color="#ffffff"), sg.Column(output)],

        [sg.Frame(layout=[
            [sg.Multiline(default_text='Paste any block of text here and this is what will be sent word for word', size=(91, 10), key='user_text')],
            [sg.Checkbox('Use Shrek movie script instead', default=False, key="shrek_script")],
            [sg.Text("Number of iterations:" ,size=(17,1),font=("Roboto",10)),
            sg.Spin([i for i in range(1,1000)],size=(6, 1),key="iterations",initial_value=1,tooltip="How many times would you like to iterate")],
        ],title='Your Text', title_color="#ffffff")],

        [sg.Button('Run', size=(10, 1), key="Run"), sg.Button('Exit', size=(10, 1))]

    ]
    # Window options
    window = sg.Window('Discord DM Spammer', layout, default_element_size=(40, 1), grab_anywhere=False,
                       location=(5, 5))

    while True:
        event, values = window.read(timeout=1000)
        window['username_email'].update(disabled=False)
        window['password'].update(disabled=False)
        if values['shrek_script']:
            window['user_text'].update(disabled=True)
        else:
            window['user_text'].update(disabled=False)

        # If exit button is clicked
        if event in (None, 'Exit'):
            break
        # If run button is clicked
        elif event == 'Run':
            window['Run'].update(disabled=True)
            settings.password = values['password']
            settings.username_email = values['username_email']
            settings.friend_names = values['friend_names'].split(';')
            settings.delay = values['delay']
            settings.iterations = values['iterations']
            if values['shrek_script']:
                settings.script = "shrek.txt"
            else:
                settings.script = "script.txt"
            with open('script.txt', 'w') as f:
                f.write(values['user_text'])

            # Calls the long_operation_thread
            try:
                threading.Thread(target=long_operation_thread,
                                 args=(), daemon=True).start()
            except Exception as e:
                print('Error')

        # Checks for incoming messages from threads
        try:
            # get_nowait() will get exception when Queue is empty
            message = gui_queue.get_nowait()
        except queue.Empty:
            # break from the loop if no more messages are queued up
            message = None
        # if message received from queue, display the message in the Window
        if message:
            print('Got a message back from the thread: ', message)

    # if user exits the window, then close the window and exit the GUI
    window.close()


if __name__ == '__main__':
    the_gui()
    print('Exiting Program')
