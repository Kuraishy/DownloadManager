from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys

import os
import os.path
import urllib.request
from PyQt5.uic import loadUiType
import pafy
import re

#pyrcc5 -o output.py input.qrc


ui,_=loadUiType('ui/main.ui')#crea la carga del ui apartir del template

class MainApp(QMainWindow, ui):#QMainWindow porque esta hecho en main window
    #carga la clase ui externa
    def __init__(self, parent=None):
        super(MainApp, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.tabWidget.setCurrentIndex(0)
        self.InitUI()
        self.Handel_Buttons()


    def InitUI(self):
        # contail all changes in loading
        self.tabWidget.tabBar().setVisible(False)


    def Handel_Buttons(self):
        #Handel button
        self.bn_DescargaPrincipal.clicked.connect(self.Download) #se conecta el boton de descarga principal con downlaod
        self.bn_GurardadoPrincipal.clicked.connect(self.Handel_Browse)
        self.bn_YoutubeBusqueda.clicked.connect(self.Get_Video_Data)
        self.bn_youtubeDir.clicked.connect(self.Save_Browse)
        self.bn_YoutubeDownload.clicked.connect(self.Download_Video)
        self.bn_PlaylistDownload.clicked.connect(self.Playlist_Download)
        self.Dummy.clicked.connect(self.DuumyBn)
        self.bn_GuardadoPlaylist.clicked.connect(self.Playlist_Save_Browse)

        self.bn_Home.clicked.connect(self.Open_Home)
        self.bn_Download.clicked.connect(self.Open_Download)
        self.bn_Youtube.clicked.connect(self.Open_Youtube)
        self.bn_Settings.clicked.connect(self.Open_Settings)

        self.pushButton_3.clicked.connect(self.Apply_Dark_Style)




    def Handel_Progress(self , blocknum , blocksize , totalsize): # se obtiene del urlib
        #calcula el progreso
        print(blocknum)
        print(blocksize)
        print(totalsize)

        readed_data = blocknum * blocksize # cuanto del data se ha leido

        if totalsize > 0: #si es valida la descarga
            download_percentage = readed_data * 100 / totalsize #saca el porcentaje del progreso
            print(download_percentage)
            self.progressBar.setValue(round(download_percentage)) #asigna el progreso
            QApplication.processEvents()#sera la ui responsiva sino se atora al acutaliza


    # permiite el browsing, escoge donde guarda la descarga
    def Handel_Browse(self):
        save_location = QFileDialog.getSaveFileName(self , directory="." ) #se abre el pop up de donde guardar en el directorio dentro de la carpeta
        self.txt_SaveUrl.setText(str(save_location[0]))


    def Download(self):
        #cuando descarga archivos
        #obetern y guardar la url
        save_url = self.txt_SaveUrl.text()
        download_url = self.txt_DownloadUrl.text()

        #si nos pasa un url o direccion vacia
        if download_url == '' or save_url == '':
            QMessageBox.warning(self , "Error en la Data OwO" , " Valide la direccion de descarga o de guardado :) ") #pop up de error
        else:
            #ver si la direccion url de descarga es valida
            try:
                urllib.request.urlretrieve(download_url , save_url , self.Handel_Progress) #saca la informacion del url como el tamaño etc
            except Exception:
                QMessageBox.warning(self, "Error en la Descarga OwO" , " Direccion URL de descarga no valida UwU ")  # pop up de error
                return
        #cuando la descarga es exitosa y se reinician los parametros
        QMessageBox.information(self , "Descarga Completa" , "Se ha completado la descarga")
        self.txt_SaveUrl.setTextext('')
        self.txt_DownloadUrl.setText('')
        self.progressBar.setValue(0)
        print(save_url)
        print(download_url)




    #########################################
    #####Descarga de youtube Unitario########
    def Get_Video_Data(self):
        video_url = self.url_Youtube.text()
        if video_url == '':
            QMessageBox.warning(self, "Error en el link OwO", " Valide la direccion del video")
        else:
            video = pafy.new(video_url) #obtiene informacion del video
            print(video.title)
            print(video.duration)
            video_stream = video.videostreams #los diferentes tipos de calidades y formatos del video

            #por cada formado y calidad encontrado
            for stream in video_stream:
                size = stream.get_filesize() #se obtiene el peso del video en ese formato
                #print("mio: " + self.format_bytes(size))
                data = "{} {} {} {} ".format(stream.mediatype, stream.extension, stream.quality, self.format_bytes(size))
                self.cb_Youtube.addItem(data)


    def Download_Video(self):
     video_url = self.url_Youtube.text()
     save_location = self.txt_YoutubeSave.text()
     print("tesmp")
     # si nos pasa un url o direccion vacia
     if video_url == '' or save_location == '':
         QMessageBox.warning(self, "Error en la Data OwO"," Valide la direccion del video o de guardado :) ")  # pop up de error
     else:
         # ver si la direccion url de descarga es valida
         video = pafy.new(video_url)
         video_stream = video.videostreams
         video_quality = self.cb_Youtube.currentIndex()
        # download = video_stream[video_quality].download(filepath= save_location , callback= self.Video_Progess)
         video_stream[video_quality].download(filepath=save_location , callback = self.Video_Progess)
         QMessageBox.information(self, "Descarga Completa", "Se ha completado la descarga")


    def Save_Browse(self): #mismo que el handle browser pero con otro text
        # guarda la localizacion de donde guardar
        save_location = QFileDialog.getSaveFileName(self , directory="." ) #se abre el pop up de donde guardar en el directorio dentro de la carpeta
        self.txt_YoutubeSave.setText(str(save_location[0]))


    def Video_Progess(self , total , receive , ratio , rate , time): #del callback recive los parametros
        readed_date = receive
        if total > 0:
            #cambia el progreso a barra
            download_percentage = readed_date * 100 / total
            self.pb_Youtube.setValue(round(download_percentage))
            #calcula el tiempo restante y lo imprime
            remaining_time= round(time/60 , 2)
            print(self.format_bytes(rate*1000) + '/s')
            self.lb_YoutubeTimes.setText(str(remaining_time) + ' minutos restantes' + ' ' + self.format_bytes(rate*1000) + '/s')
            QApplication.processEvents()  # sera la ui responsiva sino se atora al acutaliza


    ##########################################################################################################################
    #############PLAYLIST###############
    ###########################################

    def Playlist_Download(self):
        playlistUrl = self.ln_PlaylistUrl.text()
        save_location = self.ln_PlaylistSave.text()

        if playlistUrl == '' or save_location == '':
            QMessageBox.warning(self, "Error en la Data OwO", " Valide la direccion del playlist o de guardado :) ")
        else:
           playlist=pafy.get_playlist(playlistUrl)
           playlist_videos = playlist['items']
           print(len(playlist_videos))
           #self.lcd_PlaylistLength.display(len(playlist_videos))

           self.lcd_PlaylistLength.display(len(playlist_videos))
           self.lcdNumber.display(1)
           #lcd_PlaylistNumber

        #cambia a la direccion de guardado y si existe
        #el path del folder de la playlist
        #cmbia a la direccion dentro de la carpeta
        os.chdir(save_location)
        t=os.getcwd()
        playlistTitle = re.sub(r"\W+|_", " ", playlist['title'])  # remueve los caracteres especiales del titulo

        if os.path.exists(playlistTitle):
            os.chdir(playlistTitle)
        #si no existe el folder crearlo
        else:
            os.mkdir(playlistTitle)
            os.chdir(playlistTitle)

        #comienza la cuenta de video de la playlist y la imprime
        current_video_in_download = 1
        quality = self.cb_PlaylistQuality.currentIndex()

        #loop para descargar cad video en la playlist
        for video in playlist_videos:
            current_video = video['pafy']
            current_video_stream = current_video.videostreams
           # print(current_video_stream)
            download = current_video_stream[quality].download(callback = self.Playlist_Progress)
            QApplication.processEvents()
            #print(current_video_in_download)
            current_video_in_download +=1
            self.lcdNumber.display(current_video_in_download)

    def Playlist_Progress(self, total, receive, ratio, rate, time):  # del callback recive los parametros
        readed_date = receive
        if total > 0:
            # cambia el progreso a barra
            download_percentage = readed_date * 100 / total
            self.pb_Playlist.setValue(round(download_percentage))
            # calcula el tiempo restante y lo imprime
            remaining_time = round(time / 60, 2)
            #print(self.format_bytes(rate * 1000) + '/s')
            self.lb_PlaylistRestante.setText(
                str(remaining_time) + ' minutos restantes' + ' ' + self.format_bytes(rate * 1000) + '/s')
            QApplication.processEvents()  # sera la ui responsiva sino se atora al acutaliza


    def DuumyBn(self):
        self.ln_PlaylistUrl.setText('https://www.youtube.com/playlist?list=PL0SUPYdGkDOuwhmI6X3vFceUWeemSwbjo')
        self.ln_PlaylistSave.setText(os.getcwd())

    def Playlist_Save_Browse(self):
        playlist_save_location = QFileDialog.getExistingDirectory(self,"select download directory")
        self.ln_PlaylistSave.setText(playlist_save_location)

    #convierte de bytes a kilo, mega , giga dependiendo
    def format_bytes(self, size):
        power = 1000
        n = 0
        power_labels = {0: '', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}
        while size > power:
            size /= power
            n += 1
        return str(round(size,1)) + ' ' + power_labels[n] + 'B'


###################botones"""""""""""""""""""""""""""

    def Open_Home(self):
        self.tabWidget.setCurrentIndex(0)

    def Open_Download(self):
        self.tabWidget.setCurrentIndex(1)

    def Open_Youtube(self):
        self.tabWidget.setCurrentIndex(2)
        pass

    def Open_Settings(self):
        self.tabWidget.setCurrentIndex(3)
        pass



##########THEMES###################################

    def Apply_Dark_Style(self):
        style = open('ui/Themes/qdark.css' , 'r')
        style = style.read()
        self.setStyleSheet(style)






def main():#crea una aplicacion usando la clase externa
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()