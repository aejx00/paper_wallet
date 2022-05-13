import os
import io
import sys
import json
import base64
import logging
import PIL.Image
import argparse
import config
import generator
import pyminizip
import PySimpleGUI as sg

version = '1.1'


def load_wallet(file_path, file_pass):
    try:
        pyminizip.uncompress(file_path, file_pass, config.gen_path, 0)
    except Exception as e:
        sg.popup_error('please enter valid file/pass', e)
        return None
    with open(os.path.join(config.gen_path, 'wallet_details.json'), 'r') as infile:
        wallet_details = json.load(infile)
    new_size = 600, 600
    window['_W_TITLE_'].Update(visible=True)
    window['_ADR_'].Update(wallet_details["address"], visible=True)
    window['-IMAGE-'].update(data=convert_to_bytes(os.path.join(config.gen_path, 'wallet_card.png'), resize=new_size))
    window['_PASS_TITLE_'].Update(visible=True)
    window['_PASS_'].Update(visible=True)
    window['_EXP_'].Update(visible=True)
    window['_PRINT_'].Update(visible=True)
    return wallet_details


def generate_wallet(token):
    wallet_details = generator.create_wallet_card(token)
    with open(os.path.join(config.gen_path, 'wallet_details.json'), 'w') as outfile:
        outfile.write(json.dumps(wallet_details, indent=4))
    new_size = 600, 600
    window['_W_TITLE_'].Update(visible=True)
    window['_ADR_'].Update(wallet_details["address"], visible=True)
    window['-IMAGE-'].update(data=convert_to_bytes(os.path.join(config.gen_path, 'wallet_card.png'), resize=new_size))
    window['_PASS_TITLE_'].Update(visible=True)
    window['_PASS_'].Update(visible=True)
    window['_EXP_'].Update(visible=True)
    window['_PRINT_'].Update(visible=True)
    return wallet_details

def convert_to_bytes(file_or_bytes, resize=None):
    '''
    Will convert into bytes and optionally resize an image that is a file or a base64 bytes object.
    Turns into  PNG format in the process so that can be displayed by tkinter
    :param file_or_bytes: either a string filename or a bytes base64 image object
    :type file_or_bytes:  (Union[str, bytes])
    :param resize:  optional new size
    :type resize: (Tuple[int, int] or None)
    :return: (bytes) a byte-string object
    :rtype: (bytes)
    '''
    if isinstance(file_or_bytes, str):
        img = PIL.Image.open(file_or_bytes)
    else:
        try:
            img = PIL.Image.open(io.BytesIO(base64.b64decode(file_or_bytes)))
        except Exception as e:
            dataBytesIO = io.BytesIO(file_or_bytes)
            img = PIL.Image.open(dataBytesIO)

    cur_width, cur_height = img.size
    if resize:
        new_width, new_height = resize
        scale = min(new_height/cur_height, new_width/cur_width)
        img = img.resize((int(cur_width*scale), int(cur_height*scale)), PIL.Image.ANTIALIAS)
    bio = io.BytesIO()
    img.save(bio, format="PNG")
    del img
    return bio.getvalue()

if __name__ == '__main__':
    log_path = os.path.join(os.getcwd(), 'app_gui_log.log')
    logging.basicConfig(filename=log_path, level=logging.INFO,
        format="%(asctime)s:%(levelname)s:%(message)s")

    # Rough GUI prototype

    sg.SetOptions(element_padding=(0, 0), icon=config.mini_icon_path)
    # sg.ListOfLookAndFeelValues()
    # sg.ChangeLookAndFeel('Topanga')

    # ------ Menu Definition ------ #
    menu_def = [['File', ['Load', 'Exit']],
                ['Help', ['About...', 'Usage']], ]

    # ----- Tab Groups ----- #
    btc_group = [[sg.Open('Generate BTC Wallet', size=(17, 2))]]
    eth_group = [[sg.Open('Generate ETH Wallet', size=(17, 2))]]
    doge_group = [[sg.Open('Generate DOGE Wallet', size=(17, 2))]]



    # ------ GUI Defintion ------ #
    col_layout = [[sg.Text('Public Address', key='_W_TITLE_', visible=False)],[sg.InputText(key='_ADR_', visible=False)]]
    col_layout_2 = [[sg.Button('PRINT', key='_PRINT_', visible=False)]]
    layout = [
        [sg.Column(col_layout, element_justification='right', expand_x=True)],
        [sg.Text('1. Select Crypto Token')],
        [sg.Text('2. Click Generate Wallet')],
        [sg.Text('3. Print or Export Wallet\n')],
        [sg.Menu(menu_def, )],
        [sg.TabGroup([[sg.Tab('BTC', btc_group), sg.Tab('ETH', eth_group), sg.Tab('DOGE', doge_group)]])],
        [sg.Text('\n\nEnter Password for Zip File', key='_PASS_TITLE_', visible=False)],
        [sg.InputText('Password', key='_PASS_', visible=False)],
        [sg.Button('Save to Desktop', key='_EXP_', visible=False)],
        [sg.Column(col_layout_2, element_justification='right', expand_x=True)],
        [sg.Image(key='-IMAGE-')],
    ]


    # , sg.Checkbox('Send Automated Integration Request Email', change_submits=True, enable_events=True, default='0',
    #               key='checkboxx')

    window = sg.Window("Crypto Wallet Generator V%s" % version, layout, auto_size_text=True, auto_size_buttons=True,
                       default_button_element_size=(12, 1), size=(600, 1000), location=(0, 0))

    while True:
        event, values = window.Read(timeout=100)
        if event == 'About...':
                    sg.Popup('Wallet Generator Desktop Application ', 'Version %s' % version)
        elif event == 'Usage':
                    sg.Popup('1. Select Crypto Token', '2. Click Generate', '3. Save/Print/Export Wallet')
        elif event == 'Load':
                zip_wallet = sg.popup_get_file('Please enter a file')
                zip_pass = sg.popup_get_text('zip file password', 'Please enter password')
                load_wallet(zip_wallet, zip_pass)
        elif event == 'Exit':
                    config.purge_gen()
                    sys.exit()
        elif event == '_EXP_':
                    zip_pass = values['_PASS_']
                    # input file path
                    input_file = os.path.join(config.gen_path, 'wallet_card.png')
                    details_file = os.path.join(config.gen_path, 'wallet_details.json')
                    # output zip file path
                    output_file = os.path.join(os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop'), '{}_wallet_{}...{}.zip'.format(wallet_details["coin"],wallet_details["address"][:4], wallet_details["address"][-4:]))
                    # compress level
                    com_lvl = 5
                    # compressing file
                    pyminizip.compress_multiple([input_file, details_file], [], output_file, zip_pass, com_lvl)
        elif event == '_PRINT_':
                    os.startfile(os.path.join(config.gen_path, 'wallet_card.png'), "print")
        elif event == 'Generate BTC Wallet':
            try:
                wallet_details = generate_wallet('BTC')
            except Exception as e:
                sg.Popup('Error', e)
                logging.error(e)
        elif event == 'Generate ETH Wallet':
            try:
                wallet_details = generate_wallet('ETH')
            except Exception as e:
                sg.Popup('Error', e)
                logging.error(e)
        elif event == 'Generate DOGE Wallet':
            try:
                wallet_details = generate_wallet('DOGE')
            except Exception as e:
                sg.Popup('Error', e)
                logging.error(e)
        elif event in (None, 'Exit'):
            config.purge_gen()
            break

    # compile command
    # pyinstaller --clean --icon=C:\Users\[user]\PycharmProjects\paper_wallet\stock\blockz_mini.ico --paths=C:\Users\[user]\PycharmProjects\paper_wallet\venv\Lib\site-packages -wF C:\Users\[user]\PycharmProjects\paper_wallet\GUI.py
