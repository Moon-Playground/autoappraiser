import customtkinter as ctk

class Mutations:
    def populate_mutations(self):
        # Sort lists alphabetically
        self.lists.sort()

        # Preserve current selection state if possible
        current_selection = set()
        if hasattr(self, 'checkbox_vars'):
            for desc, var in self.checkbox_vars.items():
                if var.get():
                    current_selection.add(desc)
        
        # Clear existing widgets
        for widget in self.mutation_frame.winfo_children():
            widget.destroy()
            
        self.checkbox_vars = {}
        columns = 3
        for i in range(columns):
            self.mutation_frame.grid_columnconfigure(i, weight=1)

        for i, desc in enumerate(self.lists):
            var = ctk.BooleanVar(value=desc in current_selection)
            cb = ctk.CTkCheckBox(self.mutation_frame, text=desc, variable=var)
            row = i // columns
            col = i % columns
            cb.grid(row=row, column=col, sticky="w", padx=10, pady=8)
            self.checkbox_vars[desc] = var

    def open_mutation_editor(self):
        top = ctk.CTkToplevel(self.root)
        top.title("Manage Mutations")
        top.geometry("400x500")
        top.attributes("-topmost", True)
        
        ctk.CTkLabel(top, text="Edit Mutations (One per line)", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)
        
        textbox = ctk.CTkTextbox(top, width=350, height=350)
        textbox.pack(pady=10, padx=10)
        
        # Fill textbox
        text_content = "\n".join(self.lists)
        textbox.insert("0.0", text_content)
        
        btn_frame = ctk.CTkFrame(top, fg_color="transparent")
        btn_frame.pack(fill="x", pady=10)
        
        ctk.CTkButton(btn_frame, text="Save", command=lambda: self.save_mutations_list(top, textbox)).pack(side="right", padx=20)
        ctk.CTkButton(btn_frame, text="Cancel", command=top.destroy, fg_color="transparent", border_width=1).pack(side="right", padx=10)

    def save_mutations_list(self, top, textbox):
        content = textbox.get("0.0", "end")
        new_lists = [line.strip() for line in content.splitlines() if line.strip()]
        
        # Update lists
        self.lists = new_lists
        
        # Save config
        self.save_config()
        
        # Refresh UI
        self.populate_mutations()
        
        top.destroy()

    def select_all_mutations(self):
        for var in self.checkbox_vars.values():
            var.set(True)

    def deselect_all_mutations(self):
        for var in self.checkbox_vars.values():
            var.set(False)

