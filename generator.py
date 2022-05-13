import os
import config
import qrcode
from pywallet import wallet
from PIL import Image, ImageDraw, ImageFont


def create_seed():
    """generate mnemonic seed phrase"""
    seed = wallet.generate_mnemonic()
    return seed


def create_wallet(token, seed):
    """generate crypto wallet"""
    crypto_wallet = wallet.create_wallet(network=token, seed=seed, children=1)
    return crypto_wallet


def create_qr_code(address):
    """generate public address qr code"""
    img = qrcode.make(address)
    # print(type(img))
    # print(img.size)
    new_qr_path = os.path.join(os.path.join(os.getcwd(), 'generated'), 'address.png')
    img.save(new_qr_path)
    return new_qr_path

def delete_qr_code():
    """cleanup generated photo directory"""
    path = os.path.join(os.path.join(os.getcwd(), 'generated'), 'address.png')
    if os.path.exists(path):
        os.remove(path)

def create_wallet_card(token):
    s = create_seed()
    w = create_wallet(token, s)
    # w = {'coin': 'BTC', 'seed': 'spend black area skull bridge forget banana quantum carpet green edit keep', 'private_key': 'd31e80c3dfa13e1fd6510c2bf5da161ba3723f13fa3274fcdb4325b88cca3922', 'public_key': '04d59777d44b111caaf885e238659b10e9d9a3f8adeb95e3b065db88ca71553a521a9e3ef46c8beea684e72fb8ea4a82cb94b3294b8979153f6023aebaecc3dd9c', 'xprivate_key': 'xprv9s21ZrQH143K2qNicqE1tUidYsEZhRymADBMSQAdMDXY1WHae1oR2u6fYKmYPkEqLkJiyrco8SxshYyjJwBuVzgp2Cg2Kun6fdKVpc6YRkM', 'xpublic_key': 'xpub661MyMwAqRbcFKTBirm2FcfN6u546thcXS6xEnaEuZ4WtJcjBZ7fahR9PapPzW7ZMktMCSKBqw35PfJg8Xc9eVpjsqE7CvVaMzbyxtVYxFJ', 'address': '1GGE3zmAPyoG1bmU3tQeW4JmLsPVJv5S2B', 'wif': 'L4J6h3D4AP2F3dhvTauZM7tzSggBh6q6UteXmyFtXZ2Jeo8H2rkh', 'children': [{'xpublic_key': 'xpub697sQoWqohPFJxdYQUxEWYRmdYnyr1bf2pgLhiakyrA6PyoxhqPEwi1ZTUHzjrTmB8a9ZVbvFuBUMpSrvkfGBudhPPFkTnN1QdrK7GzU8Pm', 'address': '1MdBvRVTChwMgDMxoA9wAeRYz2qhRmbjEN', 'path': 'm/0', 'bip32_path': "m/44'/0'/0'/0"}], 'xpublic_key_prime': 'xpub697sQoWz9MvDVJcRnsB2RM7YxTrUG71efGAwbcy36CA53QSwtpo7o76Mzv2QwEHPzAisaTwbA6whhRAqo8FsN2eFKe4A9cWvMLnJ1en5ut7'}

    """generate buisness card sized physial wallet"""
    temp_image_0 = Image.open(config.icon_path)
    temp_image_1 = Image.open(config.blank_path)
    temp_image_2 = Image.open(create_qr_code(w["seed"]))
    temp_image_3 = Image.open(config.rocket_path)
    temp_image_4 = Image.open(config.moon_path)
    temp_image_5 = Image.open(config.arrow_path)
    # temp_font = ImageFont.truetype(font_path, 20)

    back_im = temp_image_1.copy()
    back_im.paste(temp_image_2, (580, 280))
    back_im.paste(temp_image_0, (780, 210))
    back_im.paste(temp_image_3, (820, 730))
    back_im.paste(temp_image_4, (870, 710))
    back_im.paste(temp_image_5, (550, 340))

    overlay = ImageDraw.Draw(back_im)
    title_font = ImageFont.truetype("impact.ttf", 40)
    temp_font = ImageFont.truetype("arial.ttf", 30)
    small_font = ImageFont.truetype("arial.ttf", 20)
    mini_font = ImageFont.truetype("arial.ttf", 15)
    micro_font = ImageFont.truetype("arial.ttf", 12)
    overlay.text((80, 220), "{} Paper Wallet".format(w["coin"]), fill=(0, 0, 0), font=title_font)
    pub1, pub2 = w["public_key"][:len(w["public_key"]) // 2], w["public_key"][len(w["public_key"]) // 2:]
    overlay.text((50, 280), "public: {}".format(pub1), fill=(0, 0, 0), font=micro_font)
    overlay.text((90, 295), "{}".format(pub2), fill=(0, 0, 0), font=micro_font)
    overlay.text((50, 315), "Address: {}".format(w["address"]), fill=(0, 0, 0), font=small_font)
    pri1, pri2 = w["private_key"][:len(w["private_key"]) // 2], w["private_key"][len(w["private_key"]) // 2:]
    overlay.text((50, 720), "private: {}".format(pri1), fill=(0, 0, 0), font=mini_font)
    overlay.text((100, 735), "{}".format(pri2), fill=(0, 0, 0), font=mini_font)
    if w["wif"]:
        overlay.text((50, 760), "WIF: {}".format(w["wif"]), fill=(0, 0, 0), font=micro_font)
    overlay.text((50, 775), "Seed: {}".format(w["seed"]), fill=(0, 0, 0), font=micro_font)
    overlay.text((800, 780), "Hello Moon", fill=(0, 0, 0), font=temp_font)
    final_paper_wallet_path = os.path.join(os.path.join(os.getcwd(), 'generated'), 'wallet_card.png')
    back_im.save(final_paper_wallet_path, quality=95)
    delete_qr_code()
    return w


if __name__ == '__main__':
    # se = create_seed()
    # print(s)
    # w = create_wallet('ETH', s)
    # wa = {'coin': 'BTC', 'seed': 'spend black area skull bridge forget banana quantum carpet green edit keep', 'private_key': 'd31e80c3dfa13e1fd6510c2bf5da161ba3723f13fa3274fcdb4325b88cca3922', 'public_key': '04d59777d44b111caaf885e238659b10e9d9a3f8adeb95e3b065db88ca71553a521a9e3ef46c8beea684e72fb8ea4a82cb94b3294b8979153f6023aebaecc3dd9c', 'xprivate_key': 'xprv9s21ZrQH143K2qNicqE1tUidYsEZhRymADBMSQAdMDXY1WHae1oR2u6fYKmYPkEqLkJiyrco8SxshYyjJwBuVzgp2Cg2Kun6fdKVpc6YRkM', 'xpublic_key': 'xpub661MyMwAqRbcFKTBirm2FcfN6u546thcXS6xEnaEuZ4WtJcjBZ7fahR9PapPzW7ZMktMCSKBqw35PfJg8Xc9eVpjsqE7CvVaMzbyxtVYxFJ', 'address': '1GGE3zmAPyoG1bmU3tQeW4JmLsPVJv5S2B', 'wif': 'L4J6h3D4AP2F3dhvTauZM7tzSggBh6q6UteXmyFtXZ2Jeo8H2rkh', 'children': [{'xpublic_key': 'xpub697sQoWqohPFJxdYQUxEWYRmdYnyr1bf2pgLhiakyrA6PyoxhqPEwi1ZTUHzjrTmB8a9ZVbvFuBUMpSrvkfGBudhPPFkTnN1QdrK7GzU8Pm', 'address': '1MdBvRVTChwMgDMxoA9wAeRYz2qhRmbjEN', 'path': 'm/0', 'bip32_path': "m/44'/0'/0'/0"}], 'xpublic_key_prime': 'xpub697sQoWz9MvDVJcRnsB2RM7YxTrUG71efGAwbcy36CA53QSwtpo7o76Mzv2QwEHPzAisaTwbA6whhRAqo8FsN2eFKe4A9cWvMLnJ1en5ut7'}
    create_wallet_card('BTC')
