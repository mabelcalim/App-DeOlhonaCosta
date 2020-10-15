#encondings: utf-8
# -*- coding: utf-8 -*-
__author__ = 'Mabel'

__version__ = '0.0.1.7'
'''LEGEC App
   escrito por: Mabel Calim Costa
   data: MAR/2019 - OUT/2020
   DRAFT8
 camera Ok
 sumT Ok
 recuperar senha Ok
 BD do projeto no Firebase
'''

import kivy
kivy.require('1.9.1')
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen, ScreenManager
import time
from kivy.graphics import Color, Ellipse
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
import platform
import sys
from kivy.uix.popup import Popup
from functools import partial
from kivy.uix.label import Label
from kivy.properties import ListProperty
from random import random as r
from kivy.factory import Factory as F
from kivy.uix.behaviors import DragBehavior
from random import randint
from kivy.core.window import Window
from kivy.properties import NumericProperty,ObjectProperty,StringProperty
from kivy.graphics import Line, Color, InstructionGroup
from kivy.uix.button import ButtonBehavior
from kivy.uix.image import Image
from kivy.graphics.vertex_instructions import Rectangle
from kivy.clock import Clock
from kivy.core.window import Window
import os
#os.environ['KIVY_GLES_LIMITS'] = '0'
import requests
import json, multiprocessing
from kivy.garden.mapview import MapView,MapMarker
from kivy.properties import NumericProperty
import pickle
from kivy.utils import platform
#from android.permissions import request_permissions, Permission
#request_permissions([Permission.CAMERA])

#from gi.repository import Gst
#import gi
#gi.require_version('Gst','1.0')
#from android.permissions import request_permission, Permission
#request_permission(Permission.CAMERA)

from kivy.uix.checkbox import CheckBox


class LabelButton(ButtonBehavior, Label):
    pass
class ImageButton(ButtonBehavior, Image):
    pass
class Circle_C(Widget):

    def __init__(self, **kwargs):
        super(Circle_C, self).__init__(**kwargs)

        #self.size = (50,50)
        #self.pos = (150,500)
        with self.canvas:
            #self.rect = Rectangle(pos = self.pos, size = (50,50))
            #Color(0,0, 0, 0.01)
            self.circle = Ellipse(pos=self.pos, size=self.size)
        self.bind(pos=self.redraw)
    def redraw(self, *args):
        #self.circle.size = self.size
        self.circle.pos = self.pos
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            # if the touch collides with our widget, let's grab it
            touch.grab(self)
            # and accept the touch.
        #if touch.is_double_tap:
            #self.canvas.after.clear()
        #    item = self.objects.pop(-1)
        #    self.canvas.remove(item)
            return True
        return super(Circle_C, self).on_touch_down(touch)
    def on_touch_up(self, touch):
        # check if it's a grabbed touch event
        if touch.grab_current is self:
            # don't forget to ungrab ourself, or you might have side effects
            touch.ungrab(self)
            # and accept the last up

            return True
        return super(Circle_C, self).on_touch_up(touch)
    def on_touch_move(self, touch):
        # check if it's a grabbed touch event
        if touch.grab_current is self:
            self.pos = touch.pos

            return True
        return super(Circle_C, self).on_touch_move(touch)


class FirstPage(Screen):
    pass

class LoginPage(Screen):
    # rm photo files
    import os
    import glob
    path = str(os.path.abspath(os.path.dirname(__file__)))
    files = glob.glob(path+"/fotos/*")
    for f in files:
        os.remove(f)
    files = glob.glob(path+"/maps/*")
    for f in files:
        os.remove(f)
    #os.remove(path+ "/LAT.p")
    #os.remove(path+ "/LON.p")


    def add_user(self,login_email,login_password):

        #based on Erik Sandberg
        #from firebase import firebase

        import datetime
        import os

        path = str(os.path.abspath(os.path.dirname(__file__)))
        # remove localId if exists
        if os.path.exists(path+"/localId.p") == True:
            os.remove(path+"/localId.p")
        #bd = firebase.FirebaseApplication('https://deolhonacosta-2019.firebaseio.com', None)
        wak = '' #senha google firebase
        signup_url = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/signupNewUser?key=" + wak
        #print (login_email.text, login_password.text)
        signup_payload = {"email": login_email.text, "password": login_password.text, "returnSecureToken": True}
        sign_up_request = requests.post(signup_url, data=signup_payload)
        #print(sign_up_request.ok)
        #print(sign_up_request.content.decode())
        sign_up_data = json.loads(sign_up_request.content.decode())
        #print(sign_up_data)
        if sign_up_request.ok == True:
            refresh_token = sign_up_data['refreshToken']
            localId = sign_up_data['localId']
            print (localId)
            idToken = sign_up_data['idToken']
            #u_email = str(sign_up_data['email'])
            # Save refreshToken to a file
            pickle.dump( idToken, open( path+"/id_token.p", "wb" ) )
            pickle.dump( refresh_token, open(path+ "/refresh_token.p", "wb" ) )
            pickle.dump( localId, open( path+"/localId.p", "wb" ) )
            pickle.dump( login_email.text, open( path+"/login_email.p", "wb" ) )
            self.localId =  localId
            self.idToken =  idToken
            self.refresh =  refresh_token
            id_coleta = 'coleta_000'
            pickle.dump( id_coleta, open( path+ "/id_coleta.p", "wb" ) )
            #global idToken
            # create a new user in database from localId
            # patch some data
            data_agora = str(datetime.datetime.now())
            user_data = '{"%s":{"data": "%s","local":""}}'%(id_coleta,str(datetime.datetime.now()))
            post_request = requests.patch("https://deolhonacosta-2019.firebaseio.com/users/" + localId + ".json?auth=" + idToken,
                            data=user_data)
            self.ids['forget_passwd'].text = " "
            self.ids['login_message'].text = " "
            self.ids['login_messageok'].text= " "
            self.ids['login_messageok'].text = "OK,você está conectado! "
        if sign_up_request.ok == False:
            error_data = json.loads(sign_up_request.content.decode())
            error_message = error_data["error"]['message']
            #print(login_message.text)
            self.ids['forget_passwd'].text = " "
            self.ids['login_message'].text = " "
            self.ids['login_messageok'].text= " "
            self.ids['login_message'].text = error_message


    def login_user(self,login_email,login_password):

            # first check users
            import requests
            import json
            import datetime
            import os
            import pickle

            path = str(os.path.abspath(os.path.dirname(__file__)))

            # make sure there isn't pickle files
            if os.path.exists(path+"/localId.p") == True:
                os.remove(path+"/localId.p")
            check_user = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword"
            wak = ''# coloque aqui senha do google firebase
            url = "%s?key=%s" % (check_user,wak)
            data = {"email": login_email.text,
                "password": login_password.text,
                "returnSecureToken": True}
            result = requests.post(url, json=data)
            is_login_successful = result.ok
            sign_in_data = result.json()
            #print (sign_in_data['localId'])
            #print(result.content.decode())

            if result.ok == True:
                self.ids['forget_passwd'].text = " "
                self.ids['login_message'].text = " "
                self.ids['login_messageok'].text= " "
                self.ids['login_messageok'].text = "conectando com o banco de dados ... "
                refresh_token = sign_in_data['refreshToken']
                localId = sign_in_data['localId']
                idToken = sign_in_data['idToken']
                # Save refreshToken to a file
                pickle.dump( idToken, open( path+ "/id_Token.p", "wb" ) )
                pickle.dump( refresh_token, open( path+ "/refresh_token.p", "wb" ) )
                pickle.dump( localId, open( path+ "/localId.p", "wb" ) )
                pickle.dump( login_email.text, open( path+"/login_email.p", "wb" ) )

                self.localId =  localId
                self.idToken =  idToken
                self.refresh =  refresh_token

                bd = requests.get("https://deolhonacosta-2019.firebaseio.com/users/" +localId + ".json?auth=" + idToken)
                check = bd.json()
                id_check = ObjectProperty(None) # try using kivy ids
                id_coleta = ObjectProperty(None)
                # so ate 99- passou de 100 nao funciona
                id_check = list(check)[-1]
                print(list(check)[-1])

                if (int(id_check[7:10]) + 1) <10:
                    id_coleta= "coleta_00"+ str(int(id_check[7:10]) + 1)
                elif (int(id_check[7:10]) + 1) >=9:
                    id_coleta= "coleta_0"+ str(int(id_check[7:10]) + 1)
                elif (int(id_check[7:10]) + 1) >=99:
                    id_coleta= "coleta_"+ str(int(id_check[7:10]) + 1)
                print (id_coleta)
                pickle.dump( id_coleta, open( path+ "/id_coleta.p", "wb" ) )
                user_data = '{"%s":{"data": "%s","local":""}}'%(id_coleta,str(datetime.datetime.now()))
                post_request = requests.patch("https://deolhonacosta-2019.firebaseio.com/users/" + localId + ".json?auth=" + idToken,data=user_data)
                self.ids['forget_passwd'].text = " "
                self.ids['login_message'].text = " "
                self.ids['login_messageok'].text= " "
                #self.ids['login_messageok'].text.replace = "OK,você está conectado! "
                self.ids['login_messageok'].text = "OK,você está conectado! "
            else:
                error_data = json.loads(result.content.decode())
                error_message = error_data["error"]['message']
                #print(login_message.text)
                self.ids['forget_passwd'].text = " "
                self.ids['login_message'].text = " "
                self.ids['login_messageok'].text= " "
                self.ids['login_message'].text = error_message

    def forgot_password(self,login_email):
            path = str(os.path.abspath(os.path.dirname(__file__)))
            wak = '' #coloque aqui senha do google firebase
            password_reset = "https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode?key=" + wak
            signup = {"requestType":"PASSWORD_RESET","email":login_email.text}
            post_psw = requests.post(password_reset,data=signup)
            print('Enviando email')
            self.ids['forget_passwd'].text = " "
            self.ids['login_message'].text = " "
            self.ids['login_messageok'].text= " "
            self.ids['forget_passwd'].text = "Senha enviada por email! "

    def change_screen(self):
            if self.ids['login_messageok'].text == "OK,você está conectado! ":
                #self.parent.current = 'local'
                self.parent.current = self.manager.next()
            elif self.ids['login_message'].text == "MISSING_PASSWORD":
                self.ids['forget_passwd'].text = " "
                self.ids['login_message'].text = " "
                self.ids['login_messageok'].text= " "
                self.ids['login_messageok'].text = "Se cadastre, por favor."
            elif self.ids['login_message'].text == "MISSING_EMAIL":
                self.ids['forget_passwd'].text = " "
                self.ids['login_message'].text = " "
                self.ids['login_messageok'].text= " "
                self.ids['login_messageok'].text = "Se cadastre, por favor."
            elif self.ids['login_message'].text == "WEAK_PASSWORD : Password should be at least 6 characters":
                self.ids['forget_passwd'].text = " "
                self.ids['login_message'].text = " "
                self.ids['login_messageok'].text= " "
                self.ids['login_messageok'].text = "Se cadastre, por favor."
            elif self.ids['login_message'].text == "EMAIL_EXISTS":
                self.ids['forget_passwd'].text = " "
                self.ids['login_message'].text = " "
                self.ids['login_messageok'].text= " "
                self.ids['login_messageok'].text = "Se cadastre, por favor."
            elif self.ids['login_message'].text == "INVALID_EMAIL":
                self.ids['forget_passwd'].text = " "
                self.ids['login_message'].text = " "
                self.ids['login_messageok'].text= " "
                self.ids['login_messageok'].text = "Se cadastre, por favor."
            elif self.ids['login_message'].text == "INVALID_PASSWORD":
                self.ids['forget_passwd'].text = " "
                self.ids['login_message'].text = " "
                self.ids['login_messageok'].text= " "
                self.ids['login_messageok'].text = "Se cadastre, por favor."
            elif self.ids['login_message'].text == "EMAIL_NOT_FOUND":
                self.ids['forget_passwd'].text = " "
                self.ids['login_message'].text = " "
                self.ids['login_messageok'].text= " "
                self.ids['login_messageok'].text = "Se cadastre, por favor."

class LocalColeta(Screen):
    import os
    lat= NumericProperty()
    lon= NumericProperty()
    import os
    import glob
    path = str(os.path.abspath(os.path.dirname(__file__)))
    files = glob.glob(path+"/fotos/*")
    for f in files:
        os.remove(f)
    files = glob.glob(path+"/maps/*")
    for f in files:
        os.remove(f)

    def search(self):
        path = str(os.path.abspath(os.path.dirname(__file__)))
        self.ids['local_msg'].text = ''
        #self.ids['local_msg'].color = 0,1,0,1
        #self.ids['local_msg'].text =  'procurando local da coleta ...'


        import googlemaps
        #f = open('../googlemaps_keys.txt','r')
        #gkeys = f.readlines()
        #print (str(gkeys[0]))
        #gmaps = googlemaps.Client(key=str(gkeys[0]))
        gmaps = googlemaps.Client(key='') #senha googlemaps API
        geocode_result = gmaps.geocode("%s"%self.ids['local_input'].text)
        ind_local = self.ids['local']
        ind_local.text = str(geocode_result[0]['geometry']['location'])

        #self.ids['local_msg'].color = 0,1,0,1
        #self.ids['local_msg'].text =  'procurando local da coleta ...'
        self.lat = geocode_result[0]['geometry']['location']['lat']
        self.lon = geocode_result[0]['geometry']['location']['lng']
        self.ids['localview'].center_on(self.lat, self.lon)
        self.ids['localview'].zoom = 14

        pickle.dump( self.lat, open( path+ "/LAT.p", "wb" ) )
        pickle.dump( self.lon, open( path+ "/LON.p", "wb" ) )

        marker = self.ids['local_mark']
        marker.text = "você está aqui! \n lat: %.4f \n lon: %.4f   "%(self.lat,self.lon)

        # connect to firebase
        localId = pickle.load( open(  path+"/localId.p", "rb" ) )
        id_coleta = pickle.load( open( path+ "/id_coleta.p", "rb" ) )
        idToken = pickle.load( open(  path+"/id_Token.p", "rb" ) )

        c_marker = self.ids['coleta_mark']
        c_marker.text = "%s"%id_coleta
        #bd = firebase.FirebaseApplication('https://deolhonacosta-2019.firebaseio.com/users/'+localId+id_coleta, authentication=None)
        user_data = '{"local":"%s"}'%(ind_local.text )
        post_request = requests.patch('https://deolhonacosta-2019.firebaseio.com/users/%s/%s'%(localId,id_coleta) + ".json?auth=" + idToken,
                            data=user_data)

        global name_trans
        name_trans = 'trans01'
        user_data1 = '{"ext":{"total_inf":"","total_sup":"","fx1_inf":"","fx1_sup":"","fx2_inf":"","fx2_sup":"","fx3_inf":"","fx3_sup":""}}'
        post_request = requests.patch('https://deolhonacosta-2019.firebaseio.com/users/%s/%s/%s/'%(localId,id_coleta,name_trans) + ".json?auth=" + idToken,
                data=user_data1)
        print (name_trans)

    def change_screen(self):
        #path = str(os.path.abspath(os.path.dirname(__file__)))
        #exists = os.path.isfile(path+ "/LAT.p")
        if self.lat !=0:

            self.parent.current=self.manager.next()

            #self.ids['local_msg'].color = 0,0,0,1
            #self.ids['local_msg'].text =  'Selecione um local para coleta!'
        else:
            print('error') #local_msg
            self.ids['local_msg'].text = ''
            self.ids['local_msg'].color = 1,0,0,1
            self.ids['local_msg'].text =  'Selecione um local para coleta!'


class Trans(Screen):
    #name_trans = ''
    name_fx = ''

    def change_trans(self):
        global name_trans
        name_trans=name_trans[0:6]+str(int(name_trans[-1])+1)
        print(name_trans)
        self.ids['trans_id'].text = name_trans
    def change_fx(self,name):
        global name_fx
        name_fx=name
        print(name_fx)


    def new_craca(self):
        self.ids['trans_craca'].color = 1.,1.,1., 1
        self.ids['trans_ostra'].color = 1.,1.,1., 0.6
        self.ids['trans_alga'].color = 1.,1.,1., 0.6

    def new_ostra(self):
        self.ids['trans_craca'].color = 1.,1.,1., 0.6
        self.ids['trans_ostra'].color = 1.,1.,1., 1
        self.ids['trans_alga'].color = 1.,1.,1., 0.6

    def new_alga(self):
        self.ids['trans_craca'].color = 1.,1.,1., 0.6
        self.ids['trans_ostra'].color = 1.,1.,1., 0.6
        self.ids['trans_alga'].color = 1.,1.,1., 1

    def label_craca(self):
        self.ids['trans_craca_label'].text = 'CRACA'
    def label_ostra(self):
        self.ids['trans_ostra_label'].text = 'BIVALVES'
    def label_alga(self):
        self.ids['trans_alga_label'].text = 'ALGA'
    # connect to firebase
    def add_firebase(self):
        "connect to firebase"
        import os
        # send fotos to gmail


        global name_trans
        try:
            name_trans
            path = str(os.path.abspath(os.path.dirname(__file__)))
            localId = pickle.load( open(  path+"/localId.p", "rb" ) )
            id_coleta = pickle.load( open( path+ "/id_coleta.p", "rb" ) )
            idToken = pickle.load( open(  path+"/id_Token.p", "rb" ) )
            #bd = firebase.FirebaseApplication('https://deolhonacosta-2019.firebaseio.com/users/'+localId+id_coleta, authentication=None)
            user_data = '{"ext":{"total_inf":"%s","total_sup":"%s","fx1_inf":"%s","fx1_sup":"%s","fx2_inf":"%s","fx2_sup":"%s","fx3_inf":"%s","fx3_sup":"%s"}}'%(self.ids['trans_inf'].text,self.ids['trans_sup'].text,self.ids['trans_fx1_inf'].text,self.ids['trans_fx1_sup'].text,self.ids['trans_fx2_inf'].text,self.ids['trans_fx2_sup'].text,self.ids['trans_fx3_inf'].text,self.ids['trans_fx3_sup'].text)
            #user_data = '{"fx1":{"craca":"%s","ostra":"%s","alga":"%s","rocha":"%s","total":"%s"}}'
            print('https://deolhonacosta-2019.firebaseio.com/users/%s/%s/%s/'%(localId,id_coleta,name_trans))
            post_request = requests.patch('https://deolhonacosta-2019.firebaseio.com/users/%s/%s/%s/'%(localId,id_coleta,name_trans) + ".json?auth=" + idToken,
                    data=user_data)
            self.ids['trans_msgok'].text = ''
            self.ids['trans_msgok'].color = 0,1,0,1
            #self.ids['trans_msgok'].text = '%s salvo com sucesso no BD!'% name_trans



        except:
            self.ids['trans_msgok'].text = ''
            self.ids['trans_msgok'].color = 1,0,0,1
            self.ids['trans_msgok'].text = 'Selecione o transecto!'

    def reset(self):
        global name_fx
        self.ids['trans_inf'].text = ''
        self.ids['trans_sup'].text = ''
        self.ids['trans_fx1_inf'].text =''
        self.ids['trans_fx1_sup'].text = ''
        self.ids['trans_fx2_inf'].text =''
        self.ids['trans_fx2_sup'].text = ''
        self.ids['trans_fx3_inf'].text =''
        self.ids['trans_fx3_sup'].text = ''

        self.ids['trans_msgok'].text = ''

        self.ids['trans_craca'].color = 1.,1.,1., 0.6
        self.ids['trans_ostra'].color = 1.,1.,1., 0.6
        self.ids['trans_alga'].color = 1.,1.,1., 0.6


        path = str(os.path.abspath(os.path.dirname(__file__)))
        t01_file = (path+"/fotos/trans01faixa01_foto.png")
        t02_file = (path+"/fotos/trans02faixa01_foto.png")
        t03_file = (path+"/fotos/trans03faixa01_foto.png")
        t04_file = (path+"/fotos/trans04faixa01_foto.png")
        t05_file = (path+"/fotos/trans05faixa01_foto.png")
        name_fx = ''


    def send_photo(self):
        import os
        from email.mime.multipart import MIMEMultipart
        from email.mime.image import MIMEImage
        from email.mime.text import MIMEText
        import smtplib
        import datetime
        self.ids['trans_msgok'].text = ''
        self.ids['trans_msgok'].color = 0,0,1,1
        self.ids['trans_msgok'].text = 'enviando fotos para email do projeto ... '
        msg = MIMEMultipart()
        username = 'projetodeolhonacosta@gmail.com'
        password =  'C13nc1@c1d@d@'
        user_email = pickle.load( open( path+ "/login_email.p", "rb" ) )
        id_coleta = pickle.load( open( path+ "/id_coleta.p", "rb" ) )
        lat = pickle.load( open( path+ "/LAT.p", "rb" ) )
        lon = pickle.load( open( path+ "/LON.p", "rb" ) )
        msg['From'] = username
        msg['To'] = username
        print(msg['From'],msg['To'])
        txt = MIMEText('usuario: %s \n local: lat=%s lon=%s \n data:%s'% (user_email,lat,lon,str(datetime.datetime.now())))
        msg['Subject'] = '[APP] from:%s Fotos %s local lat=%s lon=%s'%(user_email,id_coleta,lat,lon)
        # list photos
        ldir = os.listdir(path+"/fotos")
        print(ldir)

        for l in ldir:
            file = path+"/fotos/"+ str(l)
            fp = open (file, 'rb')
            img = MIMEImage(fp.read())
            fp.close()
            #encoders.encode_base64(img)
            img.add_header('Content-Disposition','attachment',filename='%s'%l)
            msg.attach(img)
        msg.attach(txt)
        server = smtplib.SMTP('smtp.gmail.com: 587')
        server.starttls()
        server.login(msg['From'], password)
        server.sendmail(msg['From'], msg['To'], msg.as_string())
        server.quit()
        self.ids['trans_id'].text = 'trans01'

class Camera_page(Screen):

    #name_trans = ''
    name_fx = ''


    #def change_trans(self,name):
    #    global name_trans
    #    name_trans=name
    #    print(name_trans)
    def new_craca(self):
        self.ids['ck_fx01'].color = 1.,1.,1., 1
        self.ids['ck_fx02'].color = 1.,1.,1., 0.6
        self.ids['ck_fx03'].color = 1.,1.,1., 0.6

    def new_ostra(self):
        self.ids['ck_fx01'].color = 1.,1.,1., 0.6
        self.ids['ck_fx02'].color = 1.,1.,1., 1
        self.ids['ck_fx03'].color = 1.,1.,1., 0.6

    def new_alga(self):
        self.ids['ck_fx01'].color = 1.,1.,1., 0.6
        self.ids['ck_fx02'].color = 1.,1.,1., 0.6
        self.ids['ck_fx03'].color = 1.,1.,1., 1

    #def change_fx(self,name):
    #    global name_fx
    #    name_fx=name
    #    print(name_fx)

    def reset (self):
        self.ids['msg_error'].text = ''

    def capture(self):
        '''
        Function to capture the images and give them the names
        according to their captured time and date.
        '''
        #from os import getcwd
        #self.cwd = getcwd() + "/"
        #path = self.cwd
        ##    return
        #from android.permissions import Permission, request_permissions
        #request_permissions(Permission.CAMERA)
        global name_trans
        global name_fx
        import os


        #if name_trans is not None and  name_fx  is not None  :
        try:
            name_trans and name_fx
            path = str(os.path.abspath(os.path.dirname(__file__)))
            #print(path)
            path_faixa = path+"/fotos/%s%s_foto.png"%(name_trans,name_fx)
            if os.path.exists(path_faixa) == True:
                camera = self.ids['camera']
                os.remove(path+"/fotos/%s%s_foto.png"%(name_trans,name_fx))
                #timestr = time.strftime("%Y%m%d_%H%M%S")
                #camera.export_to_png(path+"data/FX2_OSTRA_foto.png")#%str(root.ids['craca_label'].text)) #.format(timestr))
                camera.export_to_png(path+"/fotos/%s%s_foto.png"%(name_trans,name_fx))
            else:
                camera = self.ids['camera']
                camera.export_to_png(path+"/fotos/%s%s_foto.png"%(name_trans,name_fx))
            #self.ids['msg_error'].text = ''
            #self.ids['msg_error'].color = 0,1,0,1
            #self.ids['msg_error'].text =  "%s%s_foto.png salva com sucesso!"%(name_trans,name_fx)
        except:
            self.ids['msg_error'].text = ''
            self.ids['msg_error'].color = 1,0,0,1
            self.ids['msg_error'].text = 'Selecione o transecto e a faixa!'





class Camera_check(Screen):
    #name_trans = ''
    name_fx = ''
    def load_image(self):

        global name_trans
        global name_fx
        path = str(os.path.abspath(os.path.dirname(__file__)))
        try:
            name_trans and name_fx
            im = self.ids['imageView']
            im.source = path+"/fotos/%s%s_foto.png"%(name_trans,name_fx)
            #im = Image(source = "data/Trans01_CRACA_foto.png")
            im.reload()
            self.ids['msg_error'].text = ''
            self.ids['msg_error'].color = 0,1,0,1
            self.ids['msg_error'].text =  "%s%s_foto.png"%(name_trans,name_fx)
        except:
            self.ids['msg_error'].text = ''
            self.ids['msg_error'].color = 1,0,0,1
            self.ids['msg_error'].text = 'Selecione o transecto e a faixa!'

    def reset (self):
        self.ids['msg_error'].text = ''
        im = self.ids['imageView']
        im.source = path+"/icon.png"

class Faixa1(Screen):
    #MELHORAR
    #name_trans = ''
    name_fx = ''

    objects = []
    cracas =[]
    ostras=[]
    algas=[]
    rochas=[]
    count = NumericProperty()
    del_c =NumericProperty()
    del_a =NumericProperty()
    del_o =NumericProperty()
    del_r =NumericProperty()

    ind_c = NumericProperty()
    ind_a = NumericProperty()
    ind_o = NumericProperty()
    ind_r = NumericProperty()
    total = NumericProperty()
    drawing = False

    def new_craca(self):
        self.ids['fx1_craca'].color = 1.,1.,1., 1
        self.ids['fx1_ostra'].color = 1.,1.,1., 0.6
        self.ids['fx1_alga'].color = 1.,1.,1., 0.6
        self.ids['fx1_rocha'].color = 1.,1.,1., 0.6
        #self.ids['fx1_outro'].color = 1.,1.,1., 0.6
    def new_ostra(self):
        self.ids['fx1_craca'].color = 1.,1.,1., 0.6
        self.ids['fx1_ostra'].color = 1.,1.,1., 1
        self.ids['fx1_alga'].color = 1.,1.,1., 0.6
        self.ids['fx1_rocha'].color = 1.,1.,1., 0.6
        #self.ids['fx1_outro'].color = 1.,1.,1., 0.6
    def new_alga(self):
        self.ids['fx1_craca'].color = 1.,1.,1., 0.6
        self.ids['fx1_ostra'].color = 1.,1.,1., 0.6
        self.ids['fx1_alga'].color = 1.,1.,1., 1
        self.ids['fx1_rocha'].color = 1.,1.,1., 0.6
        #self.ids['fx1_outro'].color = 1.,1.,1., 0.6
    def new_rocha(self):
        self.ids['fx1_craca'].color = 1.,1.,1., 0.6
        self.ids['fx1_ostra'].color = 1.,1.,1., 0.6
        self.ids['fx1_alga'].color = 1.,1.,1.,0.6
        self.ids['fx1_rocha'].color = 1.,1.,1., 1
        #self.ids['fx1_outro'].color = 1.,1.,1., 0.6

    def load_image(self):
        path = str(os.path.abspath(os.path.dirname(__file__)))
        global name_trans
        global name_fx
        try:
            name_trans and name_fx
            im = self.ids['imageView']
            im.source = path+"/fotos/%sfaixa01_foto.png"%(name_trans)
            #im = Image(source = "data/Trans01_CRACA_foto.png")
            im.reload()
            #self.ids['fx1_msg_error'].text = ''
            #self.ids['fx1_msg_error'].color = 0,1,0,1
            #self.ids['fx1_msg_error'].text =  "%s%s_foto.png aberta com sucesso!"%(name_trans,name_fx)
        except:
            print('erro')
            self.ids['fx1_msg_error'].text = ''
            self.ids['fx1_msg_error'].color = 1,0,0,1
            self.ids['fx1_msg_error'].text = 'Selecione o transecto e a faixa!'



    def salvar(self):
        path = str(os.path.abspath(os.path.dirname(__file__)))
        self.ids['fx1_msg_error'].text = ''
        self.ids['fx1_msg_error'].color = 0,1,1,1
        self.ids['fx1_msg_error'].text = 'salvando no banco de dados ...'
        global name_trans
        global name_fx
        try:
            name_trans and name_fx
            self.export_to_png(path+"/fotos/%sfaixa01_data.png"%(name_trans))
        except:
            print('erro')
            self.parent.current= 'trans'

    def add_craca(self, *largs):
            count =1
            with self.canvas:
                for x in range(1):
                    #self.rect = Rectangle(pos = self.center,size=(self.width/2.,self.height/2.))
                    self.obj = InstructionGroup()
                    self.c =Circle_C(pos = (300,800),size = (50,50))
                    self.add_widget(self.c)
                    self.obj.add(Color(1,0.8,0,1))
                    self.objects.append(self.obj)
                    self.cracas.append(self.obj)
                    self.ind_c +=1
                    #print ('craca = %d'%self.ind_c)
                    total = self.ids['sumT']
                    if int(total.text) == 49:
                        self.ids['sumT'].color = [1,0,0,1]
                        total.text = str(int(total.text)+1)
                    elif total.text == "50":
                        self.objects.pop(-1)
                        self.obj.add(Color(0,0,0,0.001))
                        self.ind_c -=1
                    else:
                        total.text = str(int(total.text)+1)
                        self.ids['sumT'].color = [1,1,1,1]

    def add_ostra(self,*largs):
            count =1
            with self.canvas:
                for x in range(1):
                    self.obj = InstructionGroup()
                    self.o =Circle_C(pos = (400,800),size = (50,50))
                    self.add_widget(self.o)
                    self.obj.add(Color(0.5,0,0.5,0.7))
                    self.objects.append(self.obj)
                    self.ostras.append(self.obj)
                    self.ind_o +=1
                    #print ('ostra = %d'%self.ind_o)
                    total = self.ids['sumT']
                    if int(total.text) == 49:
                        self.ids['sumT'].color = [1,0,0,1]
                        total.text = str(int(total.text)+1)
                    elif total.text == "50":
                        self.objects.pop(-1)
                        self.obj.add(Color(0,0,0,0.001))
                        self.ind_o -=1
                    else:
                        total.text = str(int(total.text)+1)
                        self.ids['sumT'].color = [1,1,1,1]

    def add_alga(self, *largs):
            count =1
            with self.canvas:
                for x in range(1):
                    self.obj = InstructionGroup()
                    self.a =Circle_C(pos = (500,800),size = (50,50))
                    self.add_widget(self.a)
                    self.obj.add(Color(0,1,0,0.7))
                    self.objects.append(self.obj)
                    self.algas.append(self.obj)
                    self.ind_a +=1
                    #print ('alga = %d'%self.ind_a)
                    total = self.ids['sumT']
                    if int(total.text) == 49:
                        self.ids['sumT'].color = [1,0,0,1]
                        total.text = str(int(total.text)+1)
                    elif total.text == "50":
                        self.objects.pop(-1)
                        self.obj.add(Color(0,0,0,0.001))
                        self.ind_a -=1
                    else:
                        total.text = str(int(total.text)+1)
                        self.ids['sumT'].color = [1,1,1,1]

    def add_RN(self, *largs):
            count =1
            with self.canvas:
                for x in range(count):
                    self.obj = InstructionGroup()
                    self.r =Circle_C(pos = (600,800),size = (50,50))
                    self.add_widget(self.r)
                    self.obj.add(Color(1,1,1,0.7))
                    self.objects.append(self.obj)
                    self.rochas.append(self.obj)
                    self.ind_r +=1
                    #print ('rocha = %d'%self.ind_r)
                    total = self.ids['sumT']
                    if int(total.text) == 49:
                        self.ids['sumT'].color = [1,0,0,1]
                        total.text = str(int(total.text)+1)
                    elif total.text == "50":
                        self.objects.pop(-1)
                        self.obj.add(Color(0,0,0,0.001))
                        self.ind_r -=1
                    else:
                        total.text = str(int(total.text)+1)
                        self.ids['sumT'].color = [1,1,1,1]


    def undo(self, *args):
        #self.remove_widget(self.c)
        try:
            #print(self.objects)
            self.ids['sumT'].color = [1,1,1,1]
            item = self.objects[-1]
            #print (item)
            item.add(Color(0,0,0,0.001))
            self.objects.pop(-1)
            self.obj.add(Color(0,0,0,0.001))
            total = self.ids['sumT']
            total.text = str(int(total.text)-1)
            #print(item in self.cracas == True)
            if item in self.cracas :
                self.ind_c -=1
            elif item in self.ostras :
                self.ind_o -=1
            elif item in self.algas :
                self.ind_a -=1
            elif item in self.rochas:
                self.ind_r -=1
            print ('craca = %d'%self.ind_c)
            print ('ostra = %d'%self.ind_o)
            print ('alga = %d'%self.ind_a)
            print ('rocha = %d'%self.ind_r)

        except:
            print ('error')

    def add_firebase(self):
            "connect to firebase"
            import os
            global name_trans

            path = str(os.path.abspath(os.path.dirname(__file__)))
            localId = pickle.load( open(  path+"/localId.p", "rb" ) )
            id_coleta = pickle.load( open( path+ "/id_coleta.p", "rb" ) )
            idToken = pickle.load( open(  path+"/id_Token.p", "rb" ) )
            #bd = firebase.FirebaseApplication('https://deolhonacosta-2019.firebaseio.com/users/'+localId+id_coleta, authentication=None)
            total = self.ind_c +self.ind_o +self.ind_a +self.ind_r
            user_data = '{"fx1":{"craca":"%s","ostra":"%s","alga":"%s","rocha":"%s","total":"%s"}}'%(self.ind_c,self.ind_o,self.ind_a,self.ind_r, total)
            post_request = requests.patch('https://deolhonacosta-2019.firebaseio.com/users/%s/%s/%s/'%(localId,id_coleta,name_trans) + ".json?auth=" + idToken,
                                data=user_data)
    def reset(self):
        for item in self.algas:
            item.add(Color(0,0,0,0.001))
        self.algas =[]
        for item in self.cracas:
            item.add(Color(0,0,0,0.001))
        self.cracas =[]
        for item in self.ostras:
            item.add(Color(0,0,0,0.001))
        self.ostras =[]
        for item in self.rochas:
            item.add(Color(0,0,0,0.001))
        self.rochas =[]
        #print(self.rochas)
        total = self.ids['sumT']
        total.text = '0'
        im = self.ids['imageView']
        try:
            im
            im.source = ''
        except:
            self.ids['fx1_msg_error'].text = ''
            self.ids['fx1_msg_error'].color = 1,0,0,1
            #self.ids['fx1_msg_error'].text = 'Nenhuma imagem carregada.'

class Faixa2(Screen):
    #MELHORAR
    #name_trans = ''

    objects = []
    cracas =[]
    ostras=[]
    algas=[]
    rochas=[]
    count = NumericProperty()
    del_c =NumericProperty()
    del_a =NumericProperty()
    del_o =NumericProperty()
    del_r =NumericProperty()

    ind_c = NumericProperty()
    ind_a = NumericProperty()
    ind_o = NumericProperty()
    ind_r = NumericProperty()
    total = NumericProperty()
    drawing = False

    def new_craca(self):
        self.ids['fx2_craca'].color = 1.,1.,1., 1
        self.ids['fx2_ostra'].color = 1.,1.,1., 0.6
        self.ids['fx2_alga'].color = 1.,1.,1., 0.6
        self.ids['fx2_rocha'].color = 1.,1.,1., 0.6
        #self.ids['fx1_outro'].color = 1.,1.,1., 0.6
    def new_ostra(self):
        self.ids['fx2_craca'].color = 1.,1.,1., 0.6
        self.ids['fx2_ostra'].color = 1.,1.,1., 1
        self.ids['fx2_alga'].color = 1.,1.,1., 0.6
        self.ids['fx2_rocha'].color = 1.,1.,1., 0.6
        #self.ids['fx1_outro'].color = 1.,1.,1., 0.6
    def new_alga(self):
        self.ids['fx2_craca'].color = 1.,1.,1., 0.6
        self.ids['fx2_ostra'].color = 1.,1.,1., 0.6
        self.ids['fx2_alga'].color = 1.,1.,1., 1
        self.ids['fx2_rocha'].color = 1.,1.,1., 0.6
        #self.ids['fx1_outro'].color = 1.,1.,1., 0.6
    def new_rocha(self):
        self.ids['fx2_craca'].color = 1.,1.,1., 0.6
        self.ids['fx2_ostra'].color = 1.,1.,1., 0.6
        self.ids['fx2_alga'].color = 1.,1.,1.,0.6
        self.ids['fx2_rocha'].color = 1.,1.,1., 1
        #self.ids['fx1_outro'].color = 1.,1.,1., 0.6



    def load_image(self):
        path = str(os.path.abspath(os.path.dirname(__file__)))
        global name_trans
        global name_fx
        try:
            name_trans and name_fx
            im = self.ids['imageView']
            im.source = path+"/fotos/%sfaixa02_foto.png"%(name_trans)
            #im = Image(source = "data/Trans01_CRACA_foto.png")
            im.reload()
            #self.ids['fx2_msg_error'].text = ''
            #self.ids['fx2_msg_error'].color = 0,1,0,1
            #self.ids['fx2_msg_error'].text =  "%s%s_foto.png aberta com sucesso!"%(name_trans,name_fx)
        except:
            print('erro')
            self.ids['fx2_msg_error'].text = ''
            self.ids['fx2_msg_error'].color = 1,0,0,1
            self.ids['fx2_msg_error'].text = 'Selecione o transecto e a faixa!'



    def salvar(self):
        path = str(os.path.abspath(os.path.dirname(__file__)))
        self.ids['fx2_msg_error'].text = ''
        self.ids['fx2_msg_error'].color = 0,1,1,1
        self.ids['fx2_msg_error'].text = 'salvando no banco de dados ...'
        global name_trans
        global name_fx
        try:
            name_trans and name_fx
            self.export_to_png(path+"/fotos/%sfaixa02_data.png"%(name_trans))
        except:
            print('erro')
            self.parent.current= 'trans'


    def add_craca(self, *largs):
            count =1
            with self.canvas:
                for x in range(1):
                    self.obj = InstructionGroup()
                    self.c =Circle_C(pos = (300,800),size = (50,50))
                    self.add_widget(self.c)
                    self.obj.add(Color(1,0.8,0,1))
                    self.objects.append(self.obj)
                    self.cracas.append(self.obj)
                    self.ind_c +=1
                    #print ('craca = %d'%self.ind_c)
                    total = self.ids['sumT']
                    if int(total.text) == 49:
                        self.ids['sumT'].color = [1,0,0,1]
                        total.text = str(int(total.text)+1)
                    elif total.text == "50":
                        self.objects.pop(-1)
                        self.obj.add(Color(0,0,0,0.001))
                        self.ind_c -=1
                    else:
                        total.text = str(int(total.text)+1)
                        self.ids['sumT'].color = [1,1,1,1]

    def add_ostra(self,*largs):
            count =1
            with self.canvas:
                for x in range(1):
                    self.obj = InstructionGroup()
                    self.o =Circle_C(pos = (400,800),size = (50,50))
                    self.add_widget(self.o)
                    self.obj.add(Color(0.5,0,0.5,0.7))
                    self.objects.append(self.obj)
                    self.ostras.append(self.obj)
                    self.ind_o +=1
                    #print ('ostra = %d'%self.ind_o)
                    total = self.ids['sumT']
                    if int(total.text) == 49:
                        self.ids['sumT'].color = [1,0,0,1]
                        total.text = str(int(total.text)+1)
                    elif total.text == "50":
                        self.objects.pop(-1)
                        self.obj.add(Color(0,0,0,0.001))
                        self.ind_o -=1
                    else:
                        total.text = str(int(total.text)+1)
                        self.ids['sumT'].color = [1,1,1,1]

    def add_alga(self, *largs):
            count =1
            with self.canvas:
                for x in range(1):
                    self.obj = InstructionGroup()
                    self.a =Circle_C(pos = (500,800),size = (50,50))
                    self.add_widget(self.a)
                    self.obj.add(Color(0,1,0,0.7))
                    self.objects.append(self.obj)
                    self.algas.append(self.obj)
                    self.ind_a +=1
                    #print ('alga = %d'%self.ind_a)
                    total = self.ids['sumT']
                    if int(total.text) == 49:
                        self.ids['sumT'].color = [1,0,0,1]
                        total.text = str(int(total.text)+1)
                    elif total.text == "50":
                        self.objects.pop(-1)
                        self.obj.add(Color(0,0,0,0.001))
                        self.ind_a -=1
                    else:
                        total.text = str(int(total.text)+1)
                        self.ids['sumT'].color = [1,1,1,1]

    def add_RN(self, *largs):
            count =1
            with self.canvas:
                for x in range(count):
                    self.obj = InstructionGroup()
                    self.r =Circle_C(pos = (600,800),size = (50,50))
                    self.add_widget(self.r)
                    self.obj.add(Color(1,1,1,0.7))
                    self.objects.append(self.obj)
                    self.rochas.append(self.obj)
                    self.ind_r +=1
                    #print ('rocha = %d'%self.ind_r)
                    total = self.ids['sumT']
                    if int(total.text) == 49:
                        self.ids['sumT'].color = [1,0,0,1]
                        total.text = str(int(total.text)+1)
                    elif total.text == "50":
                        self.objects.pop(-1)
                        self.obj.add(Color(0,0,0,0.001))
                        self.ind_r -=1
                    else:
                        total.text = str(int(total.text)+1)
                        self.ids['sumT'].color = [1,1,1,1]


    def undo(self, *args):
        #self.remove_widget(self.c)
        try:
            #print(self.objects)
            self.ids['sumT'].color = [1,1,1,1]
            item = self.objects[-1]
            #print (item)
            item.add(Color(0,0,0,0.001))
            self.objects.pop(-1)
            self.obj.add(Color(0,0,0,0.001))
            total = self.ids['sumT']
            total.text = str(int(total.text)-1)
            #print(item in self.cracas == True)
            if item in self.cracas :
                self.ind_c -=1
            elif item in self.ostras :
                self.ind_o -=1
            elif item in self.algas :
                self.ind_a -=1
            elif item in self.rochas:
                self.ind_r -=1
            print ('craca = %d'%self.ind_c)
            print ('ostra = %d'%self.ind_o)
            print ('alga = %d'%self.ind_a)
            print ('rocha = %d'%self.ind_r)

        except:
            print ('error')

    def add_firebase(self):
            "connect to firebase"
            import os
            global name_trans
            path = str(os.path.abspath(os.path.dirname(__file__)))
            localId = pickle.load( open(  path+"/localId.p", "rb" ) )
            id_coleta = pickle.load( open( path+ "/id_coleta.p", "rb" ) )
            idToken = pickle.load( open(  path+"/id_Token.p", "rb" ) )
            #bd = firebase.FirebaseApplication('https://deolhonacosta-2019.firebaseio.com/users/'+localId+id_coleta, authentication=None)
            total = self.ind_c +self.ind_o +self.ind_a +self.ind_r
            user_data = '{"fx2":{"craca":"%s","ostra":"%s","alga":"%s","rocha":"%s","total":"%s"}}'%(self.ind_c,self.ind_o,self.ind_a,self.ind_r, total)
            post_request = requests.patch('https://deolhonacosta-2019.firebaseio.com/users/%s/%s/%s/'%(localId,id_coleta,name_trans) + ".json?auth=" + idToken,
                                data=user_data)
    def reset(self):
        for item in self.algas:
            item.add(Color(0,0,0,0.001))
        self.algas =[]
        for item in self.cracas:
            item.add(Color(0,0,0,0.001))
        self.cracas =[]
        for item in self.ostras:
            item.add(Color(0,0,0,0.001))
        self.ostras =[]
        for item in self.rochas:
            item.add(Color(0,0,0,0.001))
        self.rochas =[]
        #print(self.rochas)
        total = self.ids['sumT']
        total.text = '0'
        im = self.ids['imageView']
        try:
            im
            im.source = ''
        except:
            self.ids['fx2_msg_error'].text = ''
            self.ids['fx2_msg_error'].color = 1,0,0,1
            #self.ids['fx2_msg_error'].text = 'Nenhuma imagem carregada.'
        #with self.canvas.before:
        #    Color(0.531,0.5546,0.6172,0.7, mode='rgba')
        #    self.rect = Rectangle(pos=self.pos, size=self.size)


class Faixa3(Screen):
    #MELHORAR
    #name_trans = ''

    objects = []
    cracas =[]
    ostras=[]
    algas=[]
    rochas=[]
    count = NumericProperty()
    del_c =NumericProperty()
    del_a =NumericProperty()
    del_o =NumericProperty()
    del_r =NumericProperty()

    ind_c = NumericProperty()
    ind_a = NumericProperty()
    ind_o = NumericProperty()
    ind_r = NumericProperty()
    total = NumericProperty()
    drawing = False

    def new_craca(self):
        self.ids['fx3_craca'].color = 1.,1.,1., 1
        self.ids['fx3_ostra'].color = 1.,1.,1., 0.6
        self.ids['fx3_alga'].color = 1.,1.,1., 0.6
        self.ids['fx3_rocha'].color = 1.,1.,1., 0.6
        #self.ids['fx1_outro'].color = 1.,1.,1., 0.6
    def new_ostra(self):
        self.ids['fx3_craca'].color = 1.,1.,1., 0.6
        self.ids['fx3_ostra'].color = 1.,1.,1., 1
        self.ids['fx3_alga'].color = 1.,1.,1., 0.6
        self.ids['fx3_rocha'].color = 1.,1.,1., 0.6
        #self.ids['fx1_outro'].color = 1.,1.,1., 0.6
    def new_alga(self):
        self.ids['fx3_craca'].color = 1.,1.,1., 0.6
        self.ids['fx3_ostra'].color = 1.,1.,1., 0.6
        self.ids['fx3_alga'].color = 1.,1.,1., 1
        self.ids['fx3_rocha'].color = 1.,1.,1., 0.6
        #self.ids['fx1_outro'].color = 1.,1.,1., 0.6
    def new_rocha(self):
        self.ids['fx3_craca'].color = 1.,1.,1., 0.6
        self.ids['fx3_ostra'].color = 1.,1.,1., 0.6
        self.ids['fx3_alga'].color = 1.,1.,1.,0.6
        self.ids['fx3_rocha'].color = 1.,1.,1., 1
        #self.ids['fx1_outro'].color = 1.,1.,1., 0.6



    def load_image(self):
        path = str(os.path.abspath(os.path.dirname(__file__)))
        global name_trans
        global name_fx
        try:
            name_trans and name_fx
            im = self.ids['imageView']
            im.source = path+"/fotos/%sfaixa03_foto.png"%(name_trans)
            #im = Image(source = "data/Trans01_CRACA_foto.png")
            im.reload()
            #self.ids['fx3_msg_error'].text = ''
            #self.ids['fx3_msg_error'].color = 0,1,0,1
            #self.ids['fx3_msg_error'].text =  "%s%s_foto.png aberta com sucesso!"%(name_trans,name_fx)
        except:
            print('erro')
            self.ids['fx3_msg_error'].text = ''
            self.ids['fx3_msg_error'].color = 1,0,0,1
            self.ids['fx3_msg_error'].text = 'Selecione o transecto e a faixa!'


    def salvar(self):
        path = str(os.path.abspath(os.path.dirname(__file__)))
        self.ids['fx3_msg_error'].text = ''
        self.ids['fx3_msg_error'].color = 0,1,1,1
        self.ids['fx3_msg_error'].text = 'salvando no banco de dados ...'
        global name_trans
        global name_fx
        try:
            name_trans and name_fx
            self.export_to_png(path+"/fotos/%sfaixa03_data.png"%(name_trans))
        except:
            print('erro')
            self.parent.current= 'trans'


    def add_craca(self, *largs):
            count =1
            with self.canvas:
                for x in range(1):
                    self.obj = InstructionGroup()
                    self.c =Circle_C(pos = (300,800),size = (50,50))
                    self.add_widget(self.c)
                    self.obj.add(Color(1,0.8,0,1))
                    self.objects.append(self.obj)
                    self.cracas.append(self.obj)
                    self.ind_c +=1
                    #print ('craca = %d'%self.ind_c)
                    total = self.ids['sumT']
                    if int(total.text) == 49:
                        self.ids['sumT'].color = [1,0,0,1]
                        total.text = str(int(total.text)+1)
                    elif total.text == "50":
                        self.objects.pop(-1)
                        self.obj.add(Color(0,0,0,0.001))
                        self.ind_c -=1
                    else:
                        total.text = str(int(total.text)+1)
                        self.ids['sumT'].color = [1,1,1,1]

    def add_ostra(self,*largs):
            count =1
            with self.canvas:
                for x in range(1):
                    self.obj = InstructionGroup()
                    self.o =Circle_C(pos = (400,800),size = (50,50))
                    self.add_widget(self.o)
                    self.obj.add(Color(0.5,0,0.5,0.7))
                    self.objects.append(self.obj)
                    self.ostras.append(self.obj)
                    self.ind_o +=1
                    #print ('ostra = %d'%self.ind_o)
                    total = self.ids['sumT']
                    if int(total.text) == 49:
                        self.ids['sumT'].color = [1,0,0,1]
                        total.text = str(int(total.text)+1)
                    elif total.text == "50":
                        self.objects.pop(-1)
                        self.obj.add(Color(0,0,0,0.001))
                        self.ind_o -=1
                    else:
                        total.text = str(int(total.text)+1)
                        self.ids['sumT'].color = [1,1,1,1]

    def add_alga(self, *largs):
            count =1
            with self.canvas:
                for x in range(1):
                    self.obj = InstructionGroup()
                    self.a =Circle_C(pos = (500,800),size = (50,50))
                    self.add_widget(self.a)
                    self.obj.add(Color(0,1,0,0.7))
                    self.objects.append(self.obj)
                    self.algas.append(self.obj)
                    self.ind_a +=1
                    #print ('alga = %d'%self.ind_a)
                    total = self.ids['sumT']
                    if int(total.text) == 49:
                        self.ids['sumT'].color = [1,0,0,1]
                        total.text = str(int(total.text)+1)
                    elif total.text == "50":
                        self.objects.pop(-1)
                        self.obj.add(Color(0,0,0,0.001))
                        self.ind_a -=1
                    else:
                        total.text = str(int(total.text)+1)
                        self.ids['sumT'].color = [1,1,1,1]

    def add_RN(self, *largs):
            count =1
            with self.canvas:
                for x in range(count):
                    self.obj = InstructionGroup()
                    self.r =Circle_C(pos = (600,800),size = (50,50))
                    self.add_widget(self.r)
                    self.obj.add(Color(1,1,1,0.7))
                    self.objects.append(self.obj)
                    self.rochas.append(self.obj)
                    self.ind_r +=1
                    #print ('rocha = %d'%self.ind_r)
                    total = self.ids['sumT']
                    if int(total.text) == 49:
                        self.ids['sumT'].color = [1,0,0,1]
                        total.text = str(int(total.text)+1)
                    elif total.text == "50":
                        self.objects.pop(-1)
                        self.obj.add(Color(0,0,0,0.001))
                        self.ind_r -=1
                    else:
                        total.text = str(int(total.text)+1)
                        self.ids['sumT'].color = [1,1,1,1]


    def undo(self, *args):
        #self.remove_widget(self.c)
        try:
            #print(self.objects)
            self.ids['sumT'].color = [1,1,1,1]
            item = self.objects[-1]
            #print (item)
            item.add(Color(0,0,0,0.001))
            self.objects.pop(-1)
            self.obj.add(Color(0,0,0,0.001))
            total = self.ids['sumT']
            total.text = str(int(total.text)-1)
            #print(item in self.cracas == True)
            if item in self.cracas :
                self.ind_c -=1
            elif item in self.ostras :
                self.ind_o -=1
            elif item in self.algas :
                self.ind_a -=1
            elif item in self.rochas:
                self.ind_r -=1
            print ('craca = %d'%self.ind_c)
            print ('ostra = %d'%self.ind_o)
            print ('alga = %d'%self.ind_a)
            print ('rocha = %d'%self.ind_r)

        except:
            print ('error')

    def add_firebase(self):
            "connect to firebase"
            import os
            global name_trans
            path = str(os.path.abspath(os.path.dirname(__file__)))
            localId = pickle.load( open(  path+"/localId.p", "rb" ) )
            id_coleta = pickle.load( open( path+ "/id_coleta.p", "rb" ) )
            idToken = pickle.load( open(  path+"/id_Token.p", "rb" ) )
            #bd = firebase.FirebaseApplication('https://deolhonacosta-2019.firebaseio.com/users/'+localId+id_coleta, authentication=None)
            total = self.ind_c +self.ind_o +self.ind_a +self.ind_r
            user_data = '{"fx3":{"craca":"%s","ostra":"%s","alga":"%s","rocha":"%s","total":"%s"}}'%(self.ind_c,self.ind_o,self.ind_a,self.ind_r, total)
            post_request = requests.patch('https://deolhonacosta-2019.firebaseio.com/users/%s/%s/%s/'%(localId,id_coleta,name_trans) + ".json?auth=" + idToken,
                                data=user_data)
    def reset(self):
        for item in self.algas:
            item.add(Color(0,0,0,0.001))
        self.algas =[]
        for item in self.cracas:
            item.add(Color(0,0,0,0.001))
        self.cracas =[]
        for item in self.ostras:
            item.add(Color(0,0,0,0.001))
        self.ostras =[]
        for item in self.rochas:
            item.add(Color(0,0,0,0.001))
        self.rochas =[]
        #print(self.rochas)
        total = self.ids['sumT']
        total.text = '0'
        im = self.ids['imageView']
        try:
            im
            im.source = ''
        except:
            self.ids['fx3_msg_error'].text = ''
            self.ids['fx3_msg_error'].color = 1,0,0,1
            #self.ids['fx3_msg_error'].text = 'Nenhuma imagem carregada.'



class Final(Screen):
    lat= NumericProperty()
    lon= NumericProperty()

    def mapa(self):
        import os


        #coleta = LocalColeta()
        path = str(os.path.abspath(os.path.dirname(__file__)))
        #print (coleta.lat, coleta.lon)
        self.lat= pickle.load( open(  path+"/LAT.p", "rb" ) )#-23.9737785
        self.lon= pickle.load( open(  path+"/LON.p", "rb" ) )#-46.3525725
        print(self.lat,self.lon)
        #self.root.mapview.ids.lat = coleta.lat
        #self.root.mapview.ids.lon = coleta.lon
        #self.app.root.mapview.center_on(self.lat, self.lon)
        list = os.listdir(path+"/fotos")
        marker = self.ids['final_popup_mark']
        marker.text = "você contribuiu com: \n %d fotos"%len(list)
        self.ids['mapview'].center_on(self.lat+0.05, self.lon)
        self.ids['mapview'].zoom = 12
        #self.ids['mapmarker1'].source = 'maps/MapNow.png'
        # send to gmail







    def nova_coleta(self):
        import glob
        path = str(os.path.abspath(os.path.dirname(__file__)))
        os.remove(path + "/LAT.p")
        os.remove(path + "/LON.p")

        id_coleta = pickle.load( open( path+ "/id_coleta.p", "rb" ) )
        ind = int(id_coleta[7:10])+1
        if (int(id_coleta[7:10]) + 1) <10:
            id_coleta = "coleta_00" + str(ind)
        elif (int(id_coleta[7:10]) + 1) >=9:
            id_coleta = "coleta_0" + str(ind)
        elif (int(id_check[7:10]) + 1) >=99:
            id_coleta = "coleta_" + str (ind)
        print(id_coleta)
        pickle.dump( id_coleta, open( path+ "/id_coleta.p", "wb" ) )
        #l = LoginPage()
        #l.ids['login_email'].text =''
        #l.ids['login_password'].text =''
        global name_trans
        name_trans = 'trans01'
        #self.ids['trans_id'].text = name_trans



#GUI = Builder.load_file("main.kv")
path = str(os.path.abspath(os.path.dirname(__file__)))
GUI = Builder.load_file(path+ '/main.kv')
print (path+ '/main.kv')



class LegecApp(App):
    #url = 'https://deolhonacosta-2019.firebaseio.com'
    #rm no dir data


    def build(self):
        self.icon = 'figs/legec_logo.png'
        self.title = 'deolhonacosta-2019'
        #from android.permissions import request_permission,Permission
        return GUI

    def change_screen(self, screen_name):
        screen_manager = self.root.ids['screen_manager']
        screen_manager.current = screen_name





LegecApp().run()
