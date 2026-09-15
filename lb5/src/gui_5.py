import customtkinter as ctk
from tkinter import messagebox
from collections import deque
import tkinter as tk

class Node:
    def __init__(self):
        self.children = {}
        self.suffix_link = None
        self.output_link = None
        self.patterns = []
        self.depth = 0
        self.id = 0

class AhoCorasick:
    def __init__(self):
        self.root = Node()
        self.root.output_link = None
        self.patterns = []
        self.node_count = 1
        self.root.id = 0
        
    def add_pattern(self, pattern, pattern_num):
        node = self.root
        for char in pattern:
            if char not in node.children:
                new_node = Node()
                new_node.depth = node.depth + 1
                new_node.id = self.node_count
                self.node_count += 1
                node.children[char] = new_node
            node = node.children[char]
        node.patterns.append(pattern_num)
    
    def build_automaton(self):
        queue = deque()
        
        for char, child in self.root.children.items():
            child.suffix_link = self.root
            child.output_link = None
            queue.append(child)
        
        while queue:
            current = queue.popleft()
            
            for char, child in current.children.items():
                suffix_node = current.suffix_link
                while suffix_node != self.root and char not in suffix_node.children:
                    suffix_node = suffix_node.suffix_link
                
                if char in suffix_node.children:
                    child.suffix_link = suffix_node.children[char]
                else:
                    child.suffix_link = self.root
                
                if child.suffix_link.patterns:
                    child.output_link = child.suffix_link
                else:
                    child.output_link = child.suffix_link.output_link
                
                queue.append(child)
    
    def search_with_steps(self, text):
        """Поиск с пошаговой записью процесса"""
        results = []
        steps = []
        node = self.root
        
        for i, char in enumerate(text):
            step_info = {
                'position': i + 1,
                'char': char,
                'state_before': node.id,
                'transitions': [],
                'patterns_found': []
            }
            
            temp_node = node
            while temp_node != self.root and char not in temp_node.children:
                step_info['transitions'].append(
                    f"Состояние {temp_node.id} -> {temp_node.suffix_link.id} (суффиксная ссылка)"
                )
                temp_node = temp_node.suffix_link
            
            if char in temp_node.children:
                node = temp_node.children[char]
                step_info['transitions'].append(
                    f"Состояние {temp_node.id} -> {node.id} (по символу '{char}')"
                )
            else:
                node = self.root
                step_info['transitions'].append(
                    f"Состояние {temp_node.id} -> 0 (нет перехода, возврат в корень)"
                )
            
            temp = node
            while temp is not None and temp != self.root:
                for pattern_num in temp.patterns:
                    pattern_len = len(self.patterns[pattern_num - 1])
                    start_pos = i - pattern_len + 2
                    results.append((start_pos, pattern_num))
                    step_info['patterns_found'].append(
                        f"Найден паттерн #{pattern_num} ('{self.patterns[pattern_num-1]}') на позиции {start_pos}"
                    )
                temp = temp.output_link
            
            step_info['state_after'] = node.id
            steps.append(step_info)
        
        results.sort()
        return results, steps
    
    def get_automaton_description(self):
        """Возвращает текстовое описание автомата"""
        desc = []
        desc.append(f"Всего вершин в автомате: {self.node_count}")
        desc.append("\nОписание вершин:")
        
        queue = deque([self.root])
        visited = {self.root.id}
        
        while queue:
            node = queue.popleft()
            
            patterns_str = f", паттерны: {node.patterns}" if node.patterns else ""
            suffix_id = node.suffix_link.id if node.suffix_link else "None"
            output_id = node.output_link.id if node.output_link else "None"
            
            desc.append(f"Вершина {node.id} (глубина {node.depth}): "
                       f"суффиксная ссылка -> {suffix_id}, "
                       f"конечная ссылка -> {output_id}{patterns_str}")
            
            for char, child in node.children.items():
                if child.id not in visited:
                    visited.add(child.id)
                    queue.append(child)
        
        return "\n".join(desc)
    
    def get_transitions_description(self):
        """Возвращает описание переходов бора"""
        desc = []
        desc.append("\nПереходы бора:")
        
        queue = deque([self.root])
        visited = {self.root.id}
        
        while queue:
            node = queue.popleft()
            
            for char, child in node.children.items():
                desc.append(f"{node.id} --{char}--> {child.id}")
                if child.id not in visited:
                    visited.add(child.id)
                    queue.append(child)
        
        return "\n".join(desc)


class KmpApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Лабораторная работа 5: Ахо-Корасик и Поиск с джокером")
        self.geometry("1000x800")
        self.resizable(True, True)
        
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        self.tabview = ctk.CTkTabview(self, width=950, height=750)
        self.tabview.pack(padx=20, pady=20, expand=True, fill="both")
        
        self.tabview.add("Ахо-Корасик")
        self.tabview.add("Поиск с джокером")
        self.tabview.add("Визуализация автомата")
        
        self.setup_aho_corasick_tab()
        self.setup_wildcard_tab()
        self.setup_visualization_tab()
        
        self.automaton = None

    def setup_aho_corasick_tab(self):
        tab = self.tabview.tab("Ахо-Корасик")
        
        ctk.CTkLabel(tab, text="Поиск множества образцов (Ахо-Корасик)", 
                     font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(10, 10))
        
        frame_inputs = ctk.CTkFrame(tab)
        frame_inputs.pack(padx=20, pady=10, fill="x")
        
        ctk.CTkLabel(frame_inputs, text="Текст для поиска:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.entry_text = ctk.CTkEntry(frame_inputs, width=700, placeholder_text="Введите текст...")
        self.entry_text.grid(row=0, column=1, padx=10, pady=10)
        
        ctk.CTkLabel(frame_inputs, text="Образцы (через запятую):").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.entry_patterns = ctk.CTkEntry(frame_inputs, width=700, placeholder_text="Например: he,she,his,hers")
        self.entry_patterns.grid(row=1, column=1, padx=10, pady=10)
        
        btn_frame = ctk.CTkFrame(tab)
        btn_frame.pack(pady=10)
        
        self.btn_build = ctk.CTkButton(btn_frame, text="Построить автомат", 
                                       command=self.build_automaton_gui, width=150)
        self.btn_build.pack(side=ctk.LEFT, padx=10)
        
        self.btn_search = ctk.CTkButton(btn_frame, text="Найти вхождения", 
                                        command=self.search_patterns, width=150)
        self.btn_search.pack(side=ctk.LEFT, padx=10)
        
        ctk.CTkLabel(tab, text="Промежуточные данные:", 
                     font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(10, 5))
        
        self.text_intermediate = ctk.CTkTextbox(tab, width=900, height=400)
        self.text_intermediate.pack(padx=20, pady=10, fill="both", expand=True)
        
        self.label_result = ctk.CTkLabel(tab, text="Результат: -", font=ctk.CTkFont(size=14))
        self.label_result.pack(pady=10)

    def setup_wildcard_tab(self):
        """Настройка вкладки поиска с джокером"""
        tab = self.tabview.tab("Поиск с джокером")
        
        ctk.CTkLabel(tab, text="Поиск образца с джокером", 
                     font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(10, 10))
        
        frame_inputs = ctk.CTkFrame(tab)
        frame_inputs.pack(padx=20, pady=10, fill="x")
        
        ctk.CTkLabel(frame_inputs, text="Текст:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.entry_wildcard_text = ctk.CTkEntry(frame_inputs, width=700, placeholder_text="Введите текст...")
        self.entry_wildcard_text.grid(row=0, column=1, padx=10, pady=10)
        
        ctk.CTkLabel(frame_inputs, text="Шаблон с джокером:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.entry_wildcard_pattern = ctk.CTkEntry(frame_inputs, width=700, placeholder_text="Например: ab??c?")
        self.entry_wildcard_pattern.grid(row=1, column=1, padx=10, pady=10)
        
        ctk.CTkLabel(frame_inputs, text="Символ джокера:").grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.entry_wildcard_char = ctk.CTkEntry(frame_inputs, width=700, placeholder_text="Например: ? или $")
        self.entry_wildcard_char.grid(row=2, column=1, padx=10, pady=10)
        
        self.btn_wildcard_search = ctk.CTkButton(tab, text="Найти вхождения", 
                                                 command=self.search_with_wildcard, width=150)
        self.btn_wildcard_search.pack(pady=20)
        
        ctk.CTkLabel(tab, text="Промежуточные данные (пошаговое сравнение):", 
                     font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(10, 5))
        
        self.text_wildcard_intermediate = ctk.CTkTextbox(tab, width=900, height=400)
        self.text_wildcard_intermediate.pack(padx=20, pady=10, fill="both", expand=True)
        
        self.label_wildcard_result = ctk.CTkLabel(tab, text="Результат: -", font=ctk.CTkFont(size=14))
        self.label_wildcard_result.pack(pady=10)

    def setup_visualization_tab(self):
        tab = self.tabview.tab("Визуализация автомата")
        
        ctk.CTkLabel(tab, text="Графическое представление автомата (Вариант 7)", 
                     font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(10, 10))
        
        self.canvas_frame = ctk.CTkFrame(tab)
        self.canvas_frame.pack(padx=20, pady=10, fill="both", expand=True)
        
        self.canvas = tk.Canvas(self.canvas_frame, bg="white", width=900, height=600)
        self.canvas.pack(fill="both", expand=True)
        
        btn_frame = ctk.CTkFrame(tab)
        btn_frame.pack(pady=10)
        
        ctk.CTkButton(btn_frame, text="Обновить визуализацию", 
                     command=self.draw_automaton).pack(side=ctk.LEFT, padx=10)

    def build_automaton_gui(self):
        text = self.entry_text.get().strip()
        patterns_str = self.entry_patterns.get().strip()
        
        if not text or not patterns_str:
            messagebox.showwarning("Предупреждение", "Введите текст и образцы!")
            return
        
        patterns = [p.strip() for p in patterns_str.split(',') if p.strip()]
        
        if not patterns:
            messagebox.showwarning("Предупреждение", "Введите хотя бы один образец!")
            return
        
        self.automaton = AhoCorasick()
        self.automaton.patterns = patterns
        
        for i, pattern in enumerate(patterns, 1):
            self.automaton.add_pattern(pattern, i)
        
        self.automaton.build_automaton()
        
        self.text_intermediate.delete("1.0", "end")
        
        intermediate_text = "ПОСТРОЕНИЕ БОРА:\n"
        intermediate_text += "=" * 60 + "\n\n"
        
        for i, pattern in enumerate(patterns, 1):
            intermediate_text += f"Добавлен паттерн {i}: '{pattern}'\n"
        
        intermediate_text += f"\nВсего вершин в боре: {self.automaton.node_count}\n"
        intermediate_text += self.automaton.get_automaton_description()
        intermediate_text += "\n" + self.automaton.get_transitions_description()
        
        self.text_intermediate.insert("1.0", intermediate_text)
        self.label_result.configure(text=f"Автомат построен! Вершин: {self.automaton.node_count}", 
                                   text_color="green")

    def search_patterns(self):
        if not self.automaton:
            messagebox.showwarning("Предупреждение", "Сначала постройте автомат!")
            return
        
        results, steps = self.automaton.search_with_steps(self.entry_text.get())
        
        self.text_intermediate.insert("end", "\n\n" + "=" * 60 + "\n")
        self.text_intermediate.insert("end", "ПРОЦЕСС ПОИСКА (ПОШАГОВО):\n")
        self.text_intermediate.insert("end", "=" * 60 + "\n\n")
        
        for step in steps:
            self.text_intermediate.insert("end", f"Позиция {step['position']}: символ '{step['char']}'\n")
            self.text_intermediate.insert("end", f"  Состояние до: {step['state_before']}\n")
            
            if step['transitions']:
                self.text_intermediate.insert("end", "  Переходы:\n")
                for trans in step['transitions']:
                    self.text_intermediate.insert("end", f"    - {trans}\n")
            
            self.text_intermediate.insert("end", f"  Состояние после: {step['state_after']}\n")
            
            if step['patterns_found']:
                self.text_intermediate.insert("end", "  Найденные паттерны:\n")
                for pat in step['patterns_found']:
                    self.text_intermediate.insert("end", f"    * {pat}\n")
            
            self.text_intermediate.insert("end", "\n")
        
        if results:
            results_text = "\nИТОГОВЫЕ РЕЗУЛЬТАТЫ:\n" + "-" * 60 + "\n"
            for pos, num in results:
                results_text += f"Позиция {pos}: паттерн #{num} ('{self.automaton.patterns[num-1]}')\n"
            self.text_intermediate.insert("end", results_text)
            
            self.label_result.configure(text=f"Найдено вхождений: {len(results)}", text_color="green")
        else:
            self.text_intermediate.insert("end", "Вхождений не найдено")
            self.label_result.configure(text="Результат: -1 (вхождений не найдено)", text_color="red")

    def search_with_wildcard(self):
        """Поиск с джокером с подробным выводом"""
        text = self.entry_wildcard_text.get().strip()
        pattern = self.entry_wildcard_pattern.get().strip()
        wildcard = self.entry_wildcard_char.get().strip()
        
        if not text or not pattern or not wildcard:
            messagebox.showwarning("Предупреждение", "Заполните все поля!")
            return
        
        if len(wildcard) != 1:
            messagebox.showwarning("Предупреждение", "Символ джокера должен быть одним символом!")
            return
        
        n = len(text)
        m = len(pattern)
        
        self.text_wildcard_intermediate.delete("1.0", "end")
        
        intermediate_text = "=" * 60 + "\n"
        intermediate_text += "ПОИСК С ДЖОКЕРОМ\n"
        intermediate_text += "=" * 60 + "\n\n"
        intermediate_text += f"Текст: {text}\n"
        intermediate_text += f"Шаблон: {pattern}\n"
        intermediate_text += f"Символ джокера: '{wildcard}'\n"
        intermediate_text += f"Длина текста: {n}, длина шаблона: {m}\n\n"
        
        results = []
        
        for i in range(n - m + 1):
            intermediate_text += f"Проверка позиции {i + 1}:\n"
            intermediate_text += f"  Подстрока текста: {text[i:i+m]}\n"
            intermediate_text += f"  Сравнение с шаблоном: {pattern}\n"
            intermediate_text += f"  Сравнение посимвольное:\n"
            
            match = True
            comparisons = []
            
            for j in range(m):
                text_char = text[i + j]
                pattern_char = pattern[j]
                
                if pattern_char == wildcard:
                    comparisons.append(f"{text_char}={pattern_char}(джокер)")
                elif pattern_char == text_char:
                    comparisons.append(f"{text_char}={pattern_char}✓")
                else:
                    comparisons.append(f"{text_char}≠{pattern_char}")
                    match = False
                    break
            
            intermediate_text += f"    {' '.join(comparisons)}\n"
            
            if match:
                results.append(i + 1)
                intermediate_text += f"  → СОВПАДЕНИЕ!\n\n"
            else:
                intermediate_text += f"  → нет совпадения\n\n"
        
        intermediate_text += "=" * 60 + "\n"
        intermediate_text += f"ИТОГО: найдено {len(results)} вхождений\n"
        
        if results:
            intermediate_text += f"Позиции: {', '.join(map(str, results))}\n"
            self.label_wildcard_result.configure(text=f"Найдено вхождений: {len(results)}", text_color="green")
        else:
            intermediate_text += "-1 (вхождений не найдено)\n"
            self.label_wildcard_result.configure(text="Результат: -1 (вхождений не найдено)", text_color="red")
        
        self.text_wildcard_intermediate.insert("1.0", intermediate_text)

    def draw_automaton(self):
        if not self.automaton:
            messagebox.showwarning("Предупреждение", "Сначала постройте автомат!")
            return
        
        self.canvas.delete("all")
        
        node_radius = 25
        x_start = 80
        y_start = 60
        x_step = 140
        y_step = 120
        
        levels = {}
        queue = deque([(self.automaton.root, 0)])
        visited = set()
        
        while queue:
            node, x_pos = queue.popleft()
            if node.id in visited:
                continue
            visited.add(node.id)
            
            depth = node.depth
            if depth not in levels:
                levels[depth] = []
            levels[depth].append((node, x_pos))
            
            for char, child in node.children.items():
                if child.id not in visited:
                    queue.append((child, x_pos + x_step))
        
        node_positions = {}
        
        for depth in sorted(levels.keys()):
            nodes_at_level = levels[depth]
            y_pos = y_start + depth * y_step
            
            for i, (node, x_pos) in enumerate(nodes_at_level):
                x_center = x_start + x_pos
                y_center = y_pos
                
                node_positions[node.id] = (x_center, y_center)
                
                fill_color = "lightblue" if node.patterns else "white"
                outline_color = "red" if node.patterns else "black"
                outline_width = 3 if node.patterns else 2
                
                self.canvas.create_oval(
                    x_center - node_radius, y_center - node_radius,
                    x_center + node_radius, y_center + node_radius,
                    fill=fill_color, outline=outline_color, width=outline_width
                )
                
                self.canvas.create_text(
                    x_center, y_center - 8,
                    text=str(node.id), font=("Arial", 12, "bold")
                )
                
                if node.patterns:
                    patterns_text = f"P{node.patterns}"
                    self.canvas.create_text(
                        x_center, y_center + 10,
                        text=patterns_text, font=("Arial", 9), fill="red"
                    )
        
        visited_edges = set()
        queue = deque([self.automaton.root])
        visited_nodes = {self.automaton.root.id}
        
        while queue:
            node = queue.popleft()
            
            if node.id in node_positions:
                x1, y1 = node_positions[node.id]
                
                for char, child in node.children.items():
                    if child.id in node_positions:
                        x2, y2 = node_positions[child.id]
                        
                        self.canvas.create_line(
                            x1, y1, x2, y2,
                            arrow=tk.LAST, fill="black", width=2
                        )
                        
                        mid_x = (x1 + x2) / 2
                        mid_y = (y1 + y2) / 2
                        self.canvas.create_text(
                            mid_x, mid_y - 12,
                            text=char, font=("Arial", 10, "bold"), fill="blue"
                        )
                    
                    if child.id not in visited_nodes:
                        visited_nodes.add(child.id)
                        queue.append(child)
        
        queue = deque([self.automaton.root])
        visited_nodes = {self.automaton.root.id}
        
        while queue:
            node = queue.popleft()
            
            if node.suffix_link and node.id != node.suffix_link.id:
                if node.id in node_positions and node.suffix_link.id in node_positions:
                    x1, y1 = node_positions[node.id]
                    x2, y2 = node_positions[node.suffix_link.id]
                    
                    self.canvas.create_line(
                        x1, y1, x2, y2,
                        dash=(5, 3), fill="red", width=2
                    )
            
            for child in node.children.values():
                if child.id not in visited_nodes:
                    visited_nodes.add(child.id)
                    queue.append(child)
        
        legend_y = 650
        self.canvas.create_text(80, legend_y, text="Легенда:", font=("Arial", 14, "bold"), anchor="w")
        
        self.canvas.create_oval(80, legend_y + 15, 105, legend_y + 40, fill="lightblue", outline="red", width=2)
        self.canvas.create_text(250, legend_y + 27, text="- вершина с паттерном", anchor="w", font=("Arial", 11))
        
        self.canvas.create_line(80, legend_y + 55, 105, legend_y + 55, fill="black", width=2, arrow=tk.LAST)
        self.canvas.create_text(250, legend_y + 55, text="- переход бора", anchor="w", font=("Arial", 11))
        
        self.canvas.create_line(80, legend_y + 80, 105, legend_y + 80, dash=(5, 3), fill="red", width=2)
        self.canvas.create_text(250, legend_y + 80, text="- суффиксная ссылка", anchor="w", font=("Arial", 11))


if __name__ == "__main__":
    app = KmpApp()
    app.mainloop()