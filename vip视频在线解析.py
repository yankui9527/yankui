import sys
import webbrowser
import requests
from lxml import etree
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox,
    QLineEdit, QPushButton, QFrame, QMessageBox
)
from PyQt5.QtGui import QFont, QIcon, QPalette, QColor
from PyQt5.QtCore import Qt, QThread, pyqtSignal


class FetchThread(QThread):
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)

    def __init__(self, url):
        super().__init__()
        self.url = url

    def run(self):
        try:
            response = requests.get(self.url, timeout=10)
            response.encoding = 'utf-8'
            e = etree.HTML(response.text)
            jiek = e.xpath('//*[@id="jk"]/option/text()')
            jiek_url = e.xpath('//*[@id="jk"]/option/@value')
            jiekdi = dict(zip(jiek, jiek_url))
            self.finished.emit(jiekdi)
        except Exception as e:
            self.error.emit(str(e))


class VIPParser(QWidget):
    def __init__(self):
        super().__init__()
        self.jiekdi = {}
        self.initUI()
        self.fetchLines()

    def initUI(self):
        self.setWindowTitle('VIP视频在线解析免费观看      作者：言愧')
        self.setWindowIcon(QIcon(r'D:\Python\PycharmProjects\vip视频解析\言愧圆形白底32x32.ico'))  # 替换为你的图标文件或删除此行
        self.setFixedSize(600, 450)  # 增加高度以容纳新组件

        # 设置主布局
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)

        # 标题
        title = QLabel('VIP视频在线解析')
        title_font = QFont('Microsoft YaHei', 18, QFont.Bold)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet('color: #2c3e50;')

        # 分隔线
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet('background-color: #95a5a6;')

        # 线路选择部分
        line_layout = QHBoxLayout()
        line_label = QLabel('解析线路:')
        line_label.setFont(QFont('Microsoft YaHei', 10))
        line_label.setFixedWidth(80)

        self.combo = QComboBox()
        self.combo.setFont(QFont('Microsoft YaHei', 10))
        self.combo.setMinimumHeight(35)
        self.combo.setStyleSheet('''
            QComboBox {
                background-color: white;
                border: 1px solid #bdc3c7;
                border-radius: 4px;
                padding: 5px;
            }
            QComboBox::drop-down {
                border: none;
            }
        ''')

        line_layout.addWidget(line_label)
        line_layout.addWidget(self.combo)

        # 输入框部分
        input_layout = QHBoxLayout()
        url_label = QLabel('视频链接:')
        url_label.setFont(QFont('Microsoft YaHei', 10))
        url_label.setFixedWidth(80)

        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText('粘贴VIP视频链接到这里...')
        self.url_input.setFont(QFont('Microsoft YaHei', 10))
        self.url_input.setMinimumHeight(35)
        self.url_input.setStyleSheet('''
            QLineEdit {
                background-color: white;
                border: 1px solid #bdc3c7;
                border-radius: 4px;
                padding: 0 10px;
            }
        ''')

        input_layout.addWidget(url_label)
        input_layout.addWidget(self.url_input)

        # 按钮部分
        self.parse_btn = QPushButton('解析视频')
        self.parse_btn.setFont(QFont('Microsoft YaHei', 11, QFont.Bold))
        self.parse_btn.setMinimumHeight(45)
        self.parse_btn.setStyleSheet('''
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:disabled {
                background-color: #bdc3c7;
            }
        ''')
        self.parse_btn.setEnabled(False)
        self.parse_btn.clicked.connect(self.parseVideo)

        # 状态栏
        self.status = QLabel('正在加载解析线路...')
        self.status.setFont(QFont('Microsoft YaHei', 9))
        self.status.setStyleSheet('color: #7f8c8d;')
        self.status.setAlignment(Qt.AlignCenter)

        # 新增：视频网站选择部分
        website_layout = QHBoxLayout()
        website_layout.setContentsMargins(0, 20, 0, 0)  # 增加顶部间距

        website_label = QLabel('视频网站:')
        website_label.setFont(QFont('Microsoft YaHei', 10))
        website_label.setFixedWidth(80)

        # 创建视频网站下拉框
        self.website_combo = QComboBox()
        self.website_combo.setFont(QFont('Microsoft YaHei', 10))
        self.website_combo.setMinimumHeight(35)
        self.website_combo.setStyleSheet('''
            QComboBox {
                background-color: white;
                border: 1px solid #bdc3c7;
                border-radius: 4px;
                padding: 5px;
            }
            QComboBox::drop-down {
                border: none;
            }
        ''')

        # 添加视频网站选项
        websites = [
            ("乐视TV视频", "http://www.le.com/"),
            ("腾讯视频", "http://v.qq.com/"),
            ("爱奇艺视频", "http://www.iqiyi.com/"),
            ("优酷视频", "http://www.youku.com/"),
            ("土豆视频", "http://www.tudou.com/"),
            ("芒果TV视频", "http://www.mgtv.com/"),
            ("搜狐视频", "http://tv.sohu.com/"),
            ("Ac弹幕网", "http://www.acfun.tv/"),
            ("哔哩哔哩", "http://www.bilibili.com/"),
            ("风行网", "http://www.fun.tv/"),
            ("WASU华数视频", "http://www.wasu.cn/"),
            ("56视频", "http://www.56.com/"),
            ("音悦台MV", "http://www.yinyuetai.com/")
        ]

        for name, url in websites:
            self.website_combo.addItem(name, url)

        # 创建跳转按钮
        self.redirect_btn = QPushButton('跳转')
        self.redirect_btn.setFont(QFont('Microsoft YaHei', 10))
        self.redirect_btn.setFixedWidth(80)
        self.redirect_btn.setMinimumHeight(35)
        self.redirect_btn.setStyleSheet('''
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #219653;
            }
        ''')
        self.redirect_btn.clicked.connect(self.redirectToWebsite)

        website_layout.addWidget(website_label)
        website_layout.addWidget(self.website_combo)
        website_layout.addWidget(self.redirect_btn)

        # 添加部件到主布局
        main_layout.addWidget(title)
        main_layout.addWidget(line)
        main_layout.addLayout(line_layout)
        main_layout.addLayout(input_layout)
        main_layout.addWidget(self.parse_btn)
        main_layout.addWidget(self.status)
        main_layout.addLayout(website_layout)  # 添加视频网站选择部分
        main_layout.addStretch(1)

        # 设置背景色
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(236, 240, 241))
        self.setPalette(palette)

        self.setLayout(main_layout)

    def fetchLines(self):
        self.status.setText('正在加载解析线路...')
        self.parse_btn.setEnabled(False)

        self.thread = FetchThread('https://jx.vcs6.com/')
        self.thread.finished.connect(self.linesFetched)
        self.thread.error.connect(self.showError)
        self.thread.start()

    def linesFetched(self, lines):
        self.jiekdi = lines
        self.combo.clear()
        self.combo.addItems(self.jiekdi.keys())

        if self.jiekdi:
            self.status.setText(f'成功加载 {len(self.jiekdi)} 条解析线路')
            self.parse_btn.setEnabled(True)
        else:
            self.status.setText('未获取到解析线路')

    def showError(self, error_msg):
        self.status.setText(f'加载失败: {error_msg}')
        QMessageBox.critical(self, '错误', f'无法获取解析线路:\n{error_msg}')

    def parseVideo(self):
        url = self.url_input.text().strip()
        if not url:
            QMessageBox.warning(self, '输入错误', '请输入视频链接')
            return

        selected = self.combo.currentText()
        if selected not in self.jiekdi:
            QMessageBox.warning(self, '选择错误', '请选择有效的解析线路')
            return

        base_url = self.jiekdi[selected]
        full_url = base_url + url

        try:
            webbrowser.open(full_url)
            self.status.setText(f'已打开解析页面: {selected}')
        except Exception as e:
            QMessageBox.critical(self, '打开失败', f'无法打开浏览器:\n{str(e)}')

    def redirectToWebsite(self):
        # 获取当前选中的网站索引
        index = self.website_combo.currentIndex()
        # 获取关联的URL
        url = self.website_combo.itemData(index)

        if url:
            try:
                webbrowser.open(url)
                self.status.setText(f'已跳转到: {self.website_combo.currentText()}')
            except Exception as e:
                QMessageBox.critical(self, '跳转失败', f'无法打开浏览器:\n{str(e)}')
        else:
            QMessageBox.warning(self, '错误', '该网站链接无效')


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # 设置全局字体
    font = QFont('Microsoft YaHei', 9)
    app.setFont(font)

    parser = VIPParser()
    parser.show()
    sys.exit(app.exec_())