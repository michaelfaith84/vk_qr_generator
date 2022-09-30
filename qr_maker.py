import qrcode
from PIL import Image, ImageDraw, ImageFont

class MakeQrCode:
    def __init__(self, url, margin=1.33):
        self.url = url
        self.margin = margin
        self.logo = Image.open('vk.png')

    def add_margin(self, pil_img, margin):
        width, height = pil_img.size
        new_width = width * margin
        new_height = height * margin
        result = Image.new(pil_img.mode, (round(new_width), round(new_height)), "white")
        result.paste(pil_img, (round((new_width - width) * .5), round((new_height - height) * .5)))
        return {"new": result, "old_height": height }

    def make(self):
        basewidth = 100

        wpercent = (basewidth/float(self.logo.size[0]))
        hsize = int((float(self.logo.size[1])*float(wpercent)))
        logo = self.logo.resize((basewidth, hsize), Image.ANTIALIAS)
        QRcode = qrcode.QRCode(
            error_correction=qrcode.constants.ERROR_CORRECT_H
        )

        QRcode.add_data(self.url)

        QRcode.make()

        QRcolor = 'Black'

        QRimg = QRcode.make_image(
            fill_color=QRcolor, back_color="white").convert('RGB')

        pos = ((QRimg.size[0] - logo.size[0]) // 2,
               (QRimg.size[1] - logo.size[1]) // 2)
        QRimg.paste(logo, pos)

        res = self.add_margin(QRimg, self.margin)
        QRimg = res['new']
        old_height = res['old_height']
        img = ImageDraw.Draw(QRimg)
        font = ImageFont.truetype('Roboto-Regular.ttf', 96)
        height, width = QRimg.size
        w1, h1 = img.textsize("Secured", font=font)
        w2, h2 = img.textsize("With", font=font)
        h1 -= h1 * .21
        h2 -= h2 * .21
        img.text(((width - w1) / 2,  (height - old_height) / 2 - h1), "Secured", fill=(0, 0, 0), font=font)
        img.text(((width - w2) / 2, old_height + (height - old_height) / 2 - h2 * .5), "With", fill=(0, 0, 0), font=font)

        QRimg.save('gpg_vk.png')

        return True
