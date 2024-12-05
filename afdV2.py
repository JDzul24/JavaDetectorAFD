import os
import re
import sys
from typing import List, Dict, Tuple

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
    QWidget, QPushButton, QTextEdit, QLabel, QFileDialog, 
    QRadioButton, QButtonGroup, QMessageBox
)
from PyQt6.QtGui import QFont, QTextCharFormat, QColor
from PyQt6.QtCore import Qt

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

class JavaClassRecognizer:
    def __init__(self):

        self.keywords = {"abstract", "assert", "boolean", "break", "byte", "case", "catch", "char", "class", "const", "continue", "default", "do", "double", "else", "enum", "extends", "final", "finally", "float", "for", "goto", "if", "implements", "import", "instanceof", "int", "interface", "long", "native", "new", "package", "private", "protected", "public", "return", "short", "static", "strictfp", "super", "switch", "synchronized", "this", "throw", "throws", "transient", "try", "void", "volatile", "while"}


        self.state = 'q0'
        self.transitions = {
            ('q0', 'space'): 'q0',
            ('q0', 'tab'): 'q0',
            ('q0', 'newline'): 'q0',
            ('q0', 'public'): 'q1',
            ('q0', 'abstract'): 'q26',
            ('q0', 'final'): 'q27',
            ('q0', 'class'): 'q3',
            ('q0', 'private'): 'q30',
            ('q0', 'protected'): 'q31',
            ('q0', 'static'): 'q34',
            ('q0', 'strictfp'): 'q35',

            ('q1', 'space'): 'q1',
            ('q1', 'tab'): 'q1',
            ('q1', 'abstract'): 'q2',
            ('q1', 'final'): 'q28',
            ('q1', 'class'): 'q3',
            ('q1', 'static'): 'q32',
            ('q1', 'strictfp'): 'q33',

            ('q2', 'space'): 'q2',
            ('q2', 'tab'): 'q2',
            ('q2', 'final'): 'q29',
            ('q2', 'class'): 'q3',

             ('q26', 'space'): 'q26',
            ('q26', 'tab'): 'q26',
            ('q26', 'class'): 'q3',

            ('q27', 'space'): 'q27',
            ('q27', 'tab'): 'q27',
            ('q27', 'class'): 'q3',

            ('q28', 'space'): 'q28',
            ('q28', 'tab'): 'q28',
            ('q28', 'class'): 'q3',

            ('q29', 'space'): 'q29',
            ('q29', 'tab'): 'q29',
            ('q29', 'class'): 'q3',

            ('q30', 'space'): 'q30',
            ('q30', 'tab'): 'q30',
            ('q30', 'class'): 'q3',

            ('q31', 'space'): 'q31',
            ('q31', 'tab'): 'q31',
            ('q31', 'class'): 'q3',

            ('q32', 'space'): 'q32',
            ('q32', 'tab'): 'q32',
            ('q32', 'class'): 'q3',

            ('q33', 'space'): 'q33',
            ('q33', 'tab'): 'q33',
            ('q33', 'class'): 'q3',

            ('q34', 'space'): 'q34',
            ('q34', 'tab'): 'q34',
            ('q34', 'class'): 'q3',
            

            ('q35', 'space'): 'q35',
            ('q35', 'tab'): 'q35',
            ('q35', 'class'): 'q3',


            ('q3', 'space'): 'q3',
            ('q3', 'tab'): 'q3',
            ('q3', 'identifier'): 'q4',

            ('q4', 'space'): 'q5',  # Espacio después del nombre de la clase
            ('q4', 'tab'): 'q5',
            ('q4', 'newline'): 'q5',
            ('q4', 'extends'): 'q6',
            ('q4', 'implements'): 'q10',
            ('q4', '{'): 'q25', #Para cuando no hay extends ni implements

            ('q5', 'space'): 'q5',
            ('q5', 'tab'): 'q5',
            ('q5', 'extends'): 'q6',
            ('q5', 'implements'): 'q10',
            ('q5','{'): 'q25',

            ('q6', 'space'): 'q6',
            ('q6', 'tab'): 'q6',
            ('q6', 'identifier'): 'q7',

            ('q7', 'space'): 'q8',
            ('q7', 'tab'): 'q8',
            ('q7', 'implements'): 'q10',
            ('q7', '{'): 'q25', #Para cuando solo hay extends


            ('q8', 'space'): 'q8',
            ('q8', 'tab'): 'q8',
            ('q8', 'implements'): 'q10',
            ('q8','{'): 'q25',

            ('q10', 'space'): 'q10',
            ('q10', 'tab'): 'q10',
            ('q10', 'identifier'): 'q11',
            
            ('q11', 'space'): 'q12',
            ('q11', 'tab'): 'q12',
            ('q11', ','): 'q13',
            ('q11', '{'): 'q25', #Para cuando solo hay implements

            ('q12', 'space'): 'q12',
            ('q12', 'tab'): 'q12',
             ('q12', ','): 'q13',
             ('q12', '{'): 'q25',

             ('q13', 'space'): 'q13',
             ('q13', 'tab'): 'q13',
             ('q13', 'identifier'):'q14',

            ('q14', 'space'): 'q15',
             ('q14', 'tab'): 'q15',
             ('q14', ','): 'q13',
             ('q14', '{'): 'q25',

             ('q15', 'space'): 'q15',
             ('q15', 'tab'): 'q15',
             ('q15', ','): 'q13',
             ('q15', '{'): 'q25',

            ('q25', '}' ): 'q_accept'


        }
     # Set up the main window
        self.app = QApplication(sys.argv)
        self.window = QMainWindow()
        self.window.setWindowTitle("Java Class Recognizer")
        self.window.setGeometry(100, 100, 600, 700)

        # Central widget and layout
        central_widget = QWidget()
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        self.window.setCentralWidget(central_widget)

        # Status label
        self.status_label = QLabel("Select a folder to analyze")
        main_layout.addWidget(self.status_label)

        # Open Folder Button
        self.open_folder_button = QPushButton("Open Folder")
        self.open_folder_button.clicked.connect(self.open_folder)
        main_layout.addWidget(self.open_folder_button)

        # Analyze Button
        self.analyze_button = QPushButton("Analyze")
        self.analyze_button.setEnabled(False)
        self.analyze_button.clicked.connect(self.analyze_files)
        main_layout.addWidget(self.analyze_button)

        # Report Format Selection
        report_layout = QHBoxLayout()
        self.report_group = QButtonGroup()
        self.pdf_radio = QRadioButton("PDF")
        self.txt_radio = QRadioButton("TXT")
        self.pdf_radio.setChecked(True)
        self.report_group.addButton(self.pdf_radio)
        self.report_group.addButton(self.txt_radio)
        report_layout.addWidget(self.pdf_radio)
        report_layout.addWidget(self.txt_radio)
        main_layout.addLayout(report_layout)

        # Generate Report Button
        self.generate_report_button = QPushButton("Generate Report")
        self.generate_report_button.setEnabled(False)
        self.generate_report_button.clicked.connect(self.generate_report)
        main_layout.addWidget(self.generate_report_button)

        # Save Report Button
        self.save_report_button = QPushButton("Save Report")
        self.save_report_button.setEnabled(False)
        self.save_report_button.clicked.connect(self.save_report)
        main_layout.addWidget(self.save_report_button)

        # Output Text Area
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        main_layout.addWidget(self.output_text)

        # Store for declarations
        self.declarations_found = []
        self.folder_path = None

    def is_keyword(self, token):
        return token in self.keywords

    def transition(self, char):
        if char.isspace():
            input_type = 'space'
        elif char == '\t':
            input_type = 'tab'
        elif char == '\n':
            input_type = 'newline'
        elif self.is_keyword(char):
            input_type = char
        elif re.match(r'[a-zA-Z_$][a-zA-Z0-9_$]*', char):  # Valid identifier
            input_type = 'identifier'
        elif char in ['{', '}', ',', ';', '(', ')', '[', ']', '.']:
            input_type = char
        else:
            input_type = 'other'  # Unrecognized character

        next_state = self.transitions.get((self.state, input_type), 'q_error')

        if next_state != 'q_error':
            self.state = next_state
        else:
            self.state = 'q0'

    def is_accepted(self):
        return self.state == 'q_accept'

    def analyze_java_code(self, code):
        self.state = 'q0'  # Reset state for each analysis
        declarations = []
        current_declaration = ""
        start_index = 0

        for i, char in enumerate(code):
            previous_state = self.state
            self.transition(char)

            if previous_state == 'q0' and self.state != 'q0' and self.state != 'q_error':
                start_index = i
                current_declaration += char
            elif self.state != 'q0' and self.state != 'q_error':
                current_declaration += char

            if self.is_accepted():
                declarations.append((current_declaration.strip(), start_index))
                current_declaration = ""
                self.state = 'q0'  # Reset automaton

        self.transition('')  # Check if the last declaration is well-formed

        if self.is_accepted():
            declarations.append((current_declaration.strip(), start_index))

        return declarations

    def open_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self.window, "Select Folder")
        if folder_path:
            self.folder_path = folder_path
            self.analyze_button.setEnabled(True)
            self.output_text.clear()
            self.status_label.setText(f"Selected folder: {folder_path}")
            self.status_label.setStyleSheet("color: green;")
        else:
            self.analyze_button.setEnabled(False)

    def analyze_files(self):
        self.declarations_found = []
        self.output_text.clear()
        
        if self.folder_path:
            for filename in os.listdir(self.folder_path):
                if filename.endswith((".java", ".class")):  # Add other Java extensions if needed
                    filepath = os.path.join(self.folder_path, filename)
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            code = f.read()
                            declarations = self.analyze_java_code(code)
                            for declaration, index in declarations:
                                self.declarations_found.append({
                                    "filename": filename,
                                    "declaration": declaration,
                                    "index": index
                                })
                    except Exception as e:
                        QMessageBox.critical(self.window, "Error", f"Error analyzing {filename}: {e}")

            self.show_results(self.declarations_found)

            if self.declarations_found:
                self.generate_report_button.setEnabled(True)
                self.save_report_button.setEnabled(True)
        else:
            self.status_label.setText("No folder selected")
            self.status_label.setStyleSheet("color: red;")

    def show_results(self, declarations):
        self.output_text.clear()

        if declarations:
            for dec in declarations:
                # Create formatted text
                self.output_text.setFontWeight(QFont.Weight.Bold)
                self.output_text.append(f"File: {dec['filename']}")
                
                # Reset font and set color for declaration
                self.output_text.setFontWeight(QFont.Weight.Normal)
                self.output_text.setTextColor(QColor("blue"))
                self.output_text.append(f"Declaration: {dec['declaration']}")
                
                # Reset text color
                self.output_text.setTextColor(QColor("black"))
                self.output_text.append(f"Index: {dec['index']}\n")
        else:
            self.output_text.setFontItalic(True)
            self.output_text.append("No valid class declarations found.")
            self.output_text.setFontItalic(False)

    def generate_report(self):
        if self.pdf_radio.isChecked():
            self.generate_pdf_report()
        else:
            self.generate_txt_report()

    def generate_txt_report(self):
        try:
            with open("class_declarations_report.txt", "w", encoding="utf-8") as f:
                for dec in self.declarations_found:
                    f.write(f"File: {dec['filename']}\n")
                    f.write(f"Declaration: {dec['declaration']}\n")
                    f.write(f"Index: {dec['index']}\n\n")
            
            self.status_label.setText("TXT report generated successfully.")
            self.status_label.setStyleSheet("color: green;")
            return "class_declarations_report.txt"
        except Exception as e:
            QMessageBox.critical(self.window, "Error", f"Error generating TXT report: {e}")
            return None

    def generate_pdf_report(self):
        try:
            pdf_path = "class_declarations_report.pdf"
            doc = SimpleDocTemplate(pdf_path, pagesize=letter)
            styles = getSampleStyleSheet()
            
            # Prepare report content
            content = []
            for dec in self.declarations_found:
                content.append(Paragraph(f"File: {dec['filename']}", styles['Heading3']))
                content.append(Paragraph(f"Declaration: {dec['declaration']}", styles['Normal']))
                content.append(Paragraph(f"Index: {dec['index']}", styles['Normal']))
                content.append(Paragraph("<br/>", styles['Normal']))
            
            # Build PDF
            doc.build(content)
            
            self.status_label.setText("PDF report generated successfully.")
            self.status_label.setStyleSheet("color: green;")
            return pdf_path
        except Exception as e:
            QMessageBox.critical(self.window, "Error", f"Error generating PDF report: {e}")
            return None

    def save_report(self):
        # Determine file extension based on selected report type
        file_type = "PDF Files (*.pdf);;Text Files (*.txt)" if self.pdf_radio.isChecked() else "Text Files (*.txt);;PDF Files (*.pdf)"
        
        # Open file dialog
        file_path, _ = QFileDialog.getSaveFileName(
            self.window, 
            "Save Report", 
            "", 
            file_type
        )

        if file_path:
            # Generate report based on selected type
            if self.pdf_radio.isChecked():
                generated_report = self.generate_pdf_report()
            else:
                generated_report = self.generate_txt_report()

            if generated_report:
                # Move/copy the generated report to the selected path
                import shutil
                shutil.move(generated_report, file_path)
                
                self.status_label.setText(f"Report saved to: {file_path}")
                self.status_label.setStyleSheet("color: green;")

    def run(self):
        self.window.show()
        sys.exit(self.app.exec())

def main():
    app = JavaClassRecognizer()
    app.run()

if __name__ == "__main__":
    main()