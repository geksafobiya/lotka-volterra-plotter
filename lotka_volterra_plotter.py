#!/usr/bin/env python

# Python standard library modules
import sys

# 3rd party modules
import matplotlib
import matplotlib.backends.backend_qt5agg as backend_qt5agg
from matplotlib.figure import Figure
import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui
import PyQt5.QtWidgets as QtWidgets

# Local application modules
from growth_calculator import GrowthCalculator
from options_menu import OptionsMenu_3_species
from options_menu_4_species import OptionsMenu_4_species
from options_menu_2 import OptionsMenu_2_species

import resources

APP_NAME = 'Lotka-Volterra'
AUTHOR = 'Клименко Анастасия'

class AppForm_2_species(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)

        # название окна
        self.setWindowTitle(APP_NAME)

        # Создание в меню параметров в виджете док-станции
        self.options_menu = OptionsMenu_2_species()
        dock = QtWidgets.QDockWidget('Настройки коэффициентов', self)
        dock.setFeatures(
            QtWidgets.QDockWidget.NoDockWidgetFeatures |
            QtWidgets.QDockWidget.DockWidgetMovable |
            QtWidgets.QDockWidget.DockWidgetFloatable
        )
        dock.setAllowedAreas(
            QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea,
        )
        dock.setWidget(self.options_menu)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, dock)

        # Подключение сигналов из меню параметров
        self.options_menu.update_btn.clicked.connect(self.clear_graph)
        self.options_menu.update_btn.clicked.connect(self.calculate_data)

        self.options_menu.clear_graph_btn.clicked.connect(self.clear_graph)
        self.options_menu.legend_cb.stateChanged.connect(self.redraw_graph)
        self.options_menu.grid_cb.stateChanged.connect(self.redraw_graph)
        self.options_menu.legend_loc_cb.currentIndexChanged.connect(self.redraw_graph)

        # создание графика
        fig = Figure((7.0, 3.0), dpi=100)
        self.canvas = backend_qt5agg.FigureCanvasQTAgg(fig)
        self.canvas.setParent(self)
        self.axes = fig.add_subplot(111)
        backend_qt5agg.NavigationToolbar2QT(self.canvas, self.canvas)

        # инициализация графа
        self.clear_graph()

        self.setCentralWidget(self.canvas)

        # создать менюбар действий

        about_action = QtWidgets.QAction('&About', self)
        about_action.setToolTip('About')
        about_action.setIcon(QtGui.QIcon(':/resources/icon_info.png'))
        about_action.triggered.connect(self.show_about)

     # создать менюбар
        file_exit_action = QtWidgets.QAction('&Exit', self)
        file_exit_action.setToolTip('Exit')
        file_exit_action.setIcon(QtGui.QIcon(':/resources/door_open.png'))
        file_exit_action.triggered.connect(self.close)

        file_menu = self.menuBar().addMenu('&Exit')
        file_menu.addAction(file_exit_action)

        help_menu = self.menuBar().addMenu('&Help')
        help_menu.addAction(about_action)

    def calculate_data(self):
        # объект GrowthCalculator
        growth = GrowthCalculator()

        # Update the GrowthCalculator parameters from the GUI options
        growth.a11 = self.options_menu.a11_sb.value()
        growth.b1 = self.options_menu.b1_sb.value()

        growth.b2 = self.options_menu.b2_sb.value()
        growth.a21 = self.options_menu.a21_sb.value()

        growth.predators = self.options_menu.predator_sb.value()
        growth.prey = self.options_menu.prey_sb.value()

        growth.iterations = self.options_menu.iterations_sb.value()
        growth.dt = self.options_menu.timedelta_sb.value()

        # Calculate the population growths
        results = growth.calculate()
        self.predator_history.extend(results['predator'])
        self.prey_history.extend(results['prey'])

        if (len(self.predator_history) == 0 and
                len(self.prey_history) == 0 == 0):
            QtWidgets.QMessageBox.information(self, 'Error', 'Ошибка')
            return

        # последнее в векторе количество популяции на панель инструментов параметров
      #  print('self.predator_history[-1]', self.predator_history[-1])
      #  self.options_menu.predator_sb.setValue(self.predator_history[-1])
      #  self.options_menu.prey_sb.setValue(self.prey_history[-1])
      #  self.options_menu.superpredators_sb.setValue(self.superpredator_history[-1])
        # перерисовать граф
        self.redraw_graph()

    def clear_graph(self):
        # очистить историю популяций
        self.predator_history = []
        self.prey_history = []

        # перерисовать граф
        self.redraw_graph()

    def redraw_graph(self):
        # очистить граф
        self.axes.clear()

        # Create the graph labels
        self.axes.set_title('Цикл роста хищников и жертв')
        self.axes.set_xlabel('Итерации')
        self.axes.set_ylabel('Размер популяции')

        # Plot the current population data
        if self.predator_history:
            self.axes.plot(self.predator_history, 'r-', label='хищники')
        if self.prey_history:
            self.axes.plot(self.prey_history, 'b-', label='жертвы')

        # если нужно, создаём легенду
        if self.options_menu.legend_cb.isChecked():
            if self.predator_history or self.prey_history:
                legend_loc = str(
                    self.options_menu.legend_loc_cb.currentText()
                ).lower()
                legend = matplotlib.font_manager.FontProperties(size=10)
                self.axes.legend(loc=legend_loc, prop=legend)

        # если нужно, сетки на графике
        self.axes.grid(self.options_menu.grid_cb.isChecked())

        # рисуем график
        self.canvas.draw()

    def show_about(self):
        """
        отображение диалогового окошка "about".
        """
        message = '''<font size="+2">%s</font>
            <p>Дипломная работа на тему системы дифференциальных уравнений Лотки-Вольтерра.
            <p>Написана %s, группа КА-73.
            ''' %(APP_NAME, AUTHOR)

        QtWidgets.QMessageBox.about(self, 'About' + APP_NAME, message)

class AppForm_3_species(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)

        # название окна
        self.setWindowTitle(APP_NAME)

        # Создание в меню параметров в виджете док-станции
        self.options_menu = OptionsMenu_3_species()
        dock = QtWidgets.QDockWidget('Настройки коэффициентов', self)
        dock.setFeatures(
            QtWidgets.QDockWidget.NoDockWidgetFeatures |
            QtWidgets.QDockWidget.DockWidgetMovable |
            QtWidgets.QDockWidget.DockWidgetFloatable
        )
        dock.setAllowedAreas(
            QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea,
        )
        dock.setWidget(self.options_menu)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, dock)

        # Подключение сигналов из меню параметров
        self.options_menu.update_btn.clicked.connect(self.clear_graph)
        self.options_menu.update_btn.clicked.connect(self.calculate_data)

        self.options_menu.clear_graph_btn.clicked.connect(self.clear_graph)
        self.options_menu.legend_cb.stateChanged.connect(self.redraw_graph)
        self.options_menu.grid_cb.stateChanged.connect(self.redraw_graph)
        self.options_menu.legend_loc_cb.currentIndexChanged.connect(self.redraw_graph)

        # создание графика
        fig = Figure((7.0, 3.0), dpi=100)
        self.canvas = backend_qt5agg.FigureCanvasQTAgg(fig)
        self.canvas.setParent(self)
        self.axes = fig.add_subplot(111)
        backend_qt5agg.NavigationToolbar2QT(self.canvas, self.canvas)

        # инициализация графа
        self.clear_graph()

        self.setCentralWidget(self.canvas)

        # создать менюбар действий

        about_action = QtWidgets.QAction('&About', self)
        about_action.setToolTip('About')
        about_action.setIcon(QtGui.QIcon(':/resources/icon_info.png'))
        about_action.triggered.connect(self.show_about)

     # создать менюбар
        file_exit_action = QtWidgets.QAction('&Exit', self)
        file_exit_action.setToolTip('Exit')
        file_exit_action.setIcon(QtGui.QIcon(':/resources/door_open.png'))
        file_exit_action.triggered.connect(self.close)

        file_menu = self.menuBar().addMenu('&Exit')
        file_menu.addAction(file_exit_action)

        help_menu = self.menuBar().addMenu('&Help')
        help_menu.addAction(about_action)

    def calculate_data(self):
        # объект GrowthCalculator
        growth = GrowthCalculator()

        # Update the GrowthCalculator parameters from the GUI options
     #   growth.a11 = self.options_menu.a11_sb.value()
        growth.b1 = self.options_menu.b1_sb.value()
        growth.a12 = self.options_menu.a12_sb.value()
        growth.a13 = self.options_menu.a13_sb.value()

        growth.b2 = self.options_menu.b2_sb.value()
        growth.a21 = self.options_menu.a21_sb.value()
      #  growth.a22 = self.options_menu.a22_sb.value()
        growth.a23 = self.options_menu.a23_sb.value()

        growth.b3 = self.options_menu.b3_sb.value()
        growth.a31 = self.options_menu.a31_sb.value()
        growth.a32 = self.options_menu.a32_sb.value()
     #   growth.a33 = self.options_menu.a33_sb.value()

        growth.predators = self.options_menu.predator_sb.value()
        growth.prey = self.options_menu.prey_sb.value()
        growth.superpredator = self.options_menu.superpredator_sb.value()

        growth.iterations = self.options_menu.iterations_sb.value()
        growth.dt = self.options_menu.timedelta_sb.value()

        # Calculate the population growths
        results = growth.calculate()
        self.predator_history.extend(results['predator'])
        self.prey_history.extend(results['prey'])
        self.superpredator_history.extend(results['superpredator'])

        if (len(self.predator_history) == 0 and
                len(self.prey_history) == 0 and
                len(self.superpredator_history) == 0):
            QtWidgets.QMessageBox.information(self, 'Error', 'Ошибка')
            return

        # последнее в векторе количество популяции на панель инструментов параметров
      #  print('self.predator_history[-1]', self.predator_history[-1])
      #  self.options_menu.predator_sb.setValue(self.predator_history[-1])
      #  self.options_menu.prey_sb.setValue(self.prey_history[-1])
      #  self.options_menu.superpredators_sb.setValue(self.superpredator_history[-1])
        # перерисовать граф
        self.redraw_graph()

    def clear_graph(self):
        # очистить историю популяций
        self.predator_history = []
        self.prey_history = []
        self.superpredator_history = []

        # перерисовать граф
        self.redraw_graph()

    def redraw_graph(self):
        # очистить граф
        self.axes.clear()

        # Create the graph labels
        self.axes.set_title('Цикл роста хищников, жертв и суперхищников')
        self.axes.set_xlabel('Итерации')
        self.axes.set_ylabel('Размер популяции')

        # Plot the current population data
        if self.predator_history:
            self.axes.plot(self.predator_history, 'r-', label='хищники')
        if self.prey_history:
            self.axes.plot(self.prey_history, 'b-', label='жертвы')
        if self.superpredator_history:
            self.axes.plot(self.superpredator_history, 'g-', label='суперхищники')

        # если нужно, создаём легенду
        if self.options_menu.legend_cb.isChecked():
            if self.predator_history or self.prey_history or self.superpredator_history:
                legend_loc = str(
                    self.options_menu.legend_loc_cb.currentText()
                ).lower()
                legend = matplotlib.font_manager.FontProperties(size=10)
                self.axes.legend(loc=legend_loc, prop=legend)

        # если нужно, сетки на графике
        self.axes.grid(self.options_menu.grid_cb.isChecked())

        # рисуем график
        self.canvas.draw()

    def show_about(self):
        """
        отображение диалогового окошка "about".
        """
        message = '''<font size="+2">%s</font>
            <p>Дипломная работа на тему системы дифференциальных уравнений Лотки-Вольтерра.
            <p>Написана %s, группа КА-73.
            ''' %(APP_NAME, AUTHOR)

        QtWidgets.QMessageBox.about(self, 'About' + APP_NAME, message)

class AppForm_4_species(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)

        # название окна
        self.setWindowTitle(APP_NAME)

        # Создание в меню параметров в виджете док-станции
        self.options_menu = OptionsMenu_4_species()
        dock = QtWidgets.QDockWidget('Настройки коэффициентов', self)
        dock.setFeatures(
            QtWidgets.QDockWidget.NoDockWidgetFeatures |
            QtWidgets.QDockWidget.DockWidgetMovable |
            QtWidgets.QDockWidget.DockWidgetFloatable
        )
        dock.setAllowedAreas(
            QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea,
        )
        dock.setWidget(self.options_menu)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, dock)

        # Подключение сигналов из меню параметров
        self.options_menu.update_btn.clicked.connect(self.clear_graph)
        self.options_menu.update_btn.clicked.connect(self.calculate_data)

        self.options_menu.clear_graph_btn.clicked.connect(self.clear_graph)
        self.options_menu.legend_cb.stateChanged.connect(self.redraw_graph)
        self.options_menu.grid_cb.stateChanged.connect(self.redraw_graph)
        self.options_menu.legend_loc_cb.currentIndexChanged.connect(self.redraw_graph)

        # создание графика
        fig = Figure((7.0, 3.0), dpi=100)
        self.canvas = backend_qt5agg.FigureCanvasQTAgg(fig)
        self.canvas.setParent(self)
        self.axes = fig.add_subplot(111)
        backend_qt5agg.NavigationToolbar2QT(self.canvas, self.canvas)

        # инициализация графа
        self.clear_graph()

        self.setCentralWidget(self.canvas)

        # создать менюбар действий

        about_action = QtWidgets.QAction('&About', self)
        about_action.setToolTip('About')
        about_action.setIcon(QtGui.QIcon(':/resources/icon_info.png'))
        about_action.triggered.connect(self.show_about)

     # создать менюбар
        file_exit_action = QtWidgets.QAction('&Exit', self)
        file_exit_action.setToolTip('Exit')
        file_exit_action.setIcon(QtGui.QIcon(':/resources/door_open.png'))
        file_exit_action.triggered.connect(self.close)

        file_menu = self.menuBar().addMenu('&Exit')
        file_menu.addAction(file_exit_action)

        help_menu = self.menuBar().addMenu('&Help')
        help_menu.addAction(about_action)

    def calculate_data(self):
        self.options_menu.update_btn.setEnabled(False)
        # объект GrowthCalculator
        growth = GrowthCalculator()

        # Update the GrowthCalculator parameters from the GUI options

        growth.b1 = self.options_menu.b1_sb.value()
        growth.a11 = self.options_menu.a11_sb.value()
        growth.a12 = self.options_menu.a12_sb.value()
        growth.a13 = self.options_menu.a13_sb.value()

        growth.b2 = self.options_menu.b2_sb.value()
        growth.a21 = self.options_menu.a21_sb.value()
        growth.a22 = self.options_menu.a22_sb.value()
        growth.a23 = self.options_menu.a23_sb.value()

        growth.b3 = self.options_menu.b3_sb.value()
        growth.a31 = self.options_menu.a31_sb.value()
        growth.a32 = self.options_menu.a32_sb.value()
        growth.a33 = self.options_menu.a33_sb.value()

        growth.b4 = self.options_menu.b4_sb.value()
  #      growth.a41 = self.options_menu.a41_sb.value()
   #     growth.a42 = self.options_menu.a42_sb.value()

        growth.predator = self.options_menu.predator_sb.value()
   #     growth.predators2 = self.options_menu.predator2_sb.value()
        growth.prey1 = self.options_menu.prey1_sb.value()
        growth.prey2 = self.options_menu.prey2_sb.value()
   #     growth.predator3 = self.options_menu.predator3_sb.value()
        growth.superpredator = self.options_menu.superpredator_sb.value()

        growth.iterations = self.options_menu.iterations_sb.value()
        growth.dt = self.options_menu.timedelta_sb.value()

        # Calculate the population growths
        results = growth.calculate()
        self.predator_history.extend(results['predator'])
        self.prey1_history.extend(results['prey1'])
        self.prey2_history.extend(results['prey2'])
        self.superpredator_history.extend(results['superpredator'])
     #   self.predator2_history.extend(results['predator2'])
     #   self.predator3_history.extend(results['predator3'])
        if (len(self.predator_history) == 0 and
                len(self.prey1_history) == 0 and
                len(self.prey2_history) == 0 and
                len(self.superpredator_history) == 0):
            QtWidgets.QMessageBox.information(self, 'Error', 'Ошибка')
            self.options_menu.update_btn.setEnabled(True)
            return

        # последнее в векторе количество популяции на панель инструментов параметров
      #  print('self.predator_history[-1]', self.predator_history[-1])
      #  self.options_menu.predator_sb.setValue(self.predator_history[-1])
      #  self.options_menu.prey_sb.setValue(self.prey_history[-1])
      #  self.options_menu.superpredators_sb.setValue(self.superpredator_history[-1])
        # перерисовать граф
        self.redraw_graph()
        self.options_menu.update_btn.setEnabled(True)

    def clear_graph(self):
        # очистить историю популяций
        self.predator_history = []
        self.prey1_history = []
        self.superpredator_history = []
        self.prey2_history = []

        # перерисовать граф
        self.redraw_graph()

    def redraw_graph(self):
        # очистить граф
        self.axes.clear()

        # Create the graph labels
        self.axes.set_title('Цикл роста хищников, суперхищников и двух видов жертв')
        self.axes.set_xlabel('Итерации')
        self.axes.set_ylabel('Размер популяции')

        # Plot the current population data
        if self.prey1_history:
            self.axes.plot(self.prey1_history, 'g-', color='#0a0b0c3a', linewidth=6, label='жертвы вида 1')
        if self.predator_history:
            self.axes.plot(self.predator_history, 'r-', color='#0d7b0c5a', linewidth=6, label='хищники')
        if self.superpredator_history:
            self.axes.plot(self.superpredator_history, 'b-', label='суперхищники')
        if self.prey2_history:
            self.axes.plot(self.prey2_history, 'r-',  label='жертвы вида 2')

        # если нужно, создаём легенду
        if self.options_menu.legend_cb.isChecked():
            if self.prey1_history or self.predator_history or self.superpredator_history or self.prey2_history:
                legend_loc = str(
                    self.options_menu.legend_loc_cb.currentText()
                ).lower()
                legend = matplotlib.font_manager.FontProperties(size=10)
                self.axes.legend(loc=legend_loc, prop=legend)

        # если нужно, сетки на графике
        self.axes.grid(self.options_menu.grid_cb.isChecked())

        # рисуем график
        self.canvas.draw()

    def show_about(self):
        """
        отображение диалогового окошка "about".
        """
        message = '''<font size="+2">%s</font>
            <p>Дипломная работа на тему системы дифференциальных уравнений Лотки-Вольтерра.
            <p>Написана %s, группа КА-73.
            ''' %(APP_NAME, AUTHOR)

        QtWidgets.QMessageBox.about(self, 'About' + APP_NAME, message)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon(':/resources/icon.svg'))
    form = OptionsMenu_4_species()
    form.show()
    app.exec_()
