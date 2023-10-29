import os
import sys
import threading
import time
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QFileDialog, QProgressBar
from pytube import YouTube

class YoutubeDownloaderApp(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('YouTube Downloader')
        self.setGeometry(100, 100, 400, 250)

        layout = QVBoxLayout()

        self.url_label = QLabel('Insira a URL do vídeo:')
        layout.addWidget(self.url_label)

        self.url_input = QLineEdit()
        layout.addWidget(self.url_input)

        self.save_label = QLabel('Pasta de Salvamento:')
        layout.addWidget(self.save_label)

        self.save_button = QPushButton('Escolher Pasta')
        self.save_button.clicked.connect(self.open_save_folder)
        layout.addWidget(self.save_button)

        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar)

        self.status_label = QLabel('')
        layout.addWidget(self.status_label)

        self.download_button = QPushButton('Baixar Vídeo')
        self.download_button.clicked.connect(self.start_download)
        layout.addWidget(self.download_button)

        self.setLayout(layout)

    def open_save_folder(self):
        folder = QFileDialog.getExistingDirectory(self, 'Escolher Pasta')
        self.save_label.setText(f'Pasta de Salvamento: {folder}')
        self.save_folder = folder

    def download_progress_callback(self, stream, chunk, bytes_remaining):
        file_size = stream.filesize
        bytes_downloaded = file_size - bytes_remaining
        percentage = (bytes_downloaded / file_size) * 100
        self.progress_bar.setValue(int(percentage))

    def start_download(self):
        if not hasattr(self, 'save_folder'):
            self.save_folder = os.path.expanduser('~')

        url = self.url_input.text()

        try:
            yt = YouTube(url, on_progress_callback=self.download_progress_callback)
            video_stream = yt.streams.get_highest_resolution()
            file_name = yt.title + '.mp4'

            self.progress_bar.setValue(0)
            self.status_label.setText('Baixando...')
            self.status_label.adjustSize()

            t = threading.Thread(target=self.download_video, args=(video_stream, file_name))
            t.start()
        except Exception as e:
            self.status_label.setText(f"Erro: {e}")
            self.status_label.adjustSize()

    def download_video(self, video_stream, file_name):
        video_stream.download(self.save_folder)
        self.progress_bar.setValue(100)
        self.status_label.setText(f"Download concluído: {file_name}")
        self.status_label.adjustSize()
        time.sleep(2)
        self.status_label.setText('')
        self.status_label.adjustSize()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = YoutubeDownloaderApp()
    window.show()
    sys.exit(app.exec())
