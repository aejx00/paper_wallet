import os
import sys
import qrcode
from pywallet import wallet
from PIL import Image, ImageDraw, ImageFilter, ImageFont

icon_path = os.path.join(os.path.join(os.getcwd(), 'stock'), 'blockchain.png')
blank_path = os.path.join(os.path.join(os.getcwd(), 'stock'), 'blank.png')
font_path = os.path.join(os.path.join(os.getcwd(), 'stock'), 'Cyberpunk.tff')
rocket_path = os.path.join(os.path.join(os.getcwd(), 'stock'), 'rocket.jpg')
moon_path = os.path.join(os.path.join(os.getcwd(), 'stock'), 'moon.png')
arrow_path = os.path.join(os.path.join(os.getcwd(), 'stock'), 'arrow.png')

def purge_gen():
    """cleanup generated photo directory"""
    path = os.path.join(os.path.join(os.getcwd(), 'generated'), 'address.png')
    if os.path.exists(path):
        os.remove(path)


# generate 12 word mnemonic seed
seed = wallet.generate_mnemonic()
print(seed)


# create bitcoin wallet
w = wallet.create_wallet(network="DOGE", seed=seed, children=0)
# print(w)
# w = {'coin': 'BTC', 'seed': 'spend black area skull bridge forget banana quantum carpet green edit keep', 'private_key': 'd31e80c3dfa13e1fd6510c2bf5da161ba3723f13fa3274fcdb4325b88cca3922', 'public_key': '04d59777d44b111caaf885e238659b10e9d9a3f8adeb95e3b065db88ca71553a521a9e3ef46c8beea684e72fb8ea4a82cb94b3294b8979153f6023aebaecc3dd9c', 'xprivate_key': 'xprv9s21ZrQH143K2qNicqE1tUidYsEZhRymADBMSQAdMDXY1WHae1oR2u6fYKmYPkEqLkJiyrco8SxshYyjJwBuVzgp2Cg2Kun6fdKVpc6YRkM', 'xpublic_key': 'xpub661MyMwAqRbcFKTBirm2FcfN6u546thcXS6xEnaEuZ4WtJcjBZ7fahR9PapPzW7ZMktMCSKBqw35PfJg8Xc9eVpjsqE7CvVaMzbyxtVYxFJ', 'address': '1GGE3zmAPyoG1bmU3tQeW4JmLsPVJv5S2B', 'wif': 'L4J6h3D4AP2F3dhvTauZM7tzSggBh6q6UteXmyFtXZ2Jeo8H2rkh', 'children': [{'xpublic_key': 'xpub697sQoWqohPFJxdYQUxEWYRmdYnyr1bf2pgLhiakyrA6PyoxhqPEwi1ZTUHzjrTmB8a9ZVbvFuBUMpSrvkfGBudhPPFkTnN1QdrK7GzU8Pm', 'address': '1MdBvRVTChwMgDMxoA9wAeRYz2qhRmbjEN', 'path': 'm/0', 'bip32_path': "m/44'/0'/0'/0"}], 'xpublic_key_prime': 'xpub697sQoWz9MvDVJcRnsB2RM7YxTrUG71efGAwbcy36CA53QSwtpo7o76Mzv2QwEHPzAisaTwbA6whhRAqo8FsN2eFKe4A9cWvMLnJ1en5ut7'}


# create qr code
img = qrcode.make(w["address"])
# print(type(img))
# print(img.size)
new_qr_path = os.path.join(os.path.join(os.getcwd(), 'generated'), 'address.png')
img.save(new_qr_path)

temp_image_0 = Image.open(icon_path)
temp_image_1 = Image.open(blank_path)
temp_image_2 = Image.open(new_qr_path)
temp_image_3 = Image.open(rocket_path)
temp_image_4 = Image.open(moon_path)
temp_image_5 = Image.open(arrow_path)
# temp_font = ImageFont.truetype(font_path, 20)


back_im = temp_image_1.copy()
back_im.paste(temp_image_2, (630, 280))
back_im.paste(temp_image_0, (780, 210))
back_im.paste(temp_image_3, (820, 730))
back_im.paste(temp_image_4, (870, 710))
back_im.paste(temp_image_5, (570, 340))

overlay = ImageDraw.Draw(back_im)
title_font = ImageFont.truetype("impact.ttf", 40)
temp_font = ImageFont.truetype("arial.ttf", 30)
small_font = ImageFont.truetype("arial.ttf", 20)
mini_font = ImageFont.truetype("arial.ttf", 15)
micro_font = ImageFont.truetype("arial.ttf", 12)
overlay.text((80, 220), "{} Paper Wallet".format(w["coin"]), fill=(0, 0, 0), font=title_font)
overlay.text((50, 280), "public: {} ".format(w["public_key"]), fill=(0, 0, 0), font=micro_font)
overlay.text((50, 300), "Address: {}".format(w["address"]), fill=(0, 0, 0), font=small_font)
overlay.text((50, 660), "private: {} ".format(w["private_key"]), fill=(0, 0, 0), font=mini_font)
overlay.text((50, 690), "WIF: {}".format(w["wif"]), fill=(0, 0, 0), font=micro_font)
overlay.text((50, 710), "Seed: {}".format(seed), fill=(0, 0, 0), font=micro_font)
overlay.text((800, 780), "Hello Moon", fill=(0, 0, 0), font=temp_font)
final_paper_wallet_path = os.path.join(os.path.join(os.getcwd(), 'generated'), 'final.png')
back_im.save(final_paper_wallet_path, quality=95)
purge_gen()
