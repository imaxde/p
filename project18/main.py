import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QInputDialog, QTableWidgetItem, QSystemTrayIcon
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtCore import QStringListModel, QTimer, Qt
from ui_files.main_window_ui import Ui_MainWindow
import database_tools
from ui_files.stats_window_ui import Ui_StatsForm
from ui_files.notifications_window_ui import Ui_NotificationsForm
from ui_files.script_window_ui import Ui_ScriptForm
from ui_files.settings_window_ui import Ui_SettingsForm
import random
from datetime import datetime, timedelta
import matplotlib.pyplot as pplt
import sqlite3
import os
import csv
import emoji
import subprocess
import platform


class StatsWindow(QWidget, Ui_StatsForm):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.n = int(database_tools.update_config()[2])
        self.fill_table()
        self.fill_chart()
        self.chart_type_box.addItems([
            "По категориям", "По дням", "По месяцам", "Доходы/Расходы"
        ])
        self.chart_type_box.currentTextChanged.connect(self.fill_chart)
        self.chart_type_box.setCurrentIndex(3)

    def fill_table(self):
        history_data = database_tools.history(self.n)
        self.info.setColumnCount(5)
        self.info.setRowCount(self.n)
        for i, row in enumerate(history_data):
            self.info.setItem(i, 0, QTableWidgetItem(row[0]))
            self.info.setItem(i, 1, QTableWidgetItem(row[1]))
            self.info.setItem(i, 2, QTableWidgetItem(str(row[2])))
            self.info.setItem(i, 3, QTableWidgetItem(str(datetime.fromtimestamp(row[3]))))
            self.info.setItem(i, 4, QTableWidgetItem(row[4]))
        self.info.resizeColumnsToContents()

    def fill_chart(self):
        stat_type = self.chart_type_box.currentText()
        if stat_type == "По категориям":
            self.fill_chart_category_pie()
        elif stat_type == "По дням":
            self.fill_chart_day_bar()
        elif stat_type == "По месяцам":
            self.fill_chart_month_bar()
        else:
            self.fill_chart_expenses_income()
        self.pie_chart_label.setPixmap(QPixmap("diagram.png"))

    def fill_chart_expenses_income(self):
        expenses = 0
        income = 0
        history_data = database_tools.history(self.n)
        for i in history_data:
            if int(i[2]) > 0:
                income += abs(int(i[2]))
            elif int(i[2]) < 0:
                expenses += abs(int(i[2]))
        pplt.figure(figsize=(3, 3))
        pplt.stackplot([0, 1], [expenses / (expenses + income)] * 2, [income / (expenses + income)] * 2,
                       labels=["Расходы", "Доходы"],
                       colors=["#eb4034", "#34eb58"], alpha=1.0)
        pplt.xticks([])
        pplt.yticks([])
        pplt.axis('off')
        pplt.savefig("diagram.png", dpi=100, bbox_inches="tight")

    def fill_chart_day_bar(self):
        history_data = database_tools.history(self.n)
        day_stats = [0] * 31
        for i in history_data:
            if datetime.fromtimestamp(i[3]).month == datetime.today().month and int(i[2]) < 0:
                day_stats[datetime.fromtimestamp(i[3]).day - 1] += abs(int(i[2]))
        pplt.figure(figsize=(7, 3))
        pplt.bar([str(i + 1) for i in range(31)], day_stats)
        pplt.title("Расходы")
        pplt.savefig("diagram.png", format="png", dpi=53)

    def fill_chart_month_bar(self):
        history_data = database_tools.history(self.n)
        months = [0] * 12
        for i in history_data:
            if int(i[2]) < 0:
                months[datetime.fromtimestamp(i[3]).month - 1] += abs(int(i[2]))
        pplt.figure(figsize=(5, 3))
        pplt.bar(["янв", "фев", "мар", "апр", "май", "июн", "июл", "авг", "сен", "окт", "ноя", "дек"], months)
        pplt.title("Расходы")
        pplt.savefig("diagram.png", format="png", dpi=74)

    def fill_chart_category_pie(self):
        history_data = database_tools.history(self.n)
        d = dict()
        for i in history_data:
            if int(i[2]) < 0:
                if i[4] in d:
                    d[i[4]] += abs(i[2])
                else:
                    d[i[4]] = abs(i[2])
        costs = [(i, d[i]) for i in d] + [("", 1), ("", 1), ("", 1), ("", 1)]
        costs.sort(key=lambda x: x[1], reverse=True)
        s1, s2, s3, s4 = costs[0][1], costs[1][1], costs[2][1], sum([i[1] for i in costs[3:]])
        p1, p2, p3, p4 = costs[0][0], costs[1][0], costs[2][0], "Другое"
        data = [s1, s2, s3, s4]
        labels = [p1, p2, p3, p4]
        pplt.figure(figsize=(3, 3))
        pplt.pie(data, labels=labels, autopct="%1.1f%%", startangle=90)
        pplt.title("Расходы")
        pplt.savefig("diagram.png", format="png", dpi=94)
        self.pie_chart_label.setPixmap(QPixmap("diagram.png"))


class NotificationsWindow(QWidget, Ui_NotificationsForm):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.notification_on = int(database_tools.update_config()[1])
        self.minute_count = 0
        self.check_script()
        self.timer = QTimer()
        self.timer.setInterval(60000)
        self.timer.setTimerType(Qt.TimerType.VeryCoarseTimer)
        self.timer.timeout.connect(self.check_script)
        self.timer.start()
        self.print_all_alerts()

    def show_notification(self, t, d):
        if self.notification_on:
            self.tray_icon = QSystemTrayIcon()
            self.tray_icon.setIcon(QIcon("icon2_menu.png"))
            self.tray_icon.setVisible(True)
            self.tray_icon.show()
            self.tray_icon.showMessage(t, d, QSystemTrayIcon.MessageIcon.Information, 5000)
            database_tools.get_alerts(t, d)
        self.print_all_alerts()

    def print_all_alerts(self):
        model = QStringListModel()
        model.setStringList([f"{i[0]} | {i[1]}" for i in database_tools.get_alerts()])
        self.listView.setModel(model)

    def check_script(self):
        bal, mbal = database_tools.update_config()[3:]
        cards = database_tools.script_cards()
        for i in cards:
            if self.minute_count % i[2] == 0 and self.minute_count != 0:
                bal += int(i[1])
                self.show_notification("Сценарий сработал", i[0])
                database_tools.new_note(i[0], int(i[1]), int(i[4]))
        cards = database_tools.script_cards(False)
        for i in cards:
            if datetime.fromtimestamp(int(i[2])).date() < datetime.today().date():
                bal += int(i[1])
                database_tools.new_note(i[0], int(i[1]), int(i[4]))
                self.show_notification("План сработал", i[0])
                database_tools.del_plan(i[3])
        database_tools.update_config(money0=bal)
        if bool(self.notification_on):
            self.checkBox.setChecked(bool(self.notification_on))
        if int(bal) < int(mbal) and self.minute_count % 5 == 0:
            self.show_notification("Маленький баланс", f"Осталось всего {bal} денег")
        self.minute_count += 1


class ScriptWindow(QWidget, Ui_ScriptForm):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.change_script4.clicked.connect(self.manage_script)
        self.change_script3.clicked.connect(self.manage_script)
        self.change_script2.clicked.connect(self.manage_script)
        self.change_script1.clicked.connect(self.manage_script)
        cards = database_tools.script_cards()
        for i, frame in enumerate([self.script_frame1, self.script_frame2, self.script_frame3, self.script_frame4]):
            kids = frame.children()[:3]
            kids[0].setText("🔌 " + str(cards[i][0]))
            kids[1].setText("💰 " + str(cards[i][1]))
            kids[2].setText("🕰️ Каждые " + str(cards[i][2]) + "д")
        self.show_plans()
        self.create_plan_button.clicked.connect(self.create_plan_action)
        self.delete_plan_button.clicked.connect(self.delete_plan_action)
        self.calendar_widget.selectionChanged.connect(self.show_plans)
        self.plan_plain.setReadOnly(True)

    def manage_script(self):
        interval, ok_press1 = QInputDialog.getInt(self, "Измение сценария", "Интервал повторения (в днях)",
                                                  1, 1, 30, 1)
        if ok_press1:
            sc_name, ok_press2 = QInputDialog.getText(self, "Измение сценария", "Название")
            if ok_press2:
                edit_money_category, ok_press3 = QInputDialog.getItem(
                    self, "Изменение сценария", "В какой категории?", database_tools.get_categories(), 1, False)
                if ok_press3:
                    money_change, ok_press4 = QInputDialog.getText(self, "Измение сценария", "Измение денег")
                    if ok_press4:
                        a_id = int(self.sender().objectName()[-1])
                        try:
                            database_tools.edit_automation(a_id, sc_name, int(money_change), int(interval), 1,
                                                           edit_money_category)
                        except ValueError:
                            msg_box = QMessageBox()
                            msg_box.warning(self, "🤢", "Введено некорректное значение", QMessageBox.StandardButton.Ok)
                        if a_id == 1:
                            frame_elements = self.script_frame1.children()
                        elif a_id == 2:
                            frame_elements = self.script_frame2.children()
                        elif a_id == 3:
                            frame_elements = self.script_frame3.children()
                        else:
                            frame_elements = self.script_frame4.children()
                        frame_elements[0].setText("🔌 " + sc_name)
                        frame_elements[1].setText("💰 " + money_change)
                        frame_elements[2].setText("🕰️ Каждые " + str(interval) + "д")

    def show_plans(self):
        date_on_calendar = self.calendar_widget.selectedDate()
        self.selected_date = datetime(date_on_calendar.year(), date_on_calendar.month(), date_on_calendar.day())
        crd = database_tools.script_cards(False)
        text_to_display = ""
        for i in crd:
            if i[2] == self.selected_date.timestamp():
                text_to_display += f"{i[3]}. {i[0]} ({i[1]})\n"
        self.plan_plain.setPlainText(text_to_display)

    def create_plan_action(self):
        stamp = self.selected_date.timestamp()
        edit_money_category, ok_press1 = QInputDialog.getItem(
            self, "Добавление авто-планов", "В какой категории?", database_tools.get_categories(), 1, False)
        if ok_press1:
            sc_name, ok_press2 = QInputDialog.getText(self, "Добавление авто-планов", "Название")
            if ok_press2:
                money_change, ok_press3 = QInputDialog.getText(self, "Добавление авто-планов", "Измение денег")
                if ok_press3:
                    con = sqlite3.connect("finance.sqlite3")
                    cur = con.cursor()
                    category_id = cur.execute("""SELECT id FROM categories
                                    WHERE name = ?""", (edit_money_category,)).fetchone()
                    cur.execute(
                        """INSERT INTO automatic(caption,money,cooldown,repeat,category_id) VALUES(?,?,?,0,?)""",
                        (sc_name, money_change, stamp, category_id[0]))
                    con.commit()
                    con.close()
            self.show_plans()

    def delete_plan_action(self):
        textik = self.plan_plain.textCursor().selectedText()
        if len(textik) > 4:
            for i in self.plan_plain.toPlainText().split("\n"):
                if textik in i:
                    a_id = int(i.split(".")[0])
                    database_tools.del_plan(a_id)
                    break
        self.show_plans()


class SettingsWindow(QWidget, Ui_SettingsForm):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        cfg = database_tools.update_config()
        self.settings_spinbox1.setValue(int(cfg[0]))
        self.settings_spinbox2.setValue(int(cfg[1]))
        self.important_controller.setValue(int(cfg[2]))
        self.lineEdit.setText(str(cfg[4]))
        self.settings_spinbox1.valueChanged.connect(self.configuration)
        self.settings_spinbox2.valueChanged.connect(self.configuration)
        self.important_controller.valueChanged.connect(self.configuration)
        self.lineEdit.textChanged.connect(self.configuration)
        self.delete_button.setToolTip("При долгом нажатии удаляяет приложение")
        self.delete_button.clicked.connect(self.click_ev)
        self.delete_button.pressed.connect(self.press_ev)
        self.long_press_start = 0
        self.export_button.clicked.connect(self.export)

    def configuration(self):
        database_tools.update_config(binds0=self.settings_spinbox1.value(),
                                     notifications0=self.settings_spinbox2.value(),
                                     important0=self.important_controller.value(),
                                     minmoney0=int(self.lineEdit.text()))

    def click_ev(self):
        self.delete_button.setText("Добавить категорию")
        if datetime.now() - self.long_press_start > timedelta(0, 4):
            # os.remove("main.py")
            # os.remove("database_tools.py")
            pass
        else:
            nwn, ok1 = QInputDialog.getText(self, "Создание категории", "Введите название:")
            if ok1:
                icon_e, ok2 = QInputDialog.getText(self, "Создание категории", "Введите эмодзи:")
                if ok2:
                    if emoji.emoji_count(icon_e) == 1 and len(icon_e) == 1:
                        database_tools.add_category(nwn, icon_e)

    def press_ev(self):
        self.delete_button.setText("Удалить приложение")
        self.long_press_start = datetime.now()

    def export(self):
        with open("export_transactions.csv", "w", encoding="utf8") as csvfile:
            writer = csv.writer(csvfile, delimiter=";", quotechar='"', quoting=csv.QUOTE_MINIMAL)
            history_data = database_tools.history(99)
            writer.writerow(["Транзакция", "Сумма", "Дата и время", "Категория"])
            for i in history_data:
                writer.writerow([i[1], i[2], str(datetime.fromtimestamp(i[3])), i[4]])
        system_name = platform.system()
        if system_name == 'Windows':
            os.startfile("export_transactions.csv")
        elif system_name == 'Darwin':  # macOS
            subprocess.run(["open", "export_transactions.csv"])
        elif system_name == 'Linux':
            subprocess.run(['xdg-open', "export_transactions.csv"])


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.plus_btn.clicked.connect(self.edit_money)
        self.minus_btn.clicked.connect(self.edit_money)
        self.menu_button1.clicked.connect(self.open_stats)
        self.menu_button1.setIcon(QIcon(QPixmap("icon1_menu.png")))
        self.menu_button2.clicked.connect(self.open_notifications)
        self.menu_button2.setIcon(QIcon(QPixmap("icon2_menu.png")))
        self.menu_button3.clicked.connect(self.open_script)
        self.menu_button3.setIcon(QIcon(QPixmap("icon3_menu.png")))
        self.menu_button4.clicked.connect(self.open_settings)
        self.menu_button4.setIcon(QIcon(QPixmap("icon4_menu.png")))
        self.balance = int(open("config.txt", encoding="utf8").read().split()[3])
        self.money_label.setText(str(self.balance))
        self.date_label.setText(str(datetime.today().date()))
        self.new_tip.clicked.connect(self.advice)
        self.advice()

    def edit_money(self):
        if self.sender().text() == "+":
            a = "добавить"
        else:
            a = "вычесть"
        spending_name, ok_pressed1 = QInputDialog.getText(self, "Изменить бюджет", f"Название операции")
        if ok_pressed1:
            edit_money_category, ok_pressed2 = QInputDialog.getItem(
                self, "Изменить бюджет", "В какой категории?", database_tools.get_categories(), 1, False)
            if ok_pressed2:
                amount, ok_pressed3 = QInputDialog.getText(self, "Изменить бюджет", f"Сколько денег {a}?")
                if ok_pressed3:
                    try:
                        if a == "добавить":
                            self.balance += abs(int(amount))
                            amount = abs(int(amount))
                        elif a == "вычесть":
                            self.balance -= abs(int(amount))
                            amount = -1 * abs(int(amount))
                        self.money_label.setText(str(self.balance))
                        database_tools.update_config(money0=self.balance)
                        database_tools.new_note(spending_name, amount, edit_money_category)
                    except ValueError:
                        warning_box = QMessageBox()
                        warning_box.warning(self, "🤢", "Введено некорректное значение", QMessageBox.StandardButton.Ok)

    def open_stats(self):
        self.stats_form = StatsWindow()
        self.stats_form.show()

    def open_notifications(self):
        self.notifications_form = NotificationsWindow()
        self.notifications_form.show()

    def open_script(self):
        self.script_form = ScriptWindow()
        self.script_form.show()

    def open_settings(self):
        self.settings_form = SettingsWindow()
        self.settings_form.show()

    def advice(self):
        a = open("advice.txt", encoding="utf8")
        advices = a.readlines()
        a.close()
        self.tip_plain.setPlainText(random.choice(advices))
        self.balance = int(open("config.txt", encoding="utf8").read().split()[3])
        self.money_label.setText(str(self.balance))

    def keyPressEvent(self, event):
        if event.modifiers() == (Qt.KeyboardModifier.AltModifier | Qt.KeyboardModifier.ShiftModifier):
            if int(database_tools.update_config()[0]) == 1:
                if event.key() == Qt.Key.Key_Plus:
                    self.plus_btn.click()
                elif event.key() == Qt.Key.Key_Minus:
                    self.minus_btn.click()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())
