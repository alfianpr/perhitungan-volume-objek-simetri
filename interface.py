import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import cv2
import ml_model_beras
import ml_model_telur
import numpy as np

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        # Declare global function
        global threshold_beras, threshold_telur, open_morphology

        # Window setting
        self.title('volume objek simetri 1.0')
        self.geometry("450x570")
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.pixel = tk.StringVar()
        self.predict_result = tk.StringVar()
        self.jarak_var = tk.DoubleVar()
        self.create_widgets()

        # Read file android_camera
        with open("android_camera.txt", encoding='utf8') as url:
            self.url = str(url.readlines()[0])+"/video"
    
        # Fungsi Otsu's Thresholding after Gaussian filtering
        def threshold_beras(img):
            blur = cv2.GaussianBlur(img,(5,5),0)
            ret3, th3 = cv2.threshold(blur, 0, 255, 
                        cv2.THRESH_BINARY+cv2.THRESH_OTSU)
            return th3
        
        # Thresholding with value 90
        def threshold_telur(img):
            blur = cv2.GaussianBlur(img,(5,5),0)
            ret1,th1 = cv2.threshold(img, 90, 255,
                       cv2.THRESH_BINARY)
            return th1

        # Open morphology function
        def open_morphology(th3):
            kernel = np.ones((5,5),np.uint8)
            opening = cv2.morphologyEx(th3, cv2.MORPH_OPEN, kernel)
            return opening

    # Widget function
    def create_widgets(self):
        padding = {'padx': 3, 'pady': 3}
        # Button telur
        btn_telur = ttk.Button(self, text='Telur', command=self.telur)
        btn_telur.grid(column=0, row=0, **padding)

        # Entry
        name_entry = ttk.Entry(self, justify='center', 
                        width=10, textvariable=self.jarak_var)
        name_entry.grid(column=1, row=0, **padding)
        name_entry.focus()

        # Button beras
        btn_beras = ttk.Button(self, text='Beras', command=self.beras)
        btn_beras.grid(column=2, row=0, **padding)

        # Output RGB pict
        #self.lbl_rgb = ttk.Label(self)
        #self.lbl_rgb.grid(column=0, row=2, **padding)

        # Output Thresh pict
        self.lbl_thresh = ttk.Label(self)
        self.lbl_thresh.grid(column=0, row=2, columnspan=3, **padding)

        # Output sum of pixel
        self.lbl_pixel = ttk.Label(self, textvariable=self.pixel)
        self.lbl_pixel.grid(column=2, row=1, **padding)

        # Output predict
        self.lbl_predict = ttk.Label(self, textvariable=self.predict_result)
        self.lbl_predict.grid(column=0, row=1, **padding)

    def beras(self):
        # Open camera
        cap = cv2.VideoCapture(self.url)

        # RGB Picture
        ret, img = cap.read()
        cv2.imwrite("beras.jpg", img)
        show = cv2.resize(img, (500, 400))
        show = cv2.rotate(show, cv2.ROTATE_90_COUNTERCLOCKWISE)
        show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)
        show = Image.fromarray(show)
        show = ImageTk.PhotoImage(show)
        #self.lbl_rgb.imgtk = show
        #self.lbl_rgb.configure(image=show)

        # Thresh Picture
        img = cv2.imread("beras.jpg", 0)
        th3 = threshold_beras(img)
        opening = open_morphology(th3)
        biner = cv2.resize(opening, (500, 400))
        biner = cv2.rotate(biner, cv2.ROTATE_90_COUNTERCLOCKWISE)
        biner = Image.fromarray(biner)
        biner = ImageTk.PhotoImage(biner)
        self.lbl_thresh.imgtk = biner
        self.lbl_thresh.configure(image=biner)

        # Sum Pixel
        jumlah_pixel= np.sum(opening == 255)
        jumlah_pixel = np.float64(jumlah_pixel).item()
        self.pixel.set("Jumlah pixel : "+str(jumlah_pixel))

        # jarak
        jarak_var = self.jarak_var.get()
        float(jarak_var)

        # predict
        predict_result = ml_model_beras.predict(jarak_var, jumlah_pixel)
        self.predict_result.set("Volume (cm^3) : "+
                            str(np.round(predict_result, decimals=2)))

    def telur(self):
        # Open camera
        cap = cv2.VideoCapture(self.url)

        # RGB Picture
        ret, img = cap.read()
        cv2.imwrite("telur.jpg", img)
        show = cv2.resize(img, (500, 400))
        show = cv2.rotate(show, cv2.ROTATE_90_COUNTERCLOCKWISE)
        show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)
        show = Image.fromarray(show)
        show = ImageTk.PhotoImage(show)
        #self.lbl_rgb.imgtk = show
        #self.lbl_rgb.configure(image=show)

        # Thresh Picture
        img = cv2.imread("telur.jpg", 0)
        th3 = threshold_telur(img)
        opening = open_morphology(th3)
        biner = cv2.resize(opening, (500, 400))
        biner = cv2.rotate(biner, cv2.ROTATE_90_COUNTERCLOCKWISE)
        biner = Image.fromarray(biner)
        biner = ImageTk.PhotoImage(biner)
        self.lbl_thresh.imgtk = biner
        self.lbl_thresh.configure(image=biner)

        # Sum Pixel
        jumlah_pixel= np.sum(opening == 255)
        jumlah_pixel = np.float64(jumlah_pixel).item()
        self.pixel.set("Jumlah pixel : "+str(jumlah_pixel))

        # Jarak
        jarak_var = self.jarak_var.get()
        float(jarak_var)

        # Predict
        predict_result = ml_model_telur.predict(jarak_var, jumlah_pixel)
        self.predict_result.set("Volume (cm^3) : "+
                            str(np.round(predict_result, decimals=2)))

if __name__ == "__main__":
    app = App()
    app.mainloop()