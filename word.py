import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QTextEdit, QToolBar, 
                            QFontComboBox, QSpinBox, QColorDialog, QFileDialog,
                            QMessageBox, QPushButton, QVBoxLayout, QLabel, QWidget, QGridLayout)
from PyQt6.QtGui import QFont, QTextCharFormat, QColor, QTextCursor, QPixmap
from PyQt6.QtCore import Qt
from PyQt6.QtPrintSupport import QPrinter, QPrintDialog

def generate_templates():
    # Создаем папки, если их нет
    templates_dir = 'templates'
    icons_dir = 'icons'
    
    os.makedirs(templates_dir, exist_ok=True)
    os.makedirs(icons_dir, exist_ok=True)
    
    print(f"Создана папка шаблонов: {os.path.abspath(templates_dir)}")
    
    templates = {
        'letter.txt': """
ПИСЬМО

Кому: _____________
Дата: _____________

Уважаемый(ая) _____________,

[Текст письма]

С уважением,
[Ваше имя]
[Должность]
[Контактная информация]
        """,
        
        'resume.txt': """
РЕЗЮМЕ

Личные данные:
ФИО: 
Дата рождения:
Адрес:
Телефон:
Email:

Образование:
• [Учебное заведение] - [Годы обучения]
  [Специальность/Степень]
• 

Опыт работы:
• [Компания] - [Годы работы]
  [Должность]
  [Основные обязанности и достижения]
•

Навыки:
• [Профессиональные навыки]
• [Технические навыки]
• [Языки]
• [Сертификаты]

Дополнительная информация:
• Хобби и интересы
• Рекомендации
        """,
        
        'report.txt': """
ОТЧЕТ

Тема: _____________
Дата: _____________
Подготовил: _____________

1. Введение
• Цель отчета
• Методология
• Краткое содержание

2. Основная часть
• Анализ данных
• Результаты исследования
• Ключевые находки

3. Выводы
• Основные заключения
• Интерпретация результатов

4. Рекомендации
• Предложения по улучшению
• План действий
        """,
        
        'calendar.txt': """
КАЛЕНДАРЬ СОБЫТИЙ

Дата: _____________
Время: _____________

СОБЫТИЕ:
Название: _____________
Место проведения: _____________
Участники: _____________

ДЕТАЛИ:
• Повестка дня
• Необходимые материалы
• Дополнительная информация

Примечания:
_____________
        """,
        
        'blank.txt': """
БЛАНК

[Название организации]
[Адрес]
[Контактная информация]

Исх. № _____________
От _____________

ЗАГОЛОВОК ДОКУМЕНТА
_____________________

Содержание:
_____________________________________________
_____________________________________________
_____________________________________________

Подпись: _____________
Дата: _____________
        """,
        
        'list.txt': """
СПИСОК

Название: _____________
Дата создания: _____________

□ Пункт 1
  ◦ Подпункт 1.1
  ◦ Подпункт 1.2

□ Пункт 2
  ◦ Подпункт 2.1
  ◦ Подпункт 2.2

□ Пункт 3
  ◦ Подпункт 3.1
  ◦ Подпункт 3.2

Примечания:
_____________
        """,
        
        'note.txt': """
ЗАМЕТКА

Дата: _____________
Тема: _____________

Важность: □ Высокая □ Средняя □ Низкая

Содержание:
_____________________________________________
_____________________________________________
_____________________________________________

Задачи:
□ _____________
□ _____________
□ _____________

Напоминание: _____________
        """,
        
        'protocol.txt': """
ПРОТОКОЛ

№ _____________
Дата: _____________
Место: _____________

ПРИСУТСТВОВАЛИ:
1. _____________
2. _____________
3. _____________

ПОВЕСТКА ДНЯ:
1. _____________
2. _____________
3. _____________

СЛУШАЛИ:
1. _____________
   Решили: _____________

2. _____________
   Решили: _____________

Председатель: _____________ /_____________/
Секретарь: _____________ /_____________/
        """
    }
    
    # Сохраняем шаблоны
    for filename, content in templates.items():
        with open(os.path.join(templates_dir, filename), 'w', encoding='utf-8') as f:
            f.write(content.strip())

    # Добавляем проверку созданных файлов
    print("\nСозданные шаблоны:")
    for filename in os.listdir(templates_dir):
        print(f"- {filename}")

class TextEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('BredovWord')
        self.setGeometry(100, 100, 1200, 800)

        # Создаем центральный виджет
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # Создаем layout для центрального виджета
        self.main_layout = QVBoxLayout(self.central_widget)
        
        # Создаем текстовое поле
        self.text_edit = QTextEdit()
        
        # Устанавливаем шрифт Times New Roman по умолчанию
        default_font = QFont("Times New Roman", 12)
        self.text_edit.setFont(default_font)
        
        # Создаем панель инструментов
        self.toolbar = QToolBar()
        self.setup_toolbar()
        
        # Создаем виджет для шаблонов
        self.templates_widget = QWidget()
        self.setup_templates()
        
        # Показываем шаблоны по умолчанию
        self.show_templates()

    def setup_toolbar(self):
        # Добавляем кнопку возврата к шаблонам
        self.toolbar.addAction('Шаблоны', self.show_templates)
        
        # Остальные кнопки панели инструментов
        font_box = QFontComboBox(self)
        font_box.currentFontChanged.connect(self.font_changed)
        self.toolbar.addWidget(font_box)

        size_box = QSpinBox(self)
        size_box.setValue(12)
        size_box.setRange(1, 100)
        size_box.valueChanged.connect(self.size_changed)
        self.toolbar.addWidget(size_box)

        self.toolbar.addAction('Жирный', self.toggle_bold)
        self.toolbar.addAction('Курсив', self.toggle_italic)
        self.toolbar.addAction('Подчеркнутый', self.toggle_underline)
        self.toolbar.addAction('Цвет', self.color_dialog)
        self.toolbar.addAction('Открыть', self.open_file)
        self.toolbar.addAction('Сохранить', self.save_file)
        self.toolbar.addAction('Печать', self.print_file)
        
        self.addToolBar(self.toolbar)

    def setup_templates(self):
        templates_layout = QGridLayout(self.templates_widget)
        templates_layout.setSpacing(20)
        
        # Шаблоны
        templates = ["Новый документ", "Письмо", "Резюме", "Отчет", "Календарь", 
                    "Бланк", "Список", "Заметка", "Протокол"]
        row, col = 0, 0
        for template in templates:
            btn = self.create_template_button(template, "")
            btn.clicked.connect(lambda checked, t=template: self.open_template(t))
            templates_layout.addWidget(btn, row, col)
            col += 1
            if col > 3:
                col = 0
                row += 1

    def show_templates(self):
        # Очищаем главный layout
        while self.main_layout.count():
            child = self.main_layout.takeAt(0)
            if child.widget():
                child.widget().hide()
        
        # Показываем шаблоны
        self.templates_widget.show()
        self.main_layout.addWidget(self.templates_widget)

    def show_editor(self):
        # Очищаем главный layout
        while self.main_layout.count():
            child = self.main_layout.takeAt(0)
            if child.widget():
                child.widget().hide()
        
        # Показываем редактор
        self.toolbar.show()
        self.text_edit.show()
        self.main_layout.addWidget(self.toolbar)
        self.main_layout.addWidget(self.text_edit)

    def font_changed(self, font):
        self.text_edit.setCurrentFont(font)

    def size_changed(self, size):
        self.text_edit.setFontPointSize(size)

    def toggle_bold(self):
        fmt = self.text_edit.currentCharFormat()
        fmt.setFontWeight(QFont.Weight.Bold if fmt.fontWeight() != QFont.Weight.Bold else QFont.Weight.Normal)
        self.text_edit.setCurrentCharFormat(fmt)

    def toggle_italic(self):
        fmt = self.text_edit.currentCharFormat()
        fmt.setFontItalic(not fmt.fontItalic())
        self.text_edit.setCurrentCharFormat(fmt)

    def toggle_underline(self):
        fmt = self.text_edit.currentCharFormat()
        fmt.setFontUnderline(not fmt.fontUnderline())
        self.text_edit.setCurrentCharFormat(fmt)

    def color_dialog(self):
        color = QColorDialog.getColor()
        if color.isValid():
            fmt = self.text_edit.currentCharFormat()
            fmt.setForeground(color)
            self.text_edit.setCurrentCharFormat(fmt)

    def open_file(self):
        fname, _ = QFileDialog.getOpenFileName(self, 'Открыть файл', '', 
                                             'Text files (*.txt);;All Files (*)')
        if fname:
            try:
                with open(fname, 'r', encoding='utf-8') as f:
                    self.text_edit.setText(f.read())
            except Exception as e:
                QMessageBox.critical(self, 'Ошибка', f'Не удалось открыть файл: {str(e)}')

    def save_file(self):
        fname, _ = QFileDialog.getSaveFileName(self, 'Сохранить файл', '', 
                                             'Text files (*.txt);;All Files (*)')
        if fname:
            try:
                with open(fname, 'w', encoding='utf-8') as f:
                    f.write(self.text_edit.toPlainText())
            except Exception as e:
                QMessageBox.critical(self, 'Ошибка', f'Не удалось сохранить файл: {str(e)}')

    def print_file(self):
        printer = QPrinter(QPrinter.PrinterMode.HighResolution)
        dialog = QPrintDialog(printer, self)

        if dialog.exec() == QPrintDialog.DialogCode.Accepted:
            self.text_edit.print(printer)

    def open_template(self, template_name):
        # Словарь соответствия названий кнопок и имен файлов
        template_files = {
            "Новый документ": None,
            "Письмо": "letter.txt",
            "Резюме": "resume.txt",
            "Отчет": "report.txt",
            "Календарь": "calendar.txt",
            "Бланк": "blank.txt",
            "Список": "list.txt",
            "Заметка": "note.txt",
            "Протокол": "protocol.txt"
        }
        
        if template_name == "Новый документ":
            self.text_edit.clear()
        else:
            template_file = template_files.get(template_name)
            if template_file:
                template_path = os.path.join('templates', template_file)
                if os.path.exists(template_path):
                    try:
                        with open(template_path, 'r', encoding='utf-8') as f:
                            self.text_edit.setText(f.read())
                    except Exception as e:
                        QMessageBox.critical(self, 'Ошибка', f'Не удалось открыть шаблон: {str(e)}')
                else:
                    QMessageBox.warning(self, 'Предупреждение', f'Шаблон {template_name} не найден')
        
        # Показываем редактор после открытия шаблона
        self.show_editor()

    def create_template_button(self, text, icon_path):
        btn = QPushButton()
        btn.setFixedSize(200, 150)
        btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 4px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #f8f8f8;
                border: 1px solid #999;
            }
        """)
        
        layout = QVBoxLayout()
        
        # Добавляем иконку
        icon_label = QLabel()
        
        # Генерируем базовые иконки для шаблонов
        icons = {
            "Новый документ": "📄",
            "Письмо": "✉️",
            "Резюме": "👤",
            "Отчет": "📊",
            "Календарь": "📅",
            "Бланк": "📋",
            "Список": "📝",
            "Заметка": "📌",
            "Протокол": "📑"
        }
        
        # Добавляем иконку (эмодзи или изображение)
        if text in icons:
            icon_label.setText(icons[text])
            icon_label.setStyleSheet("font-size: 32px;")
        elif icon_path and os.path.exists(icon_path):
            pixmap = QPixmap(icon_path)
            icon_label.setPixmap(pixmap.scaled(64, 64, Qt.AspectRatioMode.KeepAspectRatio))
        
        layout.addWidget(icon_label, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Добавляем текст
        text_label = QLabel(text)
        text_label.setStyleSheet("color: #444; font-size: 12px;")
        layout.addWidget(text_label, alignment=Qt.AlignmentFlag.AlignCenter)
        
        btn.setLayout(layout)
        return btn

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # Генерируем шаблоны при первом запуске
    generate_templates()
    
    # Устанавливаем стиль
    app.setStyle('Fusion')
    
    # Устанавливаем светлую тему
    app.setPalette(app.style().standardPalette())
    
    ex = TextEditor()
    ex.show()
    sys.exit(app.exec())
