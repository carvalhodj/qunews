from itertools import cycle
from PIL import Image
from PIL import ImageTk

try:
    # Python2
    import Tkinter as tk
except ImportError:
    # Python3
    import tkinter as tk

class App(tk.Tk):
    def __init__(self, image_files, x, y, delay):
        tk.Tk.__init__(self)
        self.geometry('+{}+{}'.format(x, y))
        self.delay = delay
        self.atualiza()
        self.picture_display = tk.Label(self)
        self.picture_display.pack()
    def show_slides(self):
        img_object, img_name = next(self.pictures)
        self.picture_display.config(image=img_object)
        self.title(img_name)
        self.after(self.delay, self.show_slides)
    def atualiza(self):
        self.pictures = cycle((ImageTk.PhotoImage(file=image), image)
                              for image in image_files)
        self.after(38500, self.atualiza)
    def run(self):
        self.mainloop()

delay = 3500

image_files = [
'001.png',
'002.png',
'003.png',
'004.png',
'005.png',
'006.png',
'007.png',
'008.png',
'009.png',
'010.png'
]

x = 100
y = 50

try:
    app = App(image_files, x, y, delay)
    app.show_slides()
    app.run()
except:
    print('Erro no processamento das imagens')
