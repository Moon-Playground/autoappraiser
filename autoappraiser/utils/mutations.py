import customtkinter as ctk
import urllib.request
import re
import threading

class Mutations:
    def _is_color_dark(self, hex_color):
        """Check if a hex color is dark based on perceived brightness."""
        if not isinstance(hex_color, str) or not hex_color.startswith("#"):
            return False
        try:
            hex_color = hex_color.lstrip('#')
            if len(hex_color) == 3:
                r, g, b = [int(hex_color[i]*2, 16) for i in range(3)]
            else:
                r, g, b = [int(hex_color[i:i+2], 16) for i in (0, 2, 4)]
            # Rec. 601 perceived brightness formula
            brightness = (r * 0.299 + g * 0.587 + b * 0.114)
            return brightness < 140 
        except:
            return False

    def populate_mutations(self):
        # Sort lists by name
        def get_name(item):
            if isinstance(item, dict):
                return list(item.keys())[0]
            return item

        self.lists.sort(key=get_name)

        # Preserve current selection state if possible
        current_selection = ""
        if hasattr(self, 'mutation_var'):
            current_selection = self.mutation_var.get()
        
        # Clear existing widgets
        for widget in self.mutation_frame.winfo_children():
            widget.destroy()
            
        self.mutation_var = ctk.StringVar(value=current_selection)
        columns = 3
        for i in range(columns):
            self.mutation_frame.grid_columnconfigure(i, weight=1)

        for i, item in enumerate(self.lists):
            if isinstance(item, dict):
                desc = list(item.keys())[0]
                color = item[desc]
            else:
                desc = item
                color = None

            # Handle special cases from colors.json (legacy/extended)
            if color in ["RAINBOW_SHADER", "PATTERN_VARIES", "INVERTED", "OPACITY_LOW"]:
                color = "#FFFFFF"

            is_dark = self._is_color_dark(color)
            
            # Create a card-like container for each mutation
            # If the text is dark, we use a LIGHT background to provide maximum contrast
            container = ctk.CTkFrame(
                self.mutation_frame, 
                fg_color="#eeeeee" if is_dark else "#2b2b2b",
                border_width=2 if is_dark else 1,
                border_color="white" if is_dark else "#333333",
                corner_radius=6
            )
            
            row = i // columns
            col = i % columns
            container.grid(row=row, column=col, sticky="nsew", padx=3, pady=3)
            container.grid_columnconfigure(0, weight=1)

            rb = ctk.CTkRadioButton(
                container, 
                text=desc, 
                variable=self.mutation_var, 
                value=desc,
                text_color=color if color else "white",
                font=ctk.CTkFont(size=12, weight="bold" if is_dark else "normal"),
                border_color="#999999" if is_dark else "#555555",
                hover_color="#cccccc" if is_dark else "#444444"
            )
            rb.pack(padx=8, pady=6, anchor="w")

    def fetch_wiki_mutations(self):
        """Replacement for editor: Fetch latest mutations from the wiki."""
        self.status_label.configure(text="Status: Syncing Wiki...", text_color="#3B8ED0")
        threading.Thread(target=self._perform_wiki_fetch, daemon=True).start()

    def _perform_wiki_fetch(self):
        try:
            url = "https://fischipedia.org/wiki/Mutations"
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
            req = urllib.request.Request(url, headers=headers)
            
            with urllib.request.urlopen(req, timeout=10) as response:
                html = response.read().decode('utf-8')

            # 1. Extract Colors from CSS
            color_pattern = r"\.mw-parser-output \.mutation-([a-z0-9_-]+(?:, \.mw-parser-output \.mutation-[a-z0-9_-]+)*)\s*{\s*--mutation-color:\s*(#[0-9a-fA-F]{6})"
            matches = re.finditer(color_pattern, html)
            
            wiki_colors = {}
            for match in matches:
                names_str = match.group(1)
                hex_color = match.group(2)
                for part in names_str.split(","):
                    name_key = part.strip().replace(".mw-parser-output .mutation-", "")
                    wiki_colors[name_key] = hex_color

            # 2. Extract Display Names and Appraisability from Table Rows
            # We look for rows that contain a mutation span and check for appraisability
            rows = re.findall(r"<tr>(.*?)</tr>", html, re.DOTALL)
            
            new_lists = []
            seen_names = set()
            
            HARDCODED_COLORS = {
                "Big": "#8bff89",
                "Giant": "#8bff89",
                "Shiny": "#fff0bc",
                "Sparkling": "#fff0bc"
            }
            
            # Use specific name pattern to find the mutation in each row
            name_pattern = r"class=\"mutation mutation-([a-z0-9_-]+)\"[^>]*>(?:<a[^>]*>)?([^<]+)(?:</a>)?</span>"
            
            for row in rows:
                name_match = re.search(name_pattern, row)
                if name_match:
                    key = name_match.group(1)
                    display_name = name_match.group(2).strip()
                    
                    # Core Logic: Keep if appraisable=true OR it's a mutation we want to hardcode
                    # Using regex to ensure we match the class attribute, not embedded CSS styles
                    is_appraisable = bool(re.search(r'class="[^"]*appraisable-true', row))
                    is_hardcoded = display_name in HARDCODED_COLORS
                    
                    if (is_appraisable or is_hardcoded) and display_name not in seen_names:
                        # Apply hardcoded colors for size/special muts, otherwise use wiki color
                        color = HARDCODED_COLORS.get(display_name, wiki_colors.get(key, "#FFFFFF"))
                        
                        new_lists.append({display_name: color})
                        seen_names.add(display_name)

            if not new_lists:
                raise Exception("No appraisable mutations found in wiki content")

            # Update and save
            self.lists = new_lists
            self.save_config()
            
            # Update GUI
            self.root.after(0, lambda: self.status_label.configure(text="Status: Inactive", text_color="#ff5555"))
            self.root.after(0, self.populate_mutations)
            
        except Exception as e:
            print(f"Wiki Fetch Error: {e}")
            self.root.after(0, lambda: self.status_label.configure(text=f"Status: Wiki Error", text_color="#ff5555"))

    def open_add_mutation_dialog(self):
        """Open a dialog to add a single mutation by name."""
        dialog = ctk.CTkInputDialog(text="Enter Mutation Name (e.g. Abyssal):", title="Add Mutation")
        name = dialog.get_input()
        
        if name and name.strip():
            name = name.strip()
            # Check if already in list
            exists = any(name.lower() == (list(m.keys())[0].lower() if isinstance(m, dict) else m.lower()) for m in self.lists)
            if exists:
                print(f"Mutation {name} already in list.")
                return
                
            self.status_label.configure(text=f"Status: Searching {name}...", text_color="#3B8ED0")
            threading.Thread(target=self._perform_single_mutation_add, args=(name,), daemon=True).start()

    def _perform_single_mutation_add(self, target_name):
        try:
            url = "https://fischipedia.org/wiki/Mutations"
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
            req = urllib.request.Request(url, headers=headers)
            
            with urllib.request.urlopen(req, timeout=10) as response:
                html = response.read().decode('utf-8')

            # Extract all available colors first
            color_pattern = r"\.mw-parser-output \.mutation-([a-z0-9_-]+(?:, \.mw-parser-output \.mutation-[a-z0-9_-]+)*)\s*{\s*--mutation-color:\s*(#[0-9a-fA-F]{6})"
            matches = re.finditer(color_pattern, html)
            wiki_colors = {}
            for match in matches:
                names_str = match.group(1)
                hex_color = match.group(2)
                for part in names_str.split(","):
                    name_key = part.strip().replace(".mw-parser-output .mutation-", "")
                    wiki_colors[name_key] = hex_color

            # Extract all names and keys (ignore appraisable status for manual add)
            name_pattern = r"class=\"mutation mutation-([a-z0-9_-]+)\"[^>]*>(?:<a[^>]*>)?([^<]+)(?:</a>)?</span>"
            name_matches = re.finditer(name_pattern, html)
            
            found_color = "#FFFFFF"
            official_name = target_name
            found = False
            
            for match in name_matches:
                key = match.group(1)
                display_name = match.group(2).strip()
                
                if display_name.lower() == target_name.lower():
                    found_color = wiki_colors.get(key, "#FFFFFF")
                    official_name = display_name
                    found = True
                    break
            
            # Special case for Big/Giant/Shiny/Sparkling if not found in table but requested
            if not found:
                lower_name = target_name.lower()
                if lower_name in ["big", "giant"]:
                    found_color = "#8bff89"
                    official_name = target_name.capitalize()
                    found = True
                elif lower_name in ["shiny", "sparkling"]:
                    found_color = "#fff0bc"
                    official_name = target_name.capitalize()
                    found = True

            # Even if not found on wiki, we add it with default white
            self.lists.append({official_name: found_color})
            self.save_config()
            
            self.root.after(0, lambda: self.status_label.configure(text="Status: Inactive", text_color="#ff5555"))
            self.root.after(0, self.populate_mutations)
            
            if not found:
                print(f"Warning: {target_name} not found on wiki. Added with default color.")

        except Exception as e:
            print(f"Add Mutation Error: {e}")
            self.root.after(0, lambda: self.status_label.configure(text=f"Status: Add Error", text_color="#ff5555"))

    def select_all_mutations(self):
        # For radio buttons, "select all" doesn't make sense. 
        if self.lists:
            self.mutation_var.set(self.lists[0])

    def deselect_all_mutations(self):
        self.mutation_var.set("")
