import os
mini_icon_path = os.path.join(os.path.join(os.getcwd(), 'stock'), 'blockz_mini.ico')
icon_path = os.path.join(os.path.join(os.getcwd(), 'stock'), 'blockchain.png')
blank_path = os.path.join(os.path.join(os.getcwd(), 'stock'), 'blank.png')
font_path = os.path.join(os.path.join(os.getcwd(), 'stock'), 'Cyberpunk.tff')
rocket_path = os.path.join(os.path.join(os.getcwd(), 'stock'), 'rocket.jpg')
moon_path = os.path.join(os.path.join(os.getcwd(), 'stock'), 'moon.png')
arrow_path = os.path.join(os.path.join(os.getcwd(), 'stock'), 'arrow.png')

# output
gen_path = os.path.join(os.getcwd(), 'generated')


def purge_gen():
    """cleanup generated photo directory"""
    # path = os.path.join(os.path.join(os.getcwd(), 'generated'), 'address.png')
    if os.path.exists(gen_path):
        for f in os.listdir(gen_path):
            os.remove(os.path.join(gen_path, f))
