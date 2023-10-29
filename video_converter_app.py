import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QLabel, QFileDialog
from moviepy.video.io.VideoFileClip import VideoFileClip


class VideoConverterApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.video_path = ""
        self.save_path = ""

    def init_ui(self):
        self.setWindowTitle("Video Converter App (mp4)")
        self.setGeometry(100, 100, 400, 200)

        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)

        self.label = QLabel("Selecione o vídeo que deseja converter:", self)
        self.btn_select_video = QPushButton("Localizar vídeo", self)
        self.btn_select_video.clicked.connect(self.get_video_path)

        self.label_save = QLabel("Selecione a pasta de salvamento:", self)
        self.btn_select_save = QPushButton("Pasta de salvamento", self)
        self.btn_select_save.clicked.connect(self.get_save_path)

        self.btn_convert = QPushButton("Converter", self)
        self.btn_convert.clicked.connect(self.convert_video)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.btn_select_video)
        layout.addWidget(self.label_save)
        layout.addWidget(self.btn_select_save)
        layout.addWidget(self.btn_convert)
        self.main_widget.setLayout(layout)

    def get_video_path(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Selecione o vídeo", "", "Video Files (*.mp4 *.avi *.mov);;All Files (*)", options=options)
        if file_path:
            self.video_path = file_path
            self.label.setText(f"Vídeo selecionado: {os.path.basename(self.video_path)}")

    def get_save_path(self):
        options = QFileDialog.Options()
        dir_path = QFileDialog.getExistingDirectory(self, "Selecione a pasta de salvamento", options=options)
        if dir_path:
            self.save_path = dir_path
            self.label_save.setText(f"Pasta de salvamento selecionada: {self.save_path}")

    def convert_video(self):
        if not self.video_path or not self.save_path:
            self.label.setText("Selecione o vídeo e a pasta de salvamento primeiro.")
            return

        video_filename = os.path.basename(self.video_path)
        output_path = os.path.join(self.save_path, video_filename)

        try:
            video_clip = VideoFileClip(self.video_path)
            video_clip.write_videofile(output_path, codec="libx264")
            video_clip.close()
            self.label.setText("Conversão concluída com sucesso!")
        except Exception as e:
            self.label.setText(f"Erro ao converter o vídeo: {str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VideoConverterApp()
    window.show()
    sys.exit(app.exec_())
