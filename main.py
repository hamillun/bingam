import csv
import random
from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivymd.uix.button import MDRectangleFlatButton, MDFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.dialog import MDDialog
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
from kivymd.uix.textfield import MDTextField
import re
from kivy.core.audio import SoundLoader

# App Build

class BDApp(MDApp):

    def build(self):
        self.icon = "bgicon.ico"
        self.hover = SoundLoader.load("sfx/sfx_hover.mp3")
        self.deny = SoundLoader.load("sfx/sfx_deny.mp3")
        self.accept = SoundLoader.load("sfx/sfx_accept.mp3")
        self.cy = 0
        self.cx = 0
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Dark"
        self.screen = Screen()
        # Parse CSV, Assign its values to a list to prevent repeat strings.
        f = open("ai_dungeon.csv", "r")
        read = csv.reader(f)
        opt = []
        for row in read:
            opt.append(row)
        f.close()
        csvmax = int(len(opt)) - 1
        val = random.sample(range(0, csvmax), 25)
        bv = ["A1 : ", "B1 : ", "C1 : ", "D1 : ", "E1 : ", "A2 : ", "B2 : ", "C2 : ", "D2 : ", "E2 : ", "A3 : ", "B3 : "
            , "C3 : ", "D3 : ", "E3 : ", "A4 : ", "B4 : ", "C4 : ", "D4 : ", "E4 : ", "A5 : ", "B5 : ", "C5 : ", "D5 : "
            , "E5 : "]
        self.bingo_chart = MDDataTable(pos_hint={"center_x": 0.5, "center_y": 0.59}, size_hint_x=0.9, width=350,
                                       size_hint_y=0.58,rows_num=5,
                                  column_data=[
            ("", dp(5)), ("A", dp(22)), ("B", dp(24)), ("C", dp(26)), ("D", dp(24)), ("E", dp(22))
        ], row_data=[
            ("1",bv[0]+(''.join(opt[val[0]])), (bv[1]+''.join(opt[val[1]])), (bv[2]+''.join(opt[val[2]])),
             (bv[3]+''.join(opt[val[3]])),(bv[4]+''.join(opt[val[4]]))),
            ("2", bv[5]+(''.join(opt[val[5]])), (bv[6]+''.join(opt[val[6]])), (bv[7]+''.join(opt[val[7]])),
             (bv[8]+''.join(opt[val[8]])), (bv[9]+''.join(opt[val[9]]))),
            ("3", (bv[10]+''.join(opt[val[10]])), (bv[11]+''.join(opt[val[11]])), (bv[12]+''.join(opt[val[12]])),
             (bv[13]+''.join(opt[val[13]])), (bv[14]+''.join(opt[val[14]]))),
            ("4", bv[15]+(''.join(opt[val[15]])), (bv[16]+''.join(opt[val[16]])), (bv[17]+''.join(opt[val[17]])),
             (bv[18]+''.join(opt[val[18]])), (bv[19]+''.join(opt[val[19]]))),
            ("5", bv[20]+(''.join(opt[val[20]])), (bv[21]+''.join(opt[val[21]])), (bv[22]+''.join(opt[val[22]])),
             (bv[23]+''.join(opt[val[23]])), (bv[24]+''.join(opt[val[24]]))),

        ])
        self.add_term = MDTextField(size_hint_x=None, pos_hint={"center_x":0.3, "center_y": 0.93}, width=150)
        confterm = MDRectangleFlatButton(text="ADD",size_hint_x=None, pos_hint={"center_x":0.75, "center_y": 0.93},
                                         on_release=self.appendterm)
        bingoconfirm = MDRectangleFlatButton(text="BINGO", pos_hint={"center_x":0.75, "center_y":0.18},
                                             on_release=self.binconf)
        select = self.bingo_chart.bind(on_row_press=self.add_select0)

        self.screen.add_widget(self.bingo_chart)
        self.screen.add_widget(bingoconfirm)
        self.screen.add_widget(self.add_term)
        self.screen.add_widget(confterm)
        return self.screen

    def add_select0(self, instance_table, instance_row):
        self.term = instance_row.text
        conf = MDFlatButton(text="Confirm", on_release=self.add_select1)
        deny = MDFlatButton(text="Cancel", on_release=self.selclose)
        self.selconf = MDDialog(size_hint=(0.65, 0.65), text="Add " + self.term + "?", buttons=[deny, conf])
        self.selconf.open()
        self.hover.play()

    def selclose(self, obj):
        self.selconf.dismiss()
        self.deny.play()

    def add_select1(self, obj):
        self.selconf.dismiss()
        term = self.term[:2]
        if(re.compile("[A]").search(term)):
            self.cx = 0.13
        elif(re.compile("[B]").search(term)):
            self.cx = 0.23
        elif(re.compile("[C]").search(term)):
            self.cx = 0.33
        elif(re.compile("[D]").search(term)):
            self.cx = 0.43
        elif(re.compile("[E]").search(term)):
            self.cx = 0.53
        if(re.compile("[1]").search(term)):
            self.cy = 0.25
        elif(re.compile("[2]").search(term)):
            self.cy = 0.21
        elif(re.compile("[3]").search(term)):
            self.cy = 0.17
        elif(re.compile("[4]").search(term)):
            self.cy = 0.13
        elif(re.compile("[5]").search(term)):
            self.cy = 0.08
        add = MDFlatButton(text=term, pos_hint={"center_x": self.cx, "center_y": self.cy})
        self.screen.add_widget(add)
        self.cx = 0
        self.cy = 0
        self.accept.play()

    def appendterm(self, obj):
        f = open("ai_dungeon.csv", "a", newline='')
        writer = csv.writer(f)
        writer.writerow([self.add_term.text])
        f.close()
        closure = MDFlatButton(text="Close", on_release=self.close_append)
        self.assure = MDDialog(text=self.add_term.text + " was added.", size_hint=(0.65, 0.65), buttons=[closure])
        self.assure.open()
        self.accept()

    def binconf(self, obj):
        bingno = MDFlatButton(text="NO", on_release=self.close_confdialog)
        bingo = MDFlatButton(text="YES", on_release=self.bingo)
        self.confdialog = MDDialog(size_hint=(0.5,0.5), text="Declare Bingo?", buttons=[bingno, bingo])
        self.confdialog.open()
        self.hover.play()

    def close_append(self, obj):
        self.assure.dismiss()
        self.deny.play()

    def close_confdialog(self, obj):
        self.confdialog.dismiss()
        self.deny.play()

    def bingo(self, obj):
        self.confdialog.dismiss()
        cong = MDDialog(size_hint=(0.65, 0.65), text="Congratulations! (Intermission...)")
        cong.open()
        bingoque = ["sfx/sfx_bingo1.wav", "sfx/sfx_bingo2.wav", "sfx/sfx_bingo3.wav", "sfx/sfx_bingo4.wav",
                    "sfx/sfx_bingo5.wav"]
        self.accept.play()
        bingoplay = SoundLoader.load(bingoque[random.randint(0,4)])
        bingoplay.play()

BDApp().run()