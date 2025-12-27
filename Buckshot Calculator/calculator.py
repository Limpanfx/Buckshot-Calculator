import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QSpinBox, QVBoxLayout,
    QHBoxLayout, QGroupBox, QComboBox, QGridLayout, QPushButton
)
from PyQt6.QtCore import Qt


class BuckshotCalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Buckshot Roulette Probability Calculator")
        self.setMinimumWidth(560)

        self.max_shells = 8
        self.prev_live = 0
        self.prev_blank = 0
        self.is_resetting = False

        self.init_ui()
        self.reset_all()

    def init_ui(self):
        layout = QVBoxLayout()

        # --- Shell configuration ---
        config_group = QGroupBox("Shell Configuration")
        config_layout = QGridLayout()

        self.current_shell = QSpinBox()
        self.current_shell.setRange(1, self.max_shells)

        self.live_spin = QSpinBox()
        self.live_spin.setRange(0, self.max_shells)
        self.live_spin.valueChanged.connect(self.on_shell_change)

        self.blank_spin = QSpinBox()
        self.blank_spin.setRange(0, self.max_shells)
        self.blank_spin.valueChanged.connect(self.on_shell_change)

        self.total_label = QLabel("Total Shells: 0")

        config_layout.addWidget(QLabel("Current Shell #"), 0, 0)
        config_layout.addWidget(self.current_shell, 0, 1)
        config_layout.addWidget(QLabel("Live Shells"), 1, 0)
        config_layout.addWidget(self.live_spin, 1, 1)
        config_layout.addWidget(QLabel("Blank Shells"), 2, 0)
        config_layout.addWidget(self.blank_spin, 2, 1)
        config_layout.addWidget(self.total_label, 3, 0, 1, 2)

        config_group.setLayout(config_layout)

        # --- Known shells (phone info) ---
        known_group = QGroupBox("Known Shells (Phone Info)")
        known_layout = QGridLayout()

        self.known_boxes = {}

        for i in range(1, self.max_shells + 1):
            combo = QComboBox()
            combo.addItems(["Unknown", "Live", "Blank"])
            combo.currentIndexChanged.connect(self.update_probabilities)
            self.known_boxes[i] = combo

            known_layout.addWidget(QLabel(f"Shell {i}"), (i - 1) // 4, ((i - 1) % 4) * 2)
            known_layout.addWidget(combo, (i - 1) // 4, ((i - 1) % 4) * 2 + 1)

        known_group.setLayout(known_layout)

        # --- Result display ---
        result_group = QGroupBox("Current Shot Probability")
        result_layout = QVBoxLayout()

        self.live_prob = QLabel()
        self.blank_prob = QLabel()

        self.live_prob.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.blank_prob.setAlignment(Qt.AlignmentFlag.AlignCenter)

        result_layout.addWidget(self.live_prob)
        result_layout.addWidget(self.blank_prob)

        result_group.setLayout(result_layout)

        # --- Buttons ---
        button_layout = QHBoxLayout()
        self.reset_button = QPushButton("Reset")
        self.reset_button.clicked.connect(self.reset_all)
        button_layout.addStretch()
        button_layout.addWidget(self.reset_button)
        button_layout.addStretch()

        layout.addWidget(config_group)
        layout.addWidget(known_group)
        layout.addWidget(result_group)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    # ---------------- LOGIC ----------------

    def reset_all(self):
        self.is_resetting = True

        self.prev_live = 0
        self.prev_blank = 0

        self.current_shell.setValue(1)
        self.live_spin.setValue(0)
        self.blank_spin.setValue(0)

        for combo in self.known_boxes.values():
            combo.setCurrentIndex(0)

        self.is_resetting = False
        self.update_probabilities()

    def on_shell_change(self):
        if self.is_resetting:
            return

        live = self.live_spin.value()
        blank = self.blank_spin.value()

        # Auto-advance shell when one is removed
        if live < self.prev_live or blank < self.prev_blank:
            self.current_shell.setValue(self.current_shell.value() + 1)

        self.prev_live = live
        self.prev_blank = blank

        self.update_probabilities()

    def update_probabilities(self):
        live = self.live_spin.value()
        blank = self.blank_spin.value()
        total = live + blank
        current = self.current_shell.value()

        self.total_label.setText(f"Total Shells: {total}")

        if total == 0:
            self.live_prob.setText("Live Probability: N/A")
            self.blank_prob.setText("Blank Probability: N/A")
            return

        # Gather known shells
        known = {}
        for i in range(1, total + 1):
            state = self.known_boxes[i].currentText()
            if state != "Unknown":
                known[i] = state

        # Current shell is known
        if current in known:
            if known[current] == "Live":
                self.live_prob.setText("Live Probability: 100%")
                self.blank_prob.setText("Blank Probability: 0%")
            else:
                self.live_prob.setText("Live Probability: 0%")
                self.blank_prob.setText("Blank Probability: 100%")
            return

        known_live = sum(1 for v in known.values() if v == "Live")
        known_blank = sum(1 for v in known.values() if v == "Blank")

        remaining_live = live - known_live
        remaining_blank = blank - known_blank
        remaining_unknown = remaining_live + remaining_blank

        if remaining_unknown <= 0:
            self.live_prob.setText("Live Probability: 0%")
            self.blank_prob.setText("Blank Probability: 0%")
            return

        self.live_prob.setText(
            f"Live Probability: {remaining_live / remaining_unknown:.2%}"
        )
        self.blank_prob.setText(
            f"Blank Probability: {remaining_blank / remaining_unknown:.2%}"
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BuckshotCalculator()
    window.show()
    sys.exit(app.exec())
