import sys
import pandas as pd
import random
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QTableWidget, QTableWidgetItem, QComboBox, QSlider,
                             QPushButton, QTabWidget, QGroupBox, QSplitter, QHeaderView)
from PyQt5.QtCore import Qt
from PyQt5.QtChart import QChart, QChartView, QBarSeries, QBarSet, QBarCategoryAxis, QValueAxis
from PyQt5.QtGui import QFont


class VTBAnalyticsApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.df = None
        self.filtered_df = None
        self.initUI()
        self.generate_sample_data()

    def initUI(self):
        self.setWindowTitle("Панель аналитики данных ВТБ")
        self.setGeometry(100, 100, 1400, 900)

        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Основной layout
        main_layout = QHBoxLayout(central_widget)

        # Создаем разделитель
        splitter = QSplitter(Qt.Horizontal)

        # Левая панель - фильтры
        left_panel = self.create_filters_panel()
        splitter.addWidget(left_panel)

        # Правая панель - данные и графики
        right_panel = self.create_main_panel()
        splitter.addWidget(right_panel)

        # Устанавливаем пропорции
        splitter.setSizes([300, 1100])

        main_layout.addWidget(splitter)

    def create_filters_panel(self):
        """Создает панель с фильтрами"""
        panel = QWidget()
        layout = QVBoxLayout(panel)

        # Заголовок
        title = QLabel("🔍 Фильтры данных")
        title.setFont(QFont("Arial", 12, QFont.Bold))
        layout.addWidget(title)

        # Фильтр по возрасту
        age_group = QGroupBox("Возраст")
        age_layout = QVBoxLayout(age_group)

        self.age_min_label = QLabel("Мин: 18")
        self.age_max_label = QLabel("Макс: 75")
        age_layout.addWidget(self.age_min_label)
        age_layout.addWidget(self.age_max_label)

        self.age_slider = QSlider(Qt.Horizontal)
        self.age_slider.setRange(18, 75)
        self.age_slider.setValue(18)
        self.age_slider.valueChanged.connect(self.update_age_filter)
        age_layout.addWidget(self.age_slider)

        layout.addWidget(age_group)

        # Фильтр по доходу
        income_group = QGroupBox("Доход (тыс. руб)")
        income_layout = QVBoxLayout(income_group)

        self.income_min_label = QLabel("Мин: 20")
        self.income_max_label = QLabel("Макс: 300")
        income_layout.addWidget(self.income_min_label)
        income_layout.addWidget(self.income_max_label)

        self.income_slider = QSlider(Qt.Horizontal)
        self.income_slider.setRange(20, 300)
        self.income_slider.setValue(20)
        self.income_slider.valueChanged.connect(self.update_income_filter)
        income_layout.addWidget(self.income_slider)

        layout.addWidget(income_group)

        # Фильтр по городу
        city_group = QGroupBox("Город")
        city_layout = QVBoxLayout(city_group)

        self.city_combo = QComboBox()
        self.city_combo.addItem("Все города")
        city_layout.addWidget(self.city_combo)

        layout.addWidget(city_group)

        # Кнопка применения фильтров
        self.apply_btn = QPushButton("Применить фильтры")
        self.apply_btn.clicked.connect(self.apply_filters)
        layout.addWidget(self.apply_btn)

        # Кнопка сброса
        self.reset_btn = QPushButton("Сбросить фильтры")
        self.reset_btn.clicked.connect(self.reset_filters)
        layout.addWidget(self.reset_btn)

        # Статистика
        stats_group = QGroupBox("📊 Статистика")
        stats_layout = QVBoxLayout(stats_group)

        self.stats_label = QLabel("Всего клиентов: 0\nСредний доход: 0\nСредний баланс: 0")
        self.stats_label.setWordWrap(True)
        stats_layout.addWidget(self.stats_label)

        layout.addWidget(stats_group)

        layout.addStretch()

        return panel

    def create_main_panel(self):
        """Создает основную панель с данными и графиками"""
        panel = QWidget()
        layout = QVBoxLayout(panel)

        # Вкладки
        self.tabs = QTabWidget()

        # Вкладка с данными
        self.data_tab = QWidget()
        data_layout = QVBoxLayout(self.data_tab)

        self.data_table = QTableWidget()
        data_layout.addWidget(self.data_table)

        # Вкладка с аналитикой
        self.analytics_tab = QWidget()
        analytics_layout = QVBoxLayout(self.analytics_tab)

        # Графики будут добавляться динамически
        self.chart_view = QChartView()
        analytics_layout.addWidget(self.chart_view)

        # Вкладка с инсайтами
        self.insights_tab = QWidget()
        insights_layout = QVBoxLayout(self.insights_tab)

        self.insights_table = QTableWidget()
        insights_layout.addWidget(self.insights_table)

        # Добавляем вкладки
        self.tabs.addTab(self.data_tab, "📋 Данные клиентов")
        self.tabs.addTab(self.analytics_tab, "📈 Аналитика")

        self.tabs.currentChanged.connect(self.on_tab_changed)

        layout.addWidget(self.tabs)

        return panel

    def generate_sample_data(self):
        """Генерирует примерные данные клиентов ВТБ"""
        cities = ['Москва', 'Санкт-Петербург', 'Казань', 'Екатеринбург', 'Новосибирск']

        data = []
        for i in range(100):
            age = random.randint(18, 75)
            income = random.randint(20000, 300000)
            balance = random.randint(5000, 500000)
            assets = random.randint(10000, 1000000)
            transactions = random.randint(1, 50)
            city = random.choice(cities)

            data.append({
                'ID': i + 1,
                'Возраст': age,
                'Доход': income,
                'Баланс': balance,
                'Активы': assets,
                'Транзакции': transactions,
                'Город': city
            })

        self.df = pd.DataFrame(data)
        self.filtered_df = self.df.copy()

        # Обновляем комбобокс городов
        self.city_combo.clear()
        self.city_combo.addItem("Все города")
        for city in sorted(self.df['Город'].unique()):
            self.city_combo.addItem(city)

        self.apply_filters()

    def update_age_filter(self):
        """Обновляет label фильтра возраста"""
        value = self.age_slider.value()
        self.age_min_label.setText(f"Мин: {value}")

    def update_income_filter(self):
        """Обновляет label фильтра дохода"""
        value = self.income_slider.value()
        self.income_min_label.setText(f"Мин: {value}")

    def apply_filters(self):
        """Применяет выбранные фильтры"""
        min_age = self.age_slider.value()
        min_income = self.income_slider.value() * 1000  # переводим в рубли
        selected_city = self.city_combo.currentText()

        # Применяем фильтры
        self.filtered_df = self.df[
            (self.df['Возраст'] >= min_age) &
            (self.df['Доход'] >= min_income)
            ]

        if selected_city != "Все города":
            self.filtered_df = self.filtered_df[self.filtered_df['Город'] == selected_city]

        self.update_display()

    def reset_filters(self):
        """Сбрасывает все фильтры"""
        self.age_slider.setValue(18)
        self.income_slider.setValue(20)
        self.city_combo.setCurrentIndex(0)
        self.apply_filters()

    def update_display(self):
        """Обновляет все отображения данных"""
        self.update_data_table()
        self.update_stats()

        # Обновляем график если открыта вкладка аналитики
        if self.tabs.currentIndex() == 1:
            self.update_chart()
        elif self.tabs.currentIndex() == 2:
            self.update_insights()

    def update_data_table(self):
        """Обновляет таблицу с данными"""
        self.data_table.clear()

        if self.filtered_df.empty:
            return

        # Устанавливаем количество строк и столбцов
        self.data_table.setRowCount(len(self.filtered_df))
        self.data_table.setColumnCount(len(self.filtered_df.columns))

        # Устанавливаем заголовки
        self.data_table.setHorizontalHeaderLabels(self.filtered_df.columns)

        # Заполняем таблицу данными
        for row in range(len(self.filtered_df)):
            for col in range(len(self.filtered_df.columns)):
                value = self.filtered_df.iloc[row, col]
                item = QTableWidgetItem(str(value))
                self.data_table.setItem(row, col, item)

        # Настраиваем отображение таблицы
        self.data_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def update_stats(self):
        """Обновляет статистику"""
        if self.filtered_df.empty:
            self.stats_label.setText("Нет данных для отображения")
            return

        total_clients = len(self.filtered_df)
        avg_income = int(self.filtered_df['Доход'].mean())
        avg_balance = int(self.filtered_df['Баланс'].mean())
        avg_age = int(self.filtered_df['Возраст'].mean())

        stats_text = f"""Всего клиентов: {total_clients}
Средний доход: {avg_income:,} ₽
Средний баланс: {avg_balance:,} ₽
Средний возраст: {avg_age} лет"""

        self.stats_label.setText(stats_text)

    def update_chart(self):
        """Обновляет график распределения доходов"""
        if self.filtered_df.empty:
            return

        # Создаем гистограмму распределения доходов
        chart = QChart()
        chart.setTitle("Распределение доходов клиентов")

        # Группируем данные по диапазонам доходов
        income_ranges = ['0-50k', '50-100k', '100-150k', '150-200k', '200k+']
        ranges = [0, 50000, 100000, 150000, 200000, float('inf')]

        counts = []
        for i in range(len(ranges) - 1):
            count = len(self.filtered_df[
                            (self.filtered_df['Доход'] >= ranges[i]) &
                            (self.filtered_df['Доход'] < ranges[i + 1])
                            ])
            counts.append(count)

        series = QBarSeries()
        bar_set = QBarSet("Количество клиентов")

        for count in counts:
            bar_set.append(count)

        bar_set.setColor(Qt.blue)
        series.append(bar_set)
        chart.addSeries(series)

        # Настраиваем оси
        axis_x = QBarCategoryAxis()
        axis_x.append(income_ranges)
        chart.addAxis(axis_x, Qt.AlignBottom)
        series.attachAxis(axis_x)

        axis_y = QValueAxis()
        axis_y.setRange(0, max(counts) + 1)
        chart.addAxis(axis_y, Qt.AlignLeft)
        series.attachAxis(axis_y)

        self.chart_view.setChart(chart)

    def on_tab_changed(self, index):
        """Обрабатывает смену вкладки"""
        if index == 1:  # Вкладка аналитики
            self.update_chart()
        elif index == 2:  # Вкладка инсайтов
            self.update_insights()


def main():
    app = QApplication(sys.argv)

    # Устанавливаем стиль для лучшего внешнего вида
    app.setStyle('Fusion')

    window = VTBAnalyticsApp()
    window.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()