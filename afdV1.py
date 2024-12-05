import tkinter as tk
from tkinter import filedialog, messagebox
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import os
import re

class JavaClassAnalyzer:
    def __init__(self):
        self.state = 'q0'
        self.current_line = ''
        self.current_position = 0
        self.declarations = []
        
    def reset(self):
        self.state = 'q0'
        self.current_position = 0
        
    def transition(self, char):
        if self.state == 'q0':
            if char == 'p':
                self.state = 'q1'
            elif char == 'a':
                self.state = 'q7'
            elif char == 's':
                self.state = 'q20'
            elif char == 'c':
                self.state = 'q29'
            elif char == 'f':
                self.state = 'q15'
            else:
                self.state = 'q0'
                
        elif self.state == 'q1':
            if char == 'u':
                self.state = 'q2'
            else:
                self.state = 'q0'
                
        elif self.state == 'q2':
            if char == 'b':
                self.state = 'q3'
            else:
                self.state = 'q0'
                
        elif self.state == 'q3':
            if char == 'l':
                self.state = 'q4'
            else:
                self.state = 'q0'
                
        elif self.state == 'q4':
            if char == 'i':
                self.state = 'q5'
            else:
                self.state = 'q0'
                
        elif self.state == 'q5':
            if char == 'c':
                self.state = 'q6'
            else:
                self.state = 'q0'
                
        elif self.state == 'q6':
            if char in [' ', '\t', '\n']:
                self.state = 'q28'
            else:
                self.state = 'q0'
                
        elif self.state == 'q7':
            if char == 'b':
                self.state = 'q8'
            else:
                self.state = 'q0'
                
        elif self.state == 'q8':
            if char == 's':
                self.state = 'q9'
            else:
                self.state = 'q0'
                
        elif self.state == 'q9':
            if char == 't':
                self.state = 'q10'
            else:
                self.state = 'q0'
                
        elif self.state == 'q10':
            if char == 'r':
                self.state = 'q11'
            else:
                self.state = 'q0'
                
        elif self.state == 'q11':
            if char == 'a':
                self.state = 'q12'
            else:
                self.state = 'q0'
                
        elif self.state == 'q12':
            if char == 'c':
                self.state = 'q13'
            else:
                self.state = 'q0'
                
        elif self.state == 'q13':
            if char == 't':
                self.state = 'q14'
            else:
                self.state = 'q0'
                
        elif self.state == 'q14':
            if char in [' ', '\t', '\n']:
                self.state = 'q34'
            else:
                self.state = 'q0'
                
        elif self.state == 'q15':
            if char == 'i':
                self.state = 'q16'
            else:
                self.state = 'q0'
                
        elif self.state == 'q16':
            if char == 'n':
                self.state = 'q17'
            else:
                self.state = 'q0'
                
        elif self.state == 'q17':
            if char == 'a':
                self.state = 'q18'
            else:
                self.state = 'q0'
                
        elif self.state == 'q18':
            if char == 'l':
                self.state = 'q19'
            else:
                self.state = 'q0'
                
        elif self.state == 'q19':
            if char in [' ', '\t', '\n']:
                self.state = 'q34'
            else:
                self.state = 'q0'
                
        # Continuación de los estados para 'static'
        elif self.state == 'q20':
            if char == 't':
                self.state = 'q21'
            else:
                self.state = 'q0'
                
        elif self.state == 'q21':
            if char == 'r':
                self.state = 'q22'
            else:
                self.state = 'q0'
                
        elif self.state == 'q22':
            if char == 'i':
                self.state = 'q23'
            else:
                self.state = 'q0'
                
        elif self.state == 'q23':
            if char == 'c':
                self.state = 'q24'
            else:
                self.state = 'q0'
                
        elif self.state == 'q24':
            if char == 't':
                self.state = 'q25'
            else:
                self.state = 'q0'
                
        elif self.state == 'q25':
            if char == 'f':
                self.state = 'q26'
            else:
                self.state = 'q0'
                
        elif self.state == 'q26':
            if char == 'p':
                self.state = 'q27'
            else:
                self.state = 'q0'
                
        elif self.state == 'q27':
            if char in [' ', '\t', '\n']:
                self.state = 'q34'
            else:
                self.state = 'q0'
                
        elif self.state == 'q28':
            if char == 'a':
                self.state = 'q7'
            elif char == 'f':
                self.state = 'q15'
            elif char == 's':
                self.state = 'q20'
            elif char in [' ', '\t', '\n']:
                self.state = 'q28'
            else:
                self.state = 'q0'
                
        elif self.state == 'q29':
            if char == 'l':
                self.state = 'q30'
            else:
                self.state = 'q0'
                
        elif self.state == 'q30':
            if char == 'a':
                self.state = 'q31'
            else:
                self.state = 'q0'
                
        elif self.state == 'q31':
            if char == 's':
                self.state = 'q32'
            else:
                self.state = 'q0'
                
        elif self.state == 'q32':
            if char == 's':
                self.state = 'q33'
            else:
                self.state = 'q0'
                
        elif self.state == 'q33':
            if char in [' ', '\t', '\n']:
                self.state = 'q35'
            else:
                self.state = 'q0'
                
        elif self.state == 'q34':
            if char == 'c':
                self.state = 'q29'
            elif char in [' ', '\t', '\n']:
                self.state = 'q34'
            else:
                self.state = 'q0'
                
        elif self.state == 'q35':
            if char.isalpha() or char == '_' or char == '$':
                self.state = 'q36'
            elif char in [' ', '\t', '\n']:
                self.state = 'q35'
            else:
                self.state = 'q0'
                
        elif self.state == 'q36':
            if char.isalnum() or char == '_' or char == '$':
                self.state = 'q36'
            elif char in [' ', '\t', '\n']:
                self.state = 'q37'
            else:
                self.state = 'q0'
                
        elif self.state == 'q37':
            if char == 'i':
                self.state = 'q38'
            elif char == 'e':
                self.state = 'q48'
            elif char == '{':
                self.state = 'q56'
            elif char in [' ', '\t', '\n']:
                self.state = 'q37'
            else:
                self.state = 'q0'
        
        elif self.state == 'q38':
            if char == 'm':
                self.state = 'q39'
            else:
                self.state = 'q0'

        elif self.state == 'q39':
            if char == 'p':
                self.state = 'q40'
            else:
                self.state = 'q0'

        elif self.state == 'q40':
            if char == 'l':
                self.state = 'q41'
            else:
                self.state = 'q0'

        elif self.state == 'q41':
            if char == 'e':
                self.state = 'q42'
            else:
                self.state = 'q0'

        elif self.state == 'q42':
            if char == 'm':
                self.state = 'q43'
            else:
                self.state = 'q0'

        elif self.state == 'q43':
            if char == 'e':
                self.state = 'q44'
            else:
                self.state = 'q0'
        elif self.state == 'q44':
            if char == 'n':
                self.state = 'q45'
            else:
                self.state = 'q0'

        elif self.state == 'q45':
            if char == 't':
                self.state = 'q46'
            else:
                self.state = 'q0'
        elif self.state == 'q46':
            if char == 's':
                self.state = 'q47'
            else:
                self.state = 'q0'

        elif self.state == 'q47':
            if char in [' ', '\t', '\n']:
                self.state = 'q53'
            else:
                self.state = 'q0'

        elif self.state == 'q48':
            if char == 'x':
                self.state = 'q49'
            else:
                self.state = 'q0'

        elif self.state == 'q49':
            if char == 't':
                self.state = 'q50'
            else:
                self.state = 'q0'

        elif self.state == 'q50':
            if char == 'e':
                self.state = 'q51'
            else:
                self.state = 'q0'

        elif self.state == 'q51':
            if char == 'n':
                self.state = 'q52'
            else:
                self.state = 'q0'

        elif self.state == 'q52':
            if char == 'd':
                self.state = 'q46'
            else:
                self.state = 'q0'


        elif self.state == 'q53':
            if char == '{':
                self.state = 'q56'
            elif char.isalnum() or char == '_' or char == '$' or char == ',':  # Updated for variable names
                self.state = 'q54'
            elif char in [' ', '\t', '\n']:
                self.state = 'q53'  # Stay in q53 for whitespace
            else:
                self.state = 'q0'

        elif self.state == 'q54':
            if char == '{':
                self.state = 'q56'
            elif char.isalnum() or char == '_' or char == '$' or char == ',':
                self.state = 'q54' # Stay in q54 for variable names and more
            elif char in [' ', '\t', '\n']:  # Transition to q55 on whitespace
                self.state = 'q55'
            else:
                self.state = 'q0'

        elif self.state == 'q55':
            if char == 'i': # Transition to implements check
                self.state = 'q38'
            elif char in [' ', '\t', '\n']:
                self.state = 'q55'
            else:
                self.state = 'q0'

        elif self.state == 'q56':
            pass # Final State
                
        # ...
        
    def analyze_line(self, line, line_number, file_path):
        self.current_line = line.strip()
        self.current_position = 0
        
        while self.current_position < len(self.current_line):
            char = self.current_line[self.current_position]
            self.transition(char)
            self.current_position += 1
            
            if self.state == 'q56':  # Estado final
                class_name = re.search(r'class\s+(\w+)', self.current_line)
                if class_name:
                    self.declarations.append({
                        'declaration': self.current_line.strip(),
                        'line': line_number,
                        'file': file_path
                    })
                self.reset()
                break
                
        self.reset()

class Application:
    def __init__(self, root):
        self.root = root
        self.root.title("Java Class Analyzer")
        self.root.geometry("400x200")
        
        self.analyzer = JavaClassAnalyzer()
        
        # Buttons
        tk.Button(root, text="Select Folder", command=self.select_folder).pack(pady=10)
        tk.Button(root, text="Analyze", command=self.analyze_files).pack(pady=10)
        
        # Report type selection
        self.report_type = tk.StringVar(value="pdf")
        tk.Radiobutton(root, text="PDF", variable=self.report_type, value="pdf").pack()
        tk.Radiobutton(root, text="TXT", variable=self.report_type, value="txt").pack()
        
        self.folder_path = None
        
    def select_folder(self):
        self.folder_path = filedialog.askdirectory()
        if self.folder_path:
            messagebox.showinfo("Success", "Folder selected successfully!")
            
    def analyze_files(self):
        if not self.folder_path:
            messagebox.showerror("Error", "Please select a folder first!")
            return
            
        self.analyzer.declarations = []
        
        for root, dirs, files in os.walk(self.folder_path):
            for file in files:
                if file.endswith('.java'):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        for i, line in enumerate(f, 1):
                            self.analyzer.analyze_line(line, i, file_path)
                            
        if self.analyzer.declarations:
            self.generate_report()
        else:
            messagebox.showinfo("Result", "No class declarations found!")
            
    def generate_report(self):
        file_types = [('PDF files', '*.pdf')] if self.report_type.get() == 'pdf' else [('Text files', '*.txt')]
        save_path = filedialog.asksaveasfilename(defaultextension=file_types[0][1], filetypes=file_types)
        
        if not save_path:
            return
            
        if self.report_type.get() == 'pdf':
            self.generate_pdf_report(save_path)
        else:
            self.generate_txt_report(save_path)
            
    def generate_pdf_report(self, save_path):
        c = canvas.Canvas(save_path, pagesize=letter)
        y = 750  # Starting y position
        
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, y, "Java Class Declarations Report")
        y -= 30
        
        c.setFont("Helvetica", 12)
        for decl in self.analyzer.declarations:
            if y < 50:  # New page if not enough space
                c.showPage()
                y = 750
                c.setFont("Helvetica", 12)
                
            c.drawString(50, y, f"File: {decl['file']}")
            y -= 20
            c.drawString(50, y, f"Line {decl['line']}: {decl['declaration']}")
            y -= 30
            
        c.save()
        messagebox.showinfo("Success", "PDF report generated successfully!")
        
    def generate_txt_report(self, save_path):
        with open(save_path, 'w', encoding='utf-8') as f:
            f.write("Java Class Declarations Report\n")
            f.write("============================\n\n")
            
            for decl in self.analyzer.declarations:
                f.write(f"File: {decl['file']}\n")
                f.write(f"Line {decl['line']}: {decl['declaration']}\n")
                f.write("----------------------------\n\n")
                
        messagebox.showinfo("Success", "Text report generated successfully!")

if __name__ == '__main__':
    root = tk.Tk()
    app = Application(root)
    root.mainloop()