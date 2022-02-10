from ctypes import windll
from bot_UI_base import Ui_MainWindow
from PyQt6 import QtWidgets as qtw
from PyQt6 import QtCore as qtc
from PyQt6.QtGui import QPixmap, QIcon, QImage, QFont, QColor, QPainter, QPainterPath
from zmq import Context, REQ
from downloader import main as downloader
import json
import requests


myappid = 'mycompany.myproduct.subproduct.version'  # arbitrary string
windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)  # updates hotbar icon (idk why but it works)

context = Context()
socket = context.socket(REQ)
socket.connect('tcp://localhost:5555')


def circleImage(imagePath):
    source = QPixmap(imagePath)
    size = min(source.width(), source.height())

    target = QPixmap(size, size)
    target.fill(QColor(0, 0, 0, 0))

    qp = QPainter(target)
    # qp.setRenderHints(qp.Antialiasing)
    path = QPainterPath()
    path.addEllipse(0, 0, size, size)
    qp.setClipPath(path)

    sourceRect = qtc.QRect(0, 0, size, size)
    sourceRect.moveCenter(source.rect().center())
    qp.drawPixmap(target.rect(), source, sourceRect)
    qp.end()

    return target


def clearLayout(layout):
    while layout.count():
        child = layout.takeAt(0)
        if child.widget() is not None:
            child.widget().deleteLater()
        elif child.layout() is not None:
            clearLayout(child.layout())


class TestWindow(qtw.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)

        self.setWindowIcon(QIcon('icons/discord2.0.png'))

        self.get_servers_button.clicked.connect(self.get_servers)

        self.scrollArea.setVerticalScrollBar(self.verticalScrollBar)
        self.scrollArea_2.setVerticalScrollBar(self.verticalScrollBar_2)

        self.lineEdit.returnPressed.connect(self.test)

    def get_servers(self):  # sends server info request to bot
        print('trying to get server info')
        socket.send(b'servers')
        message = json.loads(socket.recv())

        for server_data in message:
            self.add_server(message[server_data])

    def add_server(self, server_data):  # adds a server dinamically
        new_button = server(*server_data)
        layout = new_button.get_layout()

        self.verticalLayout_2.addLayout(layout)

    def test(self):
        selected = channel.selected
        if selected is not None:
            text = self.lineEdit.text()
            print(f'send_{selected}_{text}')
            socket.send_string(f'send_{selected}_{text}')

            message = socket.recv()

        print(self.lineEdit.text())
        print(selected)
        self.lineEdit.setText('')


class server:
    def __init__(self, server_name, server_id, icon_url):
        self.name = server_name
        self.id = server_id
        self.icon_url = icon_url

        self.horizontalLayout = qtw.QHBoxLayout()  # creates a horizontal layout
        self.horizontalLayout.setObjectName(f'horizontalLayout')

        spacerItem = qtw.QSpacerItem(40, 20, qtw.QSizePolicy.Policy.Expanding, qtw.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem)  # adds a horizontal spacer

        self.verticalLayout = qtw.QVBoxLayout()  # creates a vertical layout
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setSpacing(0)
        # self.verticalLayout.set

        self.server = qtw.QPushButton()  # creates the server button
        self.server.setIconSize(qtc.QSize(64, 64))
        self.server.setObjectName(f'server')
        self.server.clicked.connect(lambda: self.get_channels(self.id))  # connects to function

        image = QImage()  # sets button to server's icon
        image.loadFromData(requests.get(self.icon_url).content)
        circle = circleImage(image)

        self.server.setIcon(QIcon(circle))
        self.server.setStyleSheet('QPushButton{background:transparent;}'
                                  'QPushButton:hover{background: rgb(237, 131, 43);'
                                  'border: 1px solid rgb(237, 131, 43);'
                                  'border-top-left-radius: 8px;'
                                  'border-top-right-radius: 8px;}')

        self.verticalLayout.addWidget(self.server)
        self.server_name = qtw.QLabel()
        self.server_name.setAlignment(qtc.Qt.Alignment.AlignCenter)
        self.server_name.setObjectName(f'server_name')
        self.server_name.setText(self.name)
        self.server_name.setStyleSheet('background-color: rgb(237, 131, 43);'
                                       'border: 2px solid rgb(237, 131, 43);'
                                       'border-bottom-left-radius: 8px;'
                                       'border-bottom-right-radius: 8px;')
        self.server_name.setMaximumWidth(80)
        self.server_name.setWordWrap(True)
        self.server_name.setFont(QFont('open sans light', 8))
        self.verticalLayout.addWidget(self.server_name)

        self.horizontalLayout.addLayout(self.verticalLayout)

        self.horizontalLayout.addItem(spacerItem)  # adds another spacer

    def get_layout(self):
        return self.horizontalLayout

    def get_channels(self, server_id):
        print('trying to get channels info')
        socket.send_string(f'guild_{server_id}')
        message = json.loads(socket.recv())

        clearLayout(MainWindow.verticalLayout_text)
        for text_channel in message['text']:
            self.add_text_channel(text_channel)

        clearLayout(MainWindow.verticalLayout_voice)
        for voice_channel in message['voice']:
            self.add_voice_channel(voice_channel)

        print('trying to get users info')
        socket.send_string(f'users_{server_id}')
        message = json.loads(socket.recv())

        clearLayout(MainWindow.verticalLayout_users)
        downloader(message['members'], processes_count=30, img_size=1024)
        for data in message['members']:
            self.add_users(data)

    def add_text_channel(self, new_channel):
        button = channel(*new_channel).get_button()

        MainWindow.verticalLayout_text.addWidget(button)

    def add_voice_channel(self, new_channel):
        button = channel(*new_channel).get_button()

        MainWindow.verticalLayout_voice.addWidget(button)

    def add_users(self, user_data):
        new_user = user(*user_data)

        MainWindow.verticalLayout_users.addWidget(new_user.label)


class user:
    def __init__(self, name, icon_url):
        self.name = name
        # self.icon_url = icon_url.replace('size=1024', 'size=64')

        # image = QImage()  # sets button to server's icon
        # image.loadFromData(requests.get(self.icon_url).content)
        image = QPixmap(f'images/{self.name}.png')
        circle = circleImage(image)

        self.label = qtw.QPushButton()
        self.label.setIconSize(qtc.QSize(38, 38))
        self.label.setIcon(QIcon(circle))
        if len(self.name) < 16:
            self.label.setText(self.name)
        else:
            self.label.setText(self.name[:16] + '...')
        self.label.setStyleSheet('QPushButton{background:transparent;'
                                 'text-align: left;'
                                 'color: rgb(255, 255, 255)}'
                                 'QPushButton:hover{background: rgb(237, 131, 43);'
                                 'border: 1px solid rgb(237, 131, 43);'
                                 'border-radius: 10px;}')
        self.label.setFont(QFont('open sans light', 11))
        self.label.setMaximumWidth(220)


class channel:
    selected = None

    def __init__(self, channel_name, channel_id, channel_type):
        self.name = channel_name
        self.id = channel_id
        self.type = channel_type
        self.messages = []

        self.channel_name = qtw.QPushButton()
        self.channel_name.setText(self.name)
        self.channel_name.setStyleSheet('QPushButton{background: rgb(204, 120, 50);'
                                        'text-align: left;'
                                        'border: 2px solid rgb(204, 120, 50);'
                                        'border-radius: 10px;'
                                        'padding-left: 5px}'
                                        'QPushButton:hover{background: rgb(237, 131, 43);'
                                        'border: 2px solid rgb(237, 131, 43);}')
        self.channel_name.setFont(QFont('open sans light', 8))
        self.channel_name.setIcon(QIcon(f'icons/{self.type}.png'))
        self.channel_name.clicked.connect(lambda: self.get_messages(self.id))  # connects to function

    def get_button(self):
        return self.channel_name

    def get_messages(self, channel_id):
        channel.selected = channel_id
        print('trying to get messages info')
        send = f'channel_{channel_id}'
        socket.send_string(send)

        messages = json.loads(socket.recv())

        messages['message'].reverse()

        clearLayout(MainWindow.verticalLayout_messages)

        spacerItem2 = qtw.QSpacerItem(20, 40, qtw.QSizePolicy.Policy.Minimum,
                                      qtw.QSizePolicy.Policy.Expanding)
        MainWindow.verticalLayout_messages.addItem(spacerItem2)

        for channel_message in messages['message']:
            self.add_message(channel_message)

    def add_message(self, channel_message):
        new_message = message(*channel_message)

        MainWindow.verticalLayout_messages.addLayout(new_message.get_layout())


class message:
    def __init__(self, content, author):
        self.content = content
        self.author = author

        self.verticalLayout = qtw.QVBoxLayout(MainWindow.scrollAreaWidgetContents)  # creates a vertical layout
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setContentsMargins(0, 5, 0, 0)

        self.author_label = qtw.QLabel(MainWindow.scrollAreaWidgetContents)
        self.author_label.setStyleSheet('color: rgb(18, 134, 12)')
        font = QFont('open sans light', 10)
        font.setBold(True)
        self.author_label.setFont(font)
        self.author_label.setObjectName(f'author_name')
        self.author_label.setText(self.author)

        self.content_label = qtw.QLabel(MainWindow.scrollAreaWidgetContents)
        self.content_label.setStyleSheet('color: rgb(255, 255, 255);'
                                         'padding-left: 10px')
        self.content_label.setFont(font)
        self.content_label.setText(self.content)
        self.content_label.setObjectName(f'content')
        self.content_label.setWordWrap(True)

        self.verticalLayout.addWidget(self.author_label)
        self.verticalLayout.addWidget(self.content_label)

    def get_layout(self):
        return self.verticalLayout


if __name__ == '__main__':
    import sys

    app = qtw.QApplication([])

    MainWindow = TestWindow()
    MainWindow.show()

    sys.exit(app.exec())
