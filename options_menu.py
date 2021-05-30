# 3rd party modules
import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui
import PyQt5.QtWidgets as QtWidgets

class OptionsMenu_3_species(QtWidgets.QWidget):
    def __init__(self, parent=None):
        self.settings_path = 'settings\\coef.json'

        QtWidgets.QWidget.__init__(self, parent)

        # Create the "Lotka-Volterra Coefficients" options
        self.b1_sb = QtWidgets.QDoubleSpinBox()
        self.b1_sb.setObjectName("b1_sb")
        self.a12_sb = QtWidgets.QDoubleSpinBox()
        self.a12_sb.setObjectName("a12_sb")
        self.a13_sb = QtWidgets.QDoubleSpinBox()
        self.a13_sb.setObjectName("a13_sb")

        self.b2_sb = QtWidgets.QDoubleSpinBox()
        self.b2_sb.setObjectName("b2_sb")
        self.a21_sb = QtWidgets.QDoubleSpinBox()
        self.a21_sb.setObjectName("a21_sb")
        self.a23_sb = QtWidgets.QDoubleSpinBox()
        self.a23_sb.setObjectName("a23_sb")

        self.b3_sb = QtWidgets.QDoubleSpinBox()
        self.b3_sb.setObjectName("b3_sb")
        self.a31_sb = QtWidgets.QDoubleSpinBox()
        self.a31_sb.setObjectName("a31_sb")
        self.a32_sb = QtWidgets.QDoubleSpinBox()
        self.a32_sb.setObjectName("a32_sb")

        for widget in (self.b1_sb, self.a12_sb, self.a13_sb,
                       self.b2_sb, self.a21_sb, self.a23_sb,
                       self.b3_sb, self.a31_sb, self.a32_sb):
            widget.setRange(0, 1)
            widget.setSingleStep(0.05)

        coeff_grid = QtWidgets.QGridLayout()
        self.coeff_grid = coeff_grid
        coeff_grid.addWidget(QtWidgets.QLabel('Народжуваність жертв'), 0, 0)
        coeff_grid.addWidget(self.b1_sb, 0, 1)
        coeff_grid.addWidget(QtWidgets.QLabel('Смертність хижаків'), 1, 0)
        coeff_grid.addWidget(self.b2_sb, 1, 1)
        coeff_grid.addWidget(QtWidgets.QLabel('Смертність суперхижаків'), 2, 0)
        coeff_grid.addWidget(self.b3_sb, 2, 1)

        coeff_grid.addWidget(QtWidgets.QLabel('Вбивства жертв хижаками'), 3, 0)
        coeff_grid.addWidget(self.a12_sb, 3, 1)
        coeff_grid.addWidget(QtWidgets.QLabel('Вбивства жертв суперхижаками'), 4, 0)
        coeff_grid.addWidget(self.a13_sb, 4, 1)

        coeff_grid.addWidget(QtWidgets.QLabel('Приріст хижаків за рахунок вбивства жертв'), 6, 0)
        coeff_grid.addWidget(self.a21_sb, 6, 1)
        coeff_grid.addWidget(QtWidgets.QLabel('Смертність хижаків через суперхижаків'), 7, 0)
        coeff_grid.addWidget(self.a23_sb, 7, 1)

        coeff_grid.addWidget(QtWidgets.QLabel('Приріст суперхижаків за рахунок вбивства жертв'), 8, 0)
        coeff_grid.addWidget(self.a31_sb, 8, 1)
        coeff_grid.addWidget(QtWidgets.QLabel('Приріст хижаків за рахунок вбивства хижаків'), 9, 0)
        coeff_grid.addWidget(self.a32_sb, 9, 1)

        coeff_gb = QtWidgets.QGroupBox('Коефіцієнти рівняння Лотки-Вольтерра:')
        coeff_gb.setLayout(coeff_grid)

        # Create the "Other Parameters" options
        self.predator_sb = QtWidgets.QDoubleSpinBox()
        self.predator_sb.setRange(0, 100000)
        self.predator_sb.setSingleStep(1)
        self.predator_sb.setObjectName("predator_sb")

        self.superpredator_sb = QtWidgets.QDoubleSpinBox()
        self.superpredator_sb.setRange(0, 100000)
        self.superpredator_sb.setSingleStep(1)
        self.superpredator_sb.setObjectName("superpredator_sb")
        #      self.predator3_sb = QtWidgets.QDoubleSpinBox()
        #     self.predator3_sb.setRange(0, 100000)
        #     self.predator3_sb.setSingleStep(1)
        #      self.superpredator_sb = QtWidgets.QDoubleSpinBox()
        #      self.superpredator_sb.setRange(0, 100000)
        #      self.superpredator_sb.setSingleStep(1)

        self.prey_sb = QtWidgets.QDoubleSpinBox()
        self.prey_sb.setRange(0, 100000)
        self.prey_sb.setSingleStep(1)
        self.prey_sb.setObjectName("prey_sb")

        self.iterations_sb = QtWidgets.QSpinBox()
        self.iterations_sb.setRange(0, 1000000)
        self.iterations_sb.setSingleStep(100)

        self.timedelta_sb = QtWidgets.QDoubleSpinBox()
        self.timedelta_sb.setRange(0, 100)
        self.timedelta_sb.setSingleStep(0.05)

        other_grid = QtWidgets.QGridLayout()
        other_grid.addWidget(QtWidgets.QLabel('Популяція хижаків'), 0, 0)
        other_grid.addWidget(self.predator_sb, 0, 1)
        other_grid.addWidget(QtWidgets.QLabel('Популяція жертв'), 1, 0)
        other_grid.addWidget(self.prey_sb, 1, 1)
        other_grid.addWidget(QtWidgets.QLabel('Популяція суперхижаків'), 3, 0)
        other_grid.addWidget(self.superpredator_sb, 3, 1)
        #       other_grid.addWidget(QtWidgets.QLabel('Популяция суперхищников'), 1, 0)
        #      other_grid.addWidget(self.superpredator_sb, 1, 1)

        other_grid.addWidget(QtWidgets.QLabel('Ітерації'), 5, 0)
        other_grid.addWidget(self.iterations_sb, 5, 1)
        other_grid.addWidget(QtWidgets.QLabel('Час дельта'), 6, 0)
        other_grid.addWidget(self.timedelta_sb, 6, 1)

        other_gb = QtWidgets.QGroupBox('Інші параметри:')
        other_gb.setLayout(other_grid)

        # Create the "Graph Options" options
        self.legend_cb = QtWidgets.QCheckBox('Показати легенду')
        self.legend_cb.setChecked(True)
        self.legend_cb.stateChanged.connect(self.legend_change)

        self.grid_cb = QtWidgets.QCheckBox('Показати сітку')
        self.grid_cb.setChecked(True)
        self.legend_loc_lbl = QtWidgets.QLabel('Місцезнаходження легенди')
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

        graph_gb = QtWidgets.QGroupBox('Налаштування графіка:')
        graph_gb.setLayout(graph_box)

        # Create the update/reset buttons
        self.update_btn = QtWidgets.QPushButton(
            QtGui.QIcon(':/resources/calculator.png'),
            'Запустити')

        self.reset_values_btn = QtWidgets.QPushButton(
            QtGui.QIcon(':/resources/arrow_undo.png'),
            'Значення за замовченням')
        self.clear_graph_btn = QtWidgets.QPushButton(
            QtGui.QIcon(':/resources/chart_line_delete.png'),
            'Очистити графік')

        self.reset_values_btn.clicked.connect(self.reset_values)

        main_actions_vbox = QtWidgets.QVBoxLayout()
        main_actions_vbox.addWidget(self.update_btn)
        main_actions_vbox.addWidget(self.reset_values_btn)
        main_actions_vbox.addWidget(self.clear_graph_btn)

        self.save_btn = QtWidgets.QPushButton('зберігти')
        self.save_btn.clicked.connect(self.save_coeff)
        self.load_drop_box = QtWidgets.QComboBox()
        self.load_drop_box.setEditable(True)
        self.load_drop_box.currentIndexChanged.connect(self.load_coeff)

        store_load_settings_vbox = QtWidgets.QVBoxLayout()
        store_load_settings_vbox.addWidget(self.save_btn)
        store_load_settings_vbox.addWidget(self.load_drop_box)
        store_load_settings_vbox.addStretch()

        main_actions_hbox = QtWidgets.QHBoxLayout()
        main_actions_hbox.addLayout(store_load_settings_vbox)
        main_actions_hbox.addLayout(main_actions_vbox)

        # Create the main layout
        container = QtWidgets.QVBoxLayout()
        container.addWidget(coeff_gb)
        container.addWidget(other_gb)
        container.addWidget(graph_gb)
        container.addLayout(main_actions_hbox)
        self.setLayout(container)

        # Populate the widgets with values
        self.reset_values()
        self.load_coeff_names()

    def reset_values(self):
        """
        Значения по умолчанию.
        """

        self.b1_sb.setValue(0.1)
        self.a12_sb.setValue(0.1)
        self.a13_sb.setValue(0.1)

        self.b2_sb.setValue(0.1)
        self.a21_sb.setValue(0.1)
        self.a23_sb.setValue(0.1)

        self.b3_sb.setValue(0.1)
        self.a31_sb.setValue(0.1)
        self.a32_sb.setValue(0.1)

        self.predator_sb.setValue(5)
        self.superpredator_sb.setValue(5)
        self.prey_sb.setValue(5)

        #  self.superpredators_sb.setValue(5)
        self.iterations_sb.setValue(1000)
        self.timedelta_sb.setValue(0.02)

    def legend_change(self):
        self.legend_loc_cb.setEnabled(self.legend_cb.isChecked())
        self.legend_loc_lbl.setEnabled(self.legend_cb.isChecked())

    def load_coeff(self):
        current_idx = self.load_drop_box.currentIndex()

        if current_idx == 0:
            return

        coeff_preset_list = self.readSettings()
        for preset in coeff_preset_list:
            preset_name = list(preset.keys())[0]

            if preset_name == self.load_drop_box.currentText():
                coeff_dict = preset[preset_name]
                self.b1_sb.setValue(coeff_dict['b1_sb'])
                self.a12_sb.setValue(coeff_dict['a12_sb'])
                self.a13_sb.setValue(coeff_dict['a13_sb'])

                self.b2_sb.setValue(coeff_dict['b2_sb'])
                self.a21_sb.setValue(coeff_dict['a21_sb'])
                self.a23_sb.setValue(coeff_dict['a23_sb'])

                self.b3_sb.setValue(coeff_dict['b3_sb'])
                self.a31_sb.setValue(coeff_dict['a31_sb'])
                self.a32_sb.setValue(coeff_dict['a32_sb'])


    def load_coeff_names(self):
        coeff_preset_list = self.readSettings()
        self.load_drop_box.clear()
        self.load_drop_box.addItem('')

        if len(coeff_preset_list) == 0:
            return

        for preset in coeff_preset_list:
            self.load_drop_box.addItem(list(preset.keys())[0])

    def save_coeff(self):
        import json
        import os

        preset_name = self.load_drop_box.currentText().strip()
        if len(preset_name) == 0:
            print('Пустое имя для пресета с коэфициентами')
            return

        coeff_preset_list = self.readSettings()

        coeff_dict = dict()
        for widget in (self.b1_sb, self.a12_sb, self.a13_sb,
                       self.b2_sb, self.a21_sb, self.a23_sb,
                       self.b3_sb, self.a31_sb, self.a32_sb):
            if len(widget.objectName()) == 0:
                print('нет имя для переменной со значением: ', widget.value())
                continue
            coeff_dict[widget.objectName()] = widget.value()

        coeff_preset_list.append({preset_name: coeff_dict})
        self.writeSettings(coeff_preset_list)
        self.load_coeff_names()

    def readSettings(self) -> list:
        import json
        import os

        if not os.path.exists(self.settings_path):
            os.mkdir('settings')

        try:
            with open(self.settings_path) as json_file:
                coeff_preset_list = json.load(json_file)
        except FileNotFoundError as ex:
            coeff_preset_list = list()

        return coeff_preset_list

    def writeSettings(self, coeff_preset_list):
        import json
        import os

        json_coeff = json.dumps(coeff_preset_list, indent=2)
        with open(self.settings_path, 'w') as file:
            file.write(json_coeff)

