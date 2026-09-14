import customtkinter as ctk
from tkinter import messagebox
from importlib.machinery import SourceFileLoader

loader_11 = SourceFileLoader("task_11", "d:\\developper\\CC++\\stepic\\piaa\\4_1_1.py")
task_11 = loader_11.load_module()

loader_12 = SourceFileLoader("task_12", "d:\\developper\\CC++\\stepic\\piaa\\4_1_2.py")
task_12 = loader_12.load_module()

loader_2 = SourceFileLoader("task_2", "d:\\developper\\CC++\\stepic\\piaa\\4_2.py")
task_2 = loader_2.load_module()


class EditDistanceApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Редакционное расстояние — Вариант 5а")
        self.geometry("900x750")
        self.minsize(800, 650)
        
        ctk.set_appearance_mode("dark") 
        ctk.set_default_color_theme("blue")
        
        # Состояние пошагового режима для каждой вкладки
        self.step_state = {
            "411": {"dp_table": None, "str_a": "", "str_b": "", "costs": None, "i": 0, "j": 0},
            "412": {"dp_table": None, "str_a": "", "str_b": "", "costs": None, "i": 0, "j": 0},
            "42":  {"prev_row": None, "curr_row": None, "str_a": "", "str_b": "", "i": 0, "j": 0}
        }
        
        self._build_ui()
    
    def _build_ui(self):
        top = ctk.CTkFrame(self, fg_color="transparent")
        top.pack(fill="x", padx=20, pady=(15, 5))
        
        ctk.CTkLabel(
            top, text="Редакционное расстояние",
            font=ctk.CTkFont(size=24, weight="bold")
        ).pack() 
        
        self.tabs = ctk.CTkTabview(self)
        self.tabs.pack(fill="both", expand=True, padx=20, pady=10)
        
        self._build_tab_411()
        self._build_tab_412()
        self._build_tab_42()
    
    # Построение вкладок
    def _build_tab_411(self):
        tab = self.tabs.add("4.1.1 Стоимость")
        self._add_string_inputs(tab, prefix="411")
        self._add_costs_inputs(tab, prefix="411")
        
        btns = ctk.CTkFrame(tab, fg_color="transparent")
        btns.pack(fill="x", pady=10)
        ctk.CTkButton(btns, text="Вычислить", width=120,
                     command=self._calc_411).pack(side="left", padx=5)
        ctk.CTkButton(btns, text="Пошагово", width=120, fg_color="#e67e22",
                     command=self._start_step_411).pack(side="left", padx=5)
        ctk.CTkButton(btns, text="Пример", width=100, fg_color="gray",
                     command=lambda: self._fill_example("411")).pack(side="left", padx=5)
        
        # Панель управления шагами
        self.step_ctrl_411 = ctk.CTkFrame(tab, fg_color="transparent")
        self.step_ctrl_411.pack(fill="x", pady=5)
        
        self.btn_step_411 = ctk.CTkButton(self.step_ctrl_411, text="Следующий шаг", width=150,
                                          command=lambda: self._do_step("411"))
        self.btn_step_411.pack(side="left", padx=5)
        
        self.btn_reset_411 = ctk.CTkButton(self.step_ctrl_411, text="Сброс", width=100,
                                           command=lambda: self._reset_step("411"))
        self.btn_reset_411.pack(side="left", padx=5)
        
        self.step_info_411 = ctk.CTkLabel(self.step_ctrl_411, text="", text_color="gray")
        self.step_info_411.pack(side="left", padx=15)
        
        self.result_411 = ctk.CTkLabel(tab, text="", font=ctk.CTkFont(size=18, weight="bold"))
        self.result_411.pack(pady=5)
        
        self._add_dp_table(tab, "411")
    
    def _build_tab_412(self):
        tab = self.tabs.add("4.1.2 Операции")
        self._add_string_inputs(tab, prefix="412")
        self._add_costs_inputs(tab, prefix="412")
        
        # Кнопки
        btns = ctk.CTkFrame(tab, fg_color="transparent")
        btns.pack(fill="x", pady=5)  # было 10
        ctk.CTkButton(btns, text="Вычислить", width=120,
                    command=self._calc_412).pack(side="left", padx=5)
        ctk.CTkButton(btns, text="Пошагово", width=120, fg_color="#e67e22",
                    command=self._start_step_412).pack(side="left", padx=5)
        ctk.CTkButton(btns, text="Пример", width=100, fg_color="gray",
                    command=lambda: self._fill_example("412")).pack(side="left", padx=5)
        
        # Панель управления шагами
        self.step_ctrl_412 = ctk.CTkFrame(tab, fg_color="transparent")
        self.step_ctrl_412.pack(fill="x", pady=2)  # было 5
        
        self.btn_step_412 = ctk.CTkButton(self.step_ctrl_412, text="Следующий шаг", width=150,
                                        command=lambda: self._do_step("412"))
        self.btn_step_412.pack(side="left", padx=5)
        
        self.btn_reset_412 = ctk.CTkButton(self.step_ctrl_412, text="Сброс", width=100,
                                        command=lambda: self._reset_step("412"))
        self.btn_reset_412.pack(side="left", padx=5)
        
        self.step_info_412 = ctk.CTkLabel(self.step_ctrl_412, text="", text_color="gray")
        self.step_info_412.pack(side="left", padx=15)
        
        # Результат
        self.result_412 = ctk.CTkLabel(tab, text="", font=ctk.CTkFont(size=16, weight="bold"))
        self.result_412.pack(pady=2)  # было 5
        
        self._add_dp_table(tab, "412")
        
        # Операции и легенда
        self.ops_412 = ctk.CTkFrame(tab, fg_color="transparent")
        self.ops_412.pack(pady=2)  # было 5
        
        legend = ctk.CTkFrame(tab, fg_color="transparent")
        legend.pack(pady=2)  # было 5
        for op, color, desc in [
            ("M", "#2ecc71", "Match"), ("R", "#f1c40f", "Replace"),
            ("I", "#3498db", "Insert"), ("D", "#e74c3c", "Delete")
        ]:
            ctk.CTkLabel(legend, text=f" {op} ", fg_color=color,
                        corner_radius=4, width=25).pack(side="left", padx=2)
            ctk.CTkLabel(legend, text=f"= {desc}  ").pack(side="left")

    def _build_tab_42(self):
        tab = self.tabs.add("4.2 Левенштейн")
        self._add_string_inputs(tab, prefix="42")
        
        info = ctk.CTkLabel(tab, 
            text="Все операции имеют стоимость 1. Память: O(min(n,m))",
            text_color="gray", font=ctk.CTkFont(size=12))
        info.pack(pady=5)
        
        btns = ctk.CTkFrame(tab, fg_color="transparent")
        btns.pack(fill="x", pady=10)
        ctk.CTkButton(btns, text="Вычислить", width=120,
                     command=self._calc_42).pack(side="left", padx=5)
        ctk.CTkButton(btns, text="Пошагово", width=120, fg_color="#e67e22",
                     command=self._start_step_42).pack(side="left", padx=5)
        ctk.CTkButton(btns, text="Пример", width=100, fg_color="gray",
                     command=lambda: self._fill_example("42")).pack(side="left", padx=5)
        
        self.step_ctrl_42 = ctk.CTkFrame(tab, fg_color="transparent")
        self.step_ctrl_42.pack(fill="x", pady=5)
        
        self.btn_step_42 = ctk.CTkButton(self.step_ctrl_42, text="Следующий шаг", width=150,
                                         command=lambda: self._do_step("42"))
        self.btn_step_42.pack(side="left", padx=5)
        
        self.btn_reset_42 = ctk.CTkButton(self.step_ctrl_42, text="Сброс", width=100,
                                          command=lambda: self._reset_step("42"))
        self.btn_reset_42.pack(side="left", padx=5)
        
        self.step_info_42 = ctk.CTkLabel(self.step_ctrl_42, text="", text_color="gray")
        self.step_info_42.pack(side="left", padx=15)
        
        self.result_42 = ctk.CTkLabel(tab, text="", font=ctk.CTkFont(size=18, weight="bold"))
        self.result_42.pack(pady=5)
        
        self._add_dp_table(tab, "42")
    
    # Вспомогательные методы построения
    def _add_string_inputs(self, parent, prefix):
        frame = ctk.CTkFrame(parent)
        frame.pack(fill="x", pady=10, padx=10)
        
        for label, key_suffix in [("Строка A:", "a"), ("Строка B:", "b")]:
            row = ctk.CTkFrame(frame, fg_color="transparent")
            row.pack(fill="x", pady=5, padx=10)
            ctk.CTkLabel(row, text=label, width=80, anchor="w").pack(side="left")
            entry = ctk.CTkEntry(row, width=400)
            entry.pack(side="left", fill="x", expand=True)
            setattr(self, f"entry_{key_suffix}_{prefix}", entry)
    
    def _add_costs_inputs(self, parent, prefix):
        frame = ctk.CTkFrame(parent)
        frame.pack(fill="x", pady=10)
        ctk.CTkLabel(frame, text="Стоимости операций:", 
                    font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=10, pady=(8, 4))
        
        inner = ctk.CTkFrame(frame, fg_color="transparent")
        inner.pack(fill="x", padx=10, pady=(0, 8))
        
        cost_dict = {}
        for i, (name, default) in enumerate([
            ("Replace", 1), ("Insert", 1), ("Delete", 1), ("Delete×2", 2)
        ]):
            ctk.CTkLabel(inner, text=f"{name}:").grid(row=0, column=i*2, padx=5)
            entry = ctk.CTkEntry(inner, width=60)
            entry.insert(0, str(default))
            entry.grid(row=0, column=i*2+1, padx=5)
            cost_dict[name] = entry
        setattr(self, f"cost_{prefix}", cost_dict)
    
    def _add_dp_table(self, parent, prefix):
        ctk.CTkLabel(parent, text="Таблица динамического программирования:",
                    font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=10, pady=(5, 2))  # было (10, 5)
        
        scroll = ctk.CTkScrollableFrame(parent, height=200)  # можно уменьшить до 150
        scroll.pack(fill="both", expand=False, padx=10, pady=(0, 5))  # expand=False важно!
        setattr(self, f"dp_frame_{prefix}", scroll)
        setattr(self, f"dp_cells_{prefix}", [])

    def _fill_example(self, prefix):
        examples = {
            "411": ("entrance", "reenterable", ["1", "1", "1", "2"]),
            "412": ("abc", "ac", ["1", "1", "1", "1"]),
            "42": ("kitten", "sitting", None),
        }
        a, b, costs = examples[prefix]
        getattr(self, f"entry_a_{prefix}").delete(0, "end")
        getattr(self, f"entry_a_{prefix}").insert(0, a)
        getattr(self, f"entry_b_{prefix}").delete(0, "end")
        getattr(self, f"entry_b_{prefix}").insert(0, b)
        
        if costs and prefix != "42":
            cost_dict = getattr(self, f"cost_{prefix}")
            for (name, _), val in zip(
                [("Replace", 1), ("Insert", 1), ("Delete", 1), ("Delete×2", 2)], costs
            ):
                cost_dict[name].delete(0, "end")
                cost_dict[name].insert(0, val)
    
    # Мгновенное вычисление
    def _calc_411(self):
        try:
            str_a, str_b, costs = self._get_inputs_41x("411")
            dp_table = task_11.create_dp_table(
                len(str_a), len(str_b), str_a, str_b, *costs
            )
            result = dp_table[len(str_a)][len(str_b)]
            self.result_411.configure(text=f"Минимальная стоимость: {result}",
                                     text_color="#2ecc71")
            self._render_dp_table("411", dp_table, str_a, str_b)
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректные числа")
    
    def _calc_412(self):
        try:
            str_a, str_b, costs = self._get_inputs_41x("412")
            operations, total = task_12.edit_distance_with_operations(costs, str_a, str_b)
            self.result_412.configure(
                text=f"Стоимость: {total}   |   Операций: {len(operations)}",
                text_color="#2ecc71"
            )
            self._render_operations(operations)
            dp_table = task_12.edit_distance_with_operations.__code__
            n_val, m_val = len(str_a), len(str_b)
            dp_table = task_11.create_dp_table(n_val, m_val, str_a, str_b, *costs)
            self._render_dp_table("412", dp_table, str_a, str_b)
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректные числа")
    
    def _calc_42(self):
        str_a = self.entry_a_42.get()
        str_b = self.entry_b_42.get()
        if not str_a and not str_b:
            messagebox.showerror("Ошибка", "Введите обе строки")
            return
        result = task_2.levenshtein_distance(str_a, str_b)
        self.result_42.configure(text=f"Расстояние Левенштейна: {result}",
                                text_color="#2ecc71")
    
    def _get_inputs_41x(self, prefix):
        str_a = getattr(self, f"entry_a_{prefix}").get()
        str_b = getattr(self, f"entry_b_{prefix}").get()
        cost_dict = getattr(self, f"cost_{prefix}")
        costs = [int(cost_dict[n].get()) for n in 
                ["Replace", "Insert", "Delete", "Delete×2"]]
        return str_a, str_b, costs
    
    # Запуск пошагового режима
    def _start_step_411(self):
        try:
            str_a, str_b, costs = self._get_inputs_41x("411")
            n_val, m_val = len(str_a), len(str_b)
            
            # Создаём пустую таблицу с инициализацией
            dp_table = [[0] * (m_val + 1) for _ in range(n_val + 1)]
            for j in range(1, m_val + 1):
                dp_table[0][j] = dp_table[0][j-1] + costs[1]
            for i in range(1, n_val + 1):
                dp_table[i][0] = dp_table[i-1][0] + costs[2]
            
            state = self.step_state["411"]
            state["dp_table"] = dp_table
            state["str_a"] = str_a
            state["str_b"] = str_b
            state["costs"] = costs
            state["i"] = 1
            state["j"] = 1
            
            self._render_dp_table("411", dp_table, str_a, str_b, highlight=(1, 1))
            self.step_info_411.configure(text=f"Шаг: ячейка [1, 1] ({str_a[0] if str_a else ''} → {str_b[0] if str_b else ''})")
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректные числа")
    
    def _start_step_412(self):
        try:
            str_a, str_b, costs = self._get_inputs_41x("412")
            n_val, m_val = len(str_a), len(str_b)
            
            dp_table = [[0] * (m_val + 1) for _ in range(n_val + 1)]
            for j in range(1, m_val + 1):
                dp_table[0][j] = dp_table[0][j-1] + costs[1]
            for i in range(1, n_val + 1):
                dp_table[i][0] = dp_table[i-1][0] + costs[2]
            
            state = self.step_state["412"]
            state["dp_table"] = dp_table
            state["str_a"] = str_a
            state["str_b"] = str_b
            state["costs"] = costs
            state["i"] = 1
            state["j"] = 1
            
            self._render_dp_table("412", dp_table, str_a, str_b, highlight=(1, 1))
            self.step_info_412.configure(text=f"Шаг: ячейка [1, 1]")
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректные числа")
    
    def _start_step_42(self):
        str_a = self.entry_a_42.get()
        str_b = self.entry_b_42.get()
        if not str_a or not str_b:
            messagebox.showerror("Ошибка", "Введите обе строки")
            return
        
        n, m = len(str_a), len(str_b)
        if n < m:
            str_a, str_b = str_b, str_a
            n, m = m, n
        
        prev_row = list(range(m + 1))
        curr_row = [0] * (m + 1)
        
        state = self.step_state["42"]
        state["prev_row"] = prev_row
        state["curr_row"] = curr_row
        state["str_a"] = str_a
        state["str_b"] = str_b
        state["i"] = 1
        state["j"] = 0
        
        self._render_dp_table_42(str_a, str_b, prev_row, curr_row, highlight=(1, 0))
        self.step_info_42.configure(text=f"Шаг: инициализация строки 1")
    
    # Один шаг алгоритма
    def _do_step(self, prefix):
        state = self.step_state[prefix]
        
        if prefix in ["411", "412"]:
            if state["dp_table"] is None:
                messagebox.showwarning("Предупреждение", "Сначала нажмите 'Пошагово'")
                return
            
            dp_table = state["dp_table"]
            str_a = state["str_a"]
            str_b = state["str_b"]
            costs = state["costs"]
            i = state["i"]
            j = state["j"]
            n, m = len(str_a), len(str_b)
            
            if i > n:
                getattr(self, f"step_info_{prefix}").configure(text="Завершено!")
                return
            
            # Вычисляем ячейку
            replace_cost = 0 if str_a[i-1] == str_b[j-1] else costs[0]
            dp_table[i][j] = dp_table[i-1][j-1] + replace_cost
            
            insert_cost = dp_table[i][j-1] + costs[1]
            if insert_cost < dp_table[i][j]:
                dp_table[i][j] = insert_cost
            
            delete_cost = dp_table[i-1][j] + costs[2]
            if delete_cost < dp_table[i][j]:
                dp_table[i][j] = delete_cost
            
            if i >= 2 and str_a[i-1] != str_a[i-2]:
                two_del_cost = dp_table[i-2][j] + costs[3]
                if two_del_cost < dp_table[i][j]:
                    dp_table[i][j] = two_del_cost
            
            # Определяем предшественников для подсветки
            predecessors = [(i-1, j-1), (i, j-1), (i-1, j)]
            if i >= 2 and str_a[i-1] != str_a[i-2]:
                predecessors.append((i-2, j))
            
            self._render_dp_table(prefix, dp_table, str_a, str_b, 
                                 highlight=(i, j), predecessors=predecessors)
            
            # Информация о текущем шаге
            char_a = str_a[i-1] if i > 0 else ""
            char_b = str_b[j-1] if j > 0 else ""
            getattr(self, f"step_info_{prefix}").configure(
                text=f"Шаг: ячейка [{i}, {j}]  ({char_a} → {char_b})  = {dp_table[i][j]}"
            )
            
            # Переход к следующей ячейке
            j += 1
            if j > m:
                j = 1
                i += 1
            
            state["i"] = i
            state["j"] = j
            
            if i > n:
                result = dp_table[n][m]
                getattr(self, f"result_{prefix}").configure(
                    text=f"Минимальная стоимость: {result}",
                    text_color="#2ecc71"
                )
                getattr(self, f"step_info_{prefix}").configure(text="Завершено!")
                
                if prefix == "412":
                    operations, _ = task_12.edit_distance_with_operations(costs, str_a, str_b)
                    self._render_operations(operations)
        
        elif prefix == "42":
            if state["prev_row"] is None:
                messagebox.showwarning("Предупреждение", "Сначала нажмите 'Пошагово'")
                return
            
            prev_row = state["prev_row"]
            curr_row = state["curr_row"]
            str_a = state["str_a"]
            str_b = state["str_b"]
            i = state["i"]
            j = state["j"]
            n, m = len(str_a), len(str_b)
            
            if i > n:
                self.step_info_42.configure(text="Завершено!")
                return
            
            if j == 0:
                curr_row[0] = i
                j = 1
            else:
                if str_a[i-1] == str_b[j-1]:
                    curr_row[j] = prev_row[j-1]
                else:
                    curr_row[j] = 1 + min(prev_row[j], curr_row[j-1], prev_row[j-1])
                j += 1
                
                if j > m:
                    prev_row, curr_row = curr_row, prev_row
                    state["prev_row"] = prev_row
                    state["curr_row"] = curr_row
                    i += 1
                    j = 0
            
            state["i"] = i
            state["j"] = j
            
            self._render_dp_table_42(str_a, str_b, prev_row, curr_row, highlight=(i, j))
            self.step_info_42.configure(text=f"Шаг: строка {i}, столбец {j}")
            
            if i > n:
                result = prev_row[m]
                self.result_42.configure(text=f"Расстояние Левенштейна: {result}",
                                        text_color="#2ecc71")
                self.step_info_42.configure(text="Завершено!")
    
    # Сброс пошагового режима
    def _reset_step(self, prefix):
        state = self.step_state[prefix]
        
        if prefix in ["411", "412"]:
            state["dp_table"] = None
            state["i"] = 0
            state["j"] = 0
        elif prefix == "42":
            state["prev_row"] = None
            state["curr_row"] = None
            state["i"] = 0
            state["j"] = 0
        
        getattr(self, f"step_info_{prefix}").configure(text="")
        
        # Очищаем таблицу
        frame = getattr(self, f"dp_frame_{prefix}")
        for w in frame.winfo_children():
            w.destroy()
    
    # Отрисовка таблиц
    def _render_dp_table(self, prefix, dp_table, str_a, str_b, highlight=None, predecessors=None):
        frame = getattr(self, f"dp_frame_{prefix}")
        for w in frame.winfo_children():
            w.destroy()
        
        n, m = len(str_a), len(str_b)
        max_display = 20
        if n > max_display or m > max_display:
            ctk.CTkLabel(frame, 
                text=f"Таблица слишком большая ({n}×{m}). Показаны первые {max_display}×{max_display}.",
                text_color="orange").pack(pady=5)
            n_show, m_show = min(n, max_display), min(m, max_display)
        else:
            n_show, m_show = n, m
        
        # Заголовок
        header = ctk.CTkFrame(frame, fg_color="transparent")
        header.pack()
        ctk.CTkLabel(header, text="", width=35).pack(side="left")
        ctk.CTkLabel(header, text="ε", width=35).pack(side="left")
        for j in range(m_show):
            ctk.CTkLabel(header, text=str_b[j], width=35,
                        font=ctk.CTkFont(weight="bold")).pack(side="left")
        
        # Строки таблицы
        for i in range(n_show + 1):
            row = ctk.CTkFrame(frame, fg_color="transparent")
            row.pack()
            label = "ε" if i == 0 else str_a[i-1]
            ctk.CTkLabel(row, text=label, width=35,
                        font=ctk.CTkFont(weight="bold")).pack(side="left")
            for j in range(m_show + 1):
                val = dp_table[i][j]
                
                # Определяем цвет
                if highlight and (i, j) == highlight:
                    color = "#f39c12"  # Оранжевый — текущая ячейка
                    text_color = "white"
                elif predecessors and (i, j) in predecessors:
                    color = "#3498db"  # Синий — предшественники
                    text_color = "white"
                elif val == 0 and (i > 0 or j > 0):
                    color = "#2ecc71"  # Зелёный — нули
                    text_color = "white"
                elif val > 0:
                    max_val = max(dp_table[n][m], 1)
                    intensity = min(val / max_val, 1.0) if max_val > 0 else 0
                    color = self._heat_color(intensity)
                    text_color = "black"
                else:
                    color = "#34495e"
                    text_color = "gray"
                
                ctk.CTkLabel(row, text=str(val), width=35,
                            fg_color=color, corner_radius=4,
                            text_color=text_color
                            ).pack(side="left", padx=1, pady=1)
    
    def _render_dp_table_42(self, str_a, str_b, prev_row, curr_row, highlight=None):
        frame = self.dp_frame_42
        for w in frame.winfo_children():
            w.destroy()
        
        n, m = len(str_a), len(str_b)
        
        # Заголовок
        header = ctk.CTkFrame(frame, fg_color="transparent")
        header.pack()
        ctk.CTkLabel(header, text="", width=40).pack(side="left")
        ctk.CTkLabel(header, text="ε", width=35).pack(side="left")
        for j in range(m):
            ctk.CTkLabel(header, text=str_b[j], width=35,
                        font=ctk.CTkFont(weight="bold")).pack(side="left")
        
        # Предыдущая строка
        row_prev = ctk.CTkFrame(frame, fg_color="transparent")
        row_prev.pack()
        ctk.CTkLabel(row_prev, text="prev", width=40,
                    font=ctk.CTkFont(weight="bold")).pack(side="left")
        for j in range(m + 1):
            val = prev_row[j]
            color = "#3498db"
            ctk.CTkLabel(row_prev, text=str(val), width=35,
                        fg_color=color, corner_radius=4, text_color="white"
                        ).pack(side="left", padx=1, pady=1)
        
        # Текущая строка
        row_curr = ctk.CTkFrame(frame, fg_color="transparent")
        row_curr.pack()
        i_val = highlight[0] if highlight else 0
        label = "ε" if i_val == 0 else str_a[i_val-1] if i_val > 0 and i_val <= len(str_a) else ""
        ctk.CTkLabel(row_curr, text=f"curr ({label})", width=40,
                    font=ctk.CTkFont(weight="bold")).pack(side="left")
        for j in range(m + 1):
            val = curr_row[j]
            if highlight and highlight[1] == j and highlight[0] == i_val:
                color = "#f39c12"
                text_color = "white"
            else:
                color = "#ecf0f1"
                text_color = "black"
            ctk.CTkLabel(row_curr, text=str(val) if val > 0 or j == 0 else "", 
                        width=35, fg_color=color, corner_radius=4,
                        text_color=text_color
                        ).pack(side="left", padx=1, pady=1)
    
    def _heat_color(self, intensity):
        r = int(46 + (231 - 46) * intensity)
        g = int(204 - (204 - 76) * intensity)
        b = int(113 - (113 - 80) * intensity)
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def _render_operations(self, operations):
        for w in self.ops_412.winfo_children():
            w.destroy()
        
        colors = {"M": "#2ecc71", "R": "#f1c40f", "I": "#3498db", "D": "#e74c3c"}
        
        for op in operations:
            ctk.CTkLabel(
                self.ops_412, text=f" {op} ", 
                fg_color=colors.get(op, "gray"),
                corner_radius=5, width=30,
                font=ctk.CTkFont(weight="bold")
            ).pack(side="left", padx=2)


if __name__ == "__main__":
    app = EditDistanceApp()
    app.mainloop()
