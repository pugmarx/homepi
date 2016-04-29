#!/usr/bin/env python

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from oled.device import ssd1306, sh1106
from oled.render import canvas
from PIL import ImageDraw, Image

plt.plot([1,2,3, 4.5,4.2,2,1.4], linewidth=2.0)
plt.savefig('myfig1')
device = ssd1306(port=1, address=0x3C)

with canvas(device) as draw:
    #logo = Image.open('examples/images/pi_logo.png')
	logo = Image.open('myfig1.png')
	logo_r = logo.resize((128,64), Image.BICUBIC)
	logo_bw = logo_r.convert("1")
	draw.bitmap((0, 0), logo_bw, fill=1)
