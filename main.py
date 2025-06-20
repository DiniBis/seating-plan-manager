import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import csv
import json
import os


class ClassroomSeatingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Plan de Classe - Gestionnaire de Places")
        self.root.geometry("1000x700")
        # Variables
        self.rows = 4
        self.cols = 6
        self.students = []
        self.seating_plan = {}  # {(row, col): student_name}
        self.selected_student = None
        self.setup_ui()
        self.draw_classroom()

    def setup_ui(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        # Configuration des poids pour le redimensionnement
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        # Frame de contrôles (en haut)
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        # Sélection du nombre de rangées
        ttk.Label(control_frame, text="Nombre de rangées:").grid(row=0, column=0, padx=(0, 5))
        self.rows_var = tk.StringVar(value="4")
        rows_combo = ttk.Combobox(control_frame, textvariable=self.rows_var, values=["4", "6"], width=5)
        rows_combo.grid(row=0, column=1, padx=(0, 20))
        rows_combo.bind('<<ComboboxSelected>>', self.on_rows_changed)
        # Boutons
        ttk.Button(control_frame, text="Charger CSV", command=self.load_csv).grid(row=0, column=2, padx=(0, 10))
        ttk.Button(control_frame, text="Sauvegarder", command=self.save_plan).grid(row=0, column=3, padx=(0, 10))
        ttk.Button(control_frame, text="Charger Plan", command=self.load_plan).grid(row=0, column=4, padx=(0, 10))
        ttk.Button(control_frame, text="Réinitialiser", command=self.reset_plan).grid(row=0, column=5)
        # Frame pour le plan de classe (à gauche)
        classroom_frame = ttk.LabelFrame(main_frame, text="Plan de Classe", padding="10")
        classroom_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        # Canvas pour dessiner le plan
        self.canvas = tk.Canvas(classroom_frame, width=500, height=400, bg="white", relief=tk.SUNKEN, bd=2)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind("<Button-1>", self.on_seat_click)
        self.canvas.bind("<Button-3>", self.on_seat_right_click)
        # Frame pour la liste des élèves (à droite)
        students_frame = ttk.LabelFrame(main_frame, text="Liste des Élèves", padding="10")
        students_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        students_frame.columnconfigure(0, weight=1)
        students_frame.rowconfigure(1, weight=1)
        # Listbox pour les élèves
        self.students_listbox = tk.Listbox(students_frame, height=25)
        self.students_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        self.students_listbox.bind('<<ListboxSelect>>', self.on_student_select)
        # Scrollbar pour la listbox
        scrollbar = ttk.Scrollbar(students_frame, orient=tk.VERTICAL, command=self.students_listbox.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S), pady=(0, 10))
        self.students_listbox.configure(yscrollcommand=scrollbar.set)
        # Label d'instructions
        instructions = ttk.Label(students_frame,
                                 text="Instructions:\n1. Chargez un fichier CSV avec les noms\n2. Sélectionnez un élève\n3. Clic gauche sur une place libre pour assigner\n4. Clic droit sur une place occupée pour libérer",
                                 justify=tk.LEFT, wraplength=200)
        instructions.grid(row=2, column=0, columnspan=2, pady=(10, 0), sticky=tk.W)

    def on_rows_changed(self, event=None):
        self.rows = int(self.rows_var.get())
        self.draw_classroom()

    def draw_classroom(self):
        self.canvas.delete("all")
        # Dimensions du canvas
        canvas_width = self.canvas.winfo_width() or 500
        canvas_height = self.canvas.winfo_height() or 400
        # Calcul des dimensions des places
        margin = 30
        seat_width = (canvas_width - 2 * margin - (self.cols - 1) * 10) // self.cols
        seat_height = (canvas_height - 2 * margin - (self.rows - 1) * 10) // self.rows
        # Dessiner le tableau (en haut)
        board_y = 10
        self.canvas.create_rectangle(margin, board_y, canvas_width - margin, board_y + 20,
                                     fill="darkgreen", outline="black", width=2)
        self.canvas.create_text(canvas_width // 2, board_y + 10, text="TABLEAU", fill="white",
                                font=("Arial", 10, "bold"))
        # Dessiner les places
        for row in range(self.rows):
            for col in range(self.cols):
                x1 = margin + col * (seat_width + 10)
                y1 = margin + 40 + row * (seat_height + 10)  # +40 pour le tableau
                x2 = x1 + seat_width
                y2 = y1 + seat_height
                # Couleur selon l'occupation
                student_name = self.seating_plan.get((row, col))
                if student_name:
                    fill_color = "lightblue"
                    text_color = "darkblue"
                else:
                    fill_color = "lightgray"
                    text_color = "gray"
                # Dessiner la place
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=fill_color, outline="black", width=1,
                                             tags=f"seat_{row}_{col}")
                # Ajouter le nom de l'élève ou le numéro de place
                center_x = (x1 + x2) // 2
                center_y = (y1 + y2) // 2
                if student_name:
                    # Afficher le nom (tronqué si nécessaire)
                    display_name = student_name if len(student_name) <= 12 else student_name[:10] + "..."
                    self.canvas.create_text(center_x, center_y, text=display_name, fill=text_color,
                                            font=("Arial", 8, "bold"))
                else:
                    self.canvas.create_text(center_x, center_y, text=f"R{row + 1}P{col + 1}", fill=text_color,
                                            font=("Arial", 7))

    def on_seat_click(self, event):
        if not self.selected_student:
            messagebox.showwarning("Aucun élève sélectionné", "Veuillez d'abord sélectionner un élève dans la liste.")
            return
        # Trouver la place cliquée
        clicked_item = self.canvas.find_closest(event.x, event.y)[0]
        tags = self.canvas.gettags(clicked_item)
        for tag in tags:
            if tag.startswith("seat_"):
                _, row_str, col_str = tag.split("_")
                row, col = int(row_str), int(col_str)
                # Vérifier si la place est libre
                if (row, col) in self.seating_plan:
                    messagebox.showwarning("Place occupée",
                                           f"Cette place est déjà occupée par {self.seating_plan[(row, col)]}")
                    return
                # Assigner l'élève à la place
                self.seating_plan[(row, col)] = self.selected_student
                # Retirer l'élève de la liste
                current_selection = self.students_listbox.curselection()
                if current_selection:
                    self.students_listbox.delete(current_selection[0])
                self.selected_student = None
                self.draw_classroom()
                break

    def on_seat_right_click(self, event):
        # Trouver la place cliquée
        clicked_item = self.canvas.find_closest(event.x, event.y)[0]
        tags = self.canvas.gettags(clicked_item)
        for tag in tags:
            if tag.startswith("seat_"):
                _, row_str, col_str = tag.split("_")
                row, col = int(row_str), int(col_str)
            # Vérifier si la place est occupée
            if (row, col) not in self.seating_plan:
                messagebox.showinfo("Place libre", "Cette place est déjà libre.")
                return
            # Retirer l'élève de la place
            student_name = self.seating_plan[(row, col)]
            del self.seating_plan[(row, col)]
            # Remettre l'élève dans la liste
            self.update_students_list()
            self.draw_classroom()
            messagebox.showinfo("Succès", f"{student_name} a été retiré de sa place.")
            break

    def on_student_select(self, event):
        selection = self.students_listbox.curselection()
        if selection:
            self.selected_student = self.students_listbox.get(selection[0])

    def load_csv(self):
        file_path = filedialog.askopenfilename(
            title="Sélectionner le fichier CSV",
            filetypes=[("Fichiers CSV", "*.csv"), ("Tous les fichiers", "*.*")]
        )
        if file_path:
            try:
                self.students = []
                with open(file_path, 'r', encoding='utf-8') as file:
                    csv_reader = csv.reader(file)
                    for row in csv_reader:
                        if row:  # Ignorer les lignes vides
                            # Prendre le premier élément de chaque ligne comme nom
                            name = row[0].strip()
                            if name:
                                self.students.append(name)
                self.update_students_list()
                messagebox.showinfo("Succès", f"{len(self.students)} élèves chargés avec succès!")
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors du chargement du fichier CSV:\n{str(e)}")

    def update_students_list(self):
        self.students_listbox.delete(0, tk.END)
        # Afficher seulement les élèves non assignés
        assigned_students = set(self.seating_plan.values())
        for student in self.students:
            if student not in assigned_students:
                self.students_listbox.insert(tk.END, student)

    def save_plan(self):
        if not self.seating_plan:
            messagebox.showwarning("Plan vide", "Aucun plan à sauvegarder.")
            return
        file_path = filedialog.asksaveasfilename(
            title="Sauvegarder le plan de classe",
            defaultextension=".json",
            filetypes=[("Fichiers JSON", "*.json"), ("Tous les fichiers", "*.*")]
        )
        if file_path:
            try:
                data = {
                    "rows": self.rows,
                    "cols": self.cols,
                    "seating_plan": {f"{r},{c}": student for (r, c), student in self.seating_plan.items()},
                    "all_students": self.students
                }
                with open(file_path, 'w', encoding='utf-8') as file:
                    json.dump(data, file, ensure_ascii=False, indent=2)
                messagebox.showinfo("Succès", "Plan de classe sauvegardé avec succès!")
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de la sauvegarde:\n{str(e)}")

    def load_plan(self):
        file_path = filedialog.askopenfilename(
            title="Charger un plan de classe",
            filetypes=[("Fichiers JSON", "*.json"), ("Tous les fichiers", "*.*")]
        )

        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                self.rows = data.get("rows", 4)
                self.cols = data.get("cols", 6)
                self.students = data.get("all_students", [])
                # Reconstituer le plan de places
                self.seating_plan = {}
                for pos_str, student in data.get("seating_plan", {}).items():
                    r, c = map(int, pos_str.split(","))
                    self.seating_plan[(r, c)] = student
                # Mettre à jour l'interface
                self.rows_var.set(str(self.rows))
                self.update_students_list()
                self.draw_classroom()
                messagebox.showinfo("Succès", "Plan de classe chargé avec succès!")
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors du chargement:\n{str(e)}")

    def reset_plan(self):
        if messagebox.askyesno("Confirmation", "Êtes-vous sûr de vouloir réinitialiser le plan de classe?"):
            self.seating_plan = {}
            self.selected_student = None
            self.update_students_list()
            self.draw_classroom()

def main():
    root = tk.Tk()
    app = ClassroomSeatingApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()