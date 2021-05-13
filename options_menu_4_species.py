# 3rd party modules
import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui
import PyQt5.QtWidgets as QtWidgets


class OptionsMenu_4_species(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)

        # Create the "Lotka-Volterra Coefficients" options
        self.b1_sb = QtWidgets.QDoubleSpinBox()
        self.a11_sb = QtWidgets.QDoubleSpinBox()
        self.a12_sb = QtWidgets.QDoubleSpinBox()
        #self.a13_sb = QtWidgets.QDoubleSpinBox()
        self.b2_sb = QtWidgets.QDoubleSpinBox()
        self.a21_sb = QtWidgets.QDoubleSpinBox()
        self.a22_sb = QtWidgets.QDoubleSpinBox()
        #self.a23_sb = QtWidgets.QDoubleSpinBox()
        self.b3_sb = QtWidgets.QDoubleSpinBox()
        self.a31_sb = QtWidgets.QDoubleSpinBox()
        self.a32_sb = QtWidgets.QDoubleSpinBox()
        #self.a33_sb = QtWidgets.QDoubleSpinBox()
        self.b4_sb = QtWidgets.QDoubleSpinBox()
        self.a41_sb = QtWidgets.QDoubleSpinBox()
        self.a42_sb = QtWidgets.QDoubleSpinBox()
   # = QtWidgets.QDoubleSpinBox()

        for widget in (self.b1_sb, self.a11_sb, self.a12_sb,
                       self.b2_sb, self.a21_sb, self.a22_sb,
                       self.b3_sb, self.a31_sb, self.a32_sb,
                       self.b4_sb, self.a41_sb, self.a42_sb):
            widget.setRange(0, 1)
            widget.setSingleStep(0.05)

        coeff_grid = QtWidgets.QGridLayout()
        coeff_grid.addWidget(QtWidgets.QLabel('Рождаемость жертв вида 1'), 0, 0)
        coeff_grid.addWidget(self.b1_sb, 0, 1)
        coeff_grid.addWidget(QtWidgets.QLabel('Убийства жертв вида 1 хищниками вида 1'), 1, 0)
        coeff_grid.addWidget(self.a11_sb, 1, 1)
        coeff_grid.addWidget(QtWidgets.QLabel('Убийства жертв вида 1 хищниками вида 2'), 2, 0)
        coeff_grid.addWidget(self.a12_sb, 2, 1)

        coeff_grid.addWidget(QtWidgets.QLabel('Рождаемость жертв вида 2'), 3, 0)
        coeff_grid.addWidget(self.b2_sb, 3, 1)
        coeff_grid.addWidget(QtWidgets.QLabel('Убийства жертв вида 2 хищниками вида 1'), 4, 0)
        coeff_grid.addWidget(self.a21_sb, 4, 1)
        coeff_grid.addWidget(QtWidgets.QLabel('Убийства жертв вида 2 хищниками вида 2'), 5, 0)
        coeff_grid.addWidget(self.a22_sb, 5, 1)

        coeff_grid.addWidget(QtWidgets.QLabel('Смертность хищников вида 1 от голода'), 6, 0)
        coeff_grid.addWidget(self.b3_sb, 6, 1)
        coeff_grid.addWidget(QtWidgets.QLabel('Прирост хищников вида 1 за счёт убийства жертв вида 1'), 7, 0)
        coeff_grid.addWidget(self.a31_sb, 7, 1)
        coeff_grid.addWidget(QtWidgets.QLabel('Прирост хищников вида 1 за счёт убийства жертв вида 2'), 8, 0)
        coeff_grid.addWidget(self.a32_sb, 8, 1)

        coeff_grid.addWidget(QtWidgets.QLabel('Смертность хищников вида 2 от голода'), 9, 0)
        coeff_grid.addWidget(self.b4_sb, 9, 1)
        coeff_grid.addWidget(QtWidgets.QLabel('Прирост хищников вида 2 за счёт убийства жертв вида 1'), 10, 0)
        coeff_grid.addWidget(self.a41_sb, 10, 1)
        coeff_grid.addWidget(QtWidgets.QLabel('Прирост хищников вида 3 за счёт убийства жертв вида 2'), 11, 0)
        coeff_grid.addWidget(self.a42_sb, 11, 1)

        coeff_gb = QtWidgets.QGroupBox('Коэффициенты уравнения Лотки-Вольтерра:')
        coeff_gb.setLayout(coeff_grid)

        # Create the "Other Parameters" options
        self.predator1_sb = QtWidgets.QDoubleSpinBox()
        self.predator1_sb.setRange(0, 100000)
        self.predator1_sb.setSingleStep(1)

        self.predator2_sb = QtWidgets.QDoubleSpinBox()
        self.predator2_sb.setRange(0, 100000)
        self.predator2_sb.setSingleStep(1)

        self.prey1_sb = QtWidgets.QDoubleSpinBox()
        self.prey1_sb.setRange(0, 100000)
        self.prey1_sb.setSingleStep(1)

        self.prey2_sb = QtWidgets.QDoubleSpinBox()
        self.prey2_sb.setRange(0, 100000)
        self.prey2_sb.setSingleStep(1)

        #self.superpredators_sb = QtWidgets.QDoubleSpinBox()
        #self.superpredators_sb.setRange(0, 100000)
        #self.superpredators_sb.setSingleStep(1)

        self.iterations_sb = QtWidgets.QSpinBox()
        self.iterations_sb.setRange(0, 100000)
        self.iterations_sb.setSingleStep(100)

        self.timedelta_sb = QtWidgets.QDoubleSpinBox()
        self.timedelta_sb.setRange(0, 100)
        self.timedelta_sb.setSingleStep(0.05)

        other_grid = QtWidgets.QGridLayout()
        other_grid.addWidget(QtWidgets.QLabel('Популяция хищников вида 1'), 0, 0)
        other_grid.addWidget(self.predator1_sb, 0, 1)
        other_grid.addWidget(QtWidgets.QLabel('Популяция хищников вида 2'), 1, 0)
        other_grid.addWidget(self.predator2_sb, 1, 1)

        other_grid.addWidget(QtWidgets.QLabel('Популяция жертв вида 1'), 2, 0)
        other_grid.addWidget(self.prey1_sb, 2, 1)
        other_grid.addWidget(QtWidgets.QLabel('Популяция жертв вида 2'), 3, 0)
        other_grid.addWidget(self.prey2_sb, 3, 1)

        other_grid.addWidget(QtWidgets.QLabel('Итерации'), 4, 0)
        other_grid.addWidget(self.iterations_sb, 4, 1)
        other_grid.addWidget(QtWidgets.QLabel('Время дельта'), 5, 0)
        other_grid.addWidget(self.timedelta_sb, 5, 1)

        other_gb = QtWidgets.QGroupBox('Другие параметры:')
        other_gb.setLayout(other_grid)

        # Create the "Graph Options" options
        self.legend_cb = QtWidgets.QCheckBox('Показать легенду')
        self.legend_cb.setChecked(True)
        self.legend_cb.stateChanged.connect(self.legend_change)

        self.grid_cb = QtWidgets.QCheckBox('Показать сетку')
        self.grid_cb.setChecked(True)
        self.legend_loc_lbl = QtWidgets.QLabel('Местоположение легенды')
        self.legend_loc_cb = QtWidgets.QComboBox()
        self.legend_loc_cb.addItems([x.title() for x in [
            'right',
            'center',
            'lower left',
            'center right',
            'upper left',
            'center left',
            'upper right',
            'lower right',
            'upper center',
            'lower center',
            'best',
        ]])
        self.legend_loc_cb.setCurrentIndex(6)

        cb_box = QtWidgets.QHBoxLayout()
        cb_box.addWidget(self.legend_cb)
        cb_box.addWidget(self.grid_cb)

        legend_box = QtWidgets.QHBoxLayout()
        legend_box.addWidget(self.legend_loc_cb)
        legend_box.addStretch()

        graph_box = QtWidgets.QVBoxLayout()
        graph_box.addLayout(cb_box)
        graph_box.addWidget(self.legend_loc_lbl)
        graph_box.addLayout(legend_box)

        graph_gb = QtWidgets.QGroupBox('Настройки графика:')
        graph_gb.setLayout(graph_box)

        # Create the update/reset buttons
        self.update_btn = QtWidgets.QPushButton(
            QtGui.QIcon(':/resources/calculator.png'),
            'Запуск итераций')

        self.reset_values_btn = QtWidgets.QPushButton(
            QtGui.QIcon(':/resources/arrow_undo.png'),
            'Сброс значений')
        self.clear_graph_btn = QtWidgets.QPushButton(
            QtGui.QIcon(':/resources/chart_line_delete.png'),
            'Очистить график')

        self.reset_values_btn.clicked.connect(self.reset_values)

        # Create the main layout
        container = QtWidgets.QVBoxLayout()
        container.addWidget(coeff_gb)
        container.addWidget(other_gb)
        container.addWidget(graph_gb)
        container.addWidget(self.update_btn)
        container.addStretch()
        container.addStretch()
        container.addWidget(self.reset_values_btn)
        container.addWidget(self.clear_graph_btn)
        self.setLayout(container)

        # Populate the widgets with values
        self.reset_values()

    def reset_values(self):
        """
        Значения по умолчанию.
        """

#        self.a11_sb.setValue(1.0)
        self.b1_sb.setValue(0.1)
        self.a11_sb.setValue(0.1)
        self.a12_sb.setValue(0.1)
    #    self.a13_sb.setValue(0.1)

        self.b2_sb.setValue(0.1)
        self.a21_sb.setValue(0.1)
        self.a22_sb.setValue(0.1)
      #  self.a23_sb.setValue(0.1)

        self.b3_sb.setValue(0.1)
        self.a31_sb.setValue(0.1)
        self.a32_sb.setValue(0.1)
      #  self.a33_sb.setValue(0.1)

        self.b4_sb.setValue(0.1)
        self.a41_sb.setValue(0.1)
        self.a42_sb.setValue(0.1)
     #   self.a43_sb.setValue(0.1)

        self.predator1_sb.setValue(5)
        self.prey1_sb.setValue(10)
        self.predator2_sb.setValue(5)
        self.prey2_sb.setValue(10)
      #  self.superpredators_sb.setValue(5)
        self.iterations_sb.setValue(1000)
        self.timedelta_sb.setValue(0.02)

    def legend_change(self):
        self.legend_loc_cb.setEnabled(self.legend_cb.isChecked())
        self.legend_loc_lbl.setEnabled(self.legend_cb.isChecked())
