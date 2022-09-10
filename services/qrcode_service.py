import os
from PIL import Image
from typing import Dict
from uuid import uuid4
import qrcode
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
from settings import QRCODES_DIR


def qrcode_gen(qr_data: Dict) -> str:
    user_id = qr_data.get("user_id", None)
    user_name = qr_data.get("user_name", None)
    link = f'https://ya.ru'
    try:
        qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_L)
    except Exception as err:
        print(f'err1: {err}')
    
    qr.add_data(link)
    qr.make()
    img = qr.make_image(back_color="#FFFFFF",
                        module_drawer=RoundedModuleDrawer())
    filename = f"qr_{uuid4().hex}.png"
    #'/home/.../src/media/users/qrcode/domitem_6c8e3c38cb364053982aa7978d22c5ee.png'
    file_path = os.path.join(QRCODES_DIR, filename)
    img.save(file_path)
    # #Вставляем лого в середину qr
    # qr_img = Image.open(file_path)
    # width, height = qr_img.size
    # logo_size = 60
    # logo_img = Image.open(os.path.join(QRCODES_DIR, 'pass_qr.jpg'))
    # #Подгоняем размеры
    # xmin = ymin = int((width / 2) - (logo_size / 2))
    # xmax = ymax = int((width / 2) + (logo_size / 2))
    # #Изменяем размер лого
    # logo = logo_img.resize((xmax - xmin, ymax - ymin))
    # #Вставляем лого в qr
    # qr_img.paste(logo, (xmin, ymin, xmax, ymax))
    # qr_img.save(file_path)
    print(file_path)
    return file_path
