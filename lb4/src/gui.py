import customtkinter as ctk
from tkinter import messagebox
import sys
import os
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

        self._build_ui()
    
    def _build_ui(self):
        # Верхняя панель с заголовком
        top = ctk.CTkFrame(self, fg_color="transparent")
        top.pack(fill="x", padx=20, pady=(15, 5))
        
        # Заголовок
        ctk.CTkLabel(
            top, 
            text="Редакционное расстояние",
            font=ctk.CTkFont(size=24, weight="bold")
        ).pack() 
        
        # Вкладки
        self.tabs = ctk.CTkTabview(self)
        self.tabs.pack(fill="both", expand=True, padx=20, pady=10)
        
        self._build_tab_411()
        self._build_tab_412()
        self._build_tab_42()
    
    # Вкладка 4.1.1 — только стоимость
    def _build_tab_411(self):
        tab = self.tabs.add("4.1.1 Стоимость")
        
        self._add_string_inputs(tab, prefix="411")
        
        costs_frame = ctk.CTkFrame(tab)
        costs_frame.pack(fill="x", pady=10)
        ctk.CTkLabel(costs_frame, text="Стоимости операций:", 
                    font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=10, pady=(8, 4))
        
        costs_inner = ctk.CTkFrame(costs_frame, fg_color="transparent")
        costs_inner.pack(fill="x", padx=10, pady=(0, 8))
        
        self.cost_411 = {}
        for i, (name, default) in enumerate([
            ("Replace", 1), ("Insert", 1), ("Delete", 1), ("Delete×2", 2)
        ]):
            ctk.CTkLabel(costs_inner, text=f"{name}:").grid(row=0, column=i*2, padx=5)
            entry = ctk.CTkEntry(costs_inner, width=60)
            entry.insert(0, str(default))
            entry.grid(row=0, column=i*2+1, padx=5)
            self.cost_411[name] = entry
        
        btns = ctk.CTkFrame(tab, fg_color="transparent")
        btns.pack(fill="x", pady=10)
        ctk.CTkButton(btns, text="Вычислить", width=150,
                     command=self._calc_411).pack(side="left", padx=5)
        ctk.CTkButton(btns, text="Пример", width=100, fg_color="gray",
                     command=lambda: self._fill_example("411")).pack(side="left", padx=5)
        
        self.result_411 = ctk.CTkLabel(tab, text="", font=ctk.CTkFont(size=18, weight="bold"))
        self.result_411.pack(pady=5)
        
        self._add_dp_table(tab, "411")
    
    # Вкладка 4.1.2 — стоимость + операции
    def _build_tab_412(self):
        tab = self.tabs.add("4.1.2 Операции")
        
        self._add_string_inputs(tab, prefix="412")
        
        costs_frame = ctk.CTkFrame(tab)
        costs_frame.pack(fill="x", pady=10)
        ctk.CTkLabel(costs_frame, text="Стоимости операций:", 
                    font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=10, pady=(8, 4))
        
        costs_inner = ctk.CTkFrame(costs_frame, fg_color="transparent")
        costs_inner.pack(fill="x", padx=10, pady=(0, 8))
        
        self.cost_412 = {}
        for i, (name, default) in enumerate([
            ("Replace", 1), ("Insert", 1), ("Delete", 1), ("Delete×2", 2)
        ]):
            ctk.CTkLabel(costs_inner, text=f"{name}:").grid(row=0, column=i*2, padx=5)
            entry = ctk.CTkEntry(costs_inner, width=60)
            entry.insert(0, str(default))
            entry.grid(row=0, column=i*2+1, padx=5)
            self.cost_412[name] = entry
        
        btns = ctk.CTkFrame(tab, fg_color="transparent")
        btns.pack(fill="x", pady=10)
        ctk.CTkButton(btns, text="Вычислить", width=150,
                     command=self._calc_412).pack(side="left", padx=5)
        ctk.CTkButton(btns, text="Пример", width=100, fg_color="gray",
                     command=lambda: self._fill_example("412")).pack(side="left", padx=5)
        
        self.result_412 = ctk.CTkLabel(tab, text="", font=ctk.CTkFont(size=18, weight="bold"))
        self.result_412.pack(pady=5)
        
        self.ops_412 = ctk.CTkFrame(tab, fg_color="transparent")
        self.ops_412.pack(pady=5)
        
        legend = ctk.CTkFrame(tab, fg_color="transparent")
        legend.pack(pady=5)
        for op, color, desc in [
            ("M", "#2ecc71", "Match"), ("R", "#f1c40f", "Replace"),
            ("I", "#3498db", "Insert"), ("D", "#e74c3c", "Delete")
        ]:
            ctk.CTkLabel(legend, text=f" {op} ", fg_color=color,
                        corner_radius=4, width=25).pack(side="left", padx=2)
            ctk.CTkLabel(legend, text=f"= {desc}  ").pack(side="left")
    
    # Вкладка 4.2 — Левенштейн
    def _build_tab_42(self):
        tab = self.tabs.add("4.2 Левенштейн")
        
        self._add_string_inputs(tab, prefix="42")
        
        info = ctk.CTkLabel(tab, 
            text="Все операции имеют стоимость 1. Память: O(min(n,m))",
            text_color="gray", font=ctk.CTkFont(size=12))
        info.pack(pady=5)
        
        btns = ctk.CTkFrame(tab, fg_color="transparent")
        btns.pack(fill="x", pady=10)
        ctk.CTkButton(btns, text="Вычислить", width=150,
                     command=self._calc_42).pack(side="left", padx=5)
        ctk.CTkButton(btns, text="Пример", width=100, fg_color="gray",
                     command=lambda: self._fill_example("42")).pack(side="left", padx=5)
        
        self.result_42 = ctk.CTkLabel(tab, text="", font=ctk.CTkFont(size=18, weight="bold"))
        self.result_42.pack(pady=5)
    
    # Вспомогательные методы построения
    def _add_string_inputs(self, parent, prefix):
        frame = ctk.CTkFrame(parent)
        frame.pack(fill="x", pady=10, padx=10)
        
        setattr(self, f"entry_a_{prefix}", None)
        setattr(self, f"entry_b_{prefix}", None)
        
        for label, key in [("Строка A:", f"entry_a_{prefix}"), 
                           ("Строка B:", f"entry_b_{prefix}")]:
            row = ctk.CTkFrame(frame, fg_color="transparent")
            row.pack(fill="x", pady=5, padx=10)
            ctk.CTkLabel(row, text=label, width=80, anchor="w").pack(side="left")
            entry = ctk.CTkEntry(row, width=400)
            entry.pack(side="left", fill="x", expand=True)
            setattr(self, key, entry)
    
    def _add_dp_table(self, parent, prefix):
        ctk.CTkLabel(parent, text="Таблица динамического программирования:",
                    font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=10, pady=(10, 5))
        
        scroll = ctk.CTkScrollableFrame(parent, height=200)
        scroll.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        setattr(self, f"dp_frame_{prefix}", scroll)
        setattr(self, f"dp_cells_{prefix}", [])
    
    # Примеры
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
    
    # Вычисления
    def _calc_411(self):
        try:
            str_a = self.entry_a_411.get()
            str_b = self.entry_b_411.get()
            costs = [int(self.cost_411[n].get()) for n in 
                    ["Replace", "Insert", "Delete", "Delete×2"]]
            
            n_val, m_val = len(str_a), len(str_b)
            dp_table = task_11.create_dp_table(
                n_val, m_val, str_a, str_b,
                costs[0], costs[1], costs[2], costs[3]
            )
            result = dp_table[n_val][m_val]
            
            self.result_411.configure(text=f"Минимальная стоимость: {result}",
                                     text_color="#2ecc71")
            self._render_dp_table("411", dp_table, str_a, str_b)
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректные числа для стоимостей")
    
    def _calc_412(self):
        try:
            str_a = self.entry_a_412.get()
            str_b = self.entry_b_412.get()
            costs = [int(self.cost_412[n].get()) for n in 
                    ["Replace", "Insert", "Delete", "Delete×2"]]
            
            operations, total = task_12.edit_distance_with_operations(costs, str_a, str_b)
            
            self.result_412.configure(
                text=f"Стоимость: {total}   |   Операций: {len(operations)}",
                text_color="#2ecc71"
            )
            self._render_operations(operations)
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
    
    # Отрисовка DP-таблицы
    def _render_dp_table(self, prefix, dp_table, str_a, str_b):
        frame = getattr(self, f"dp_frame_{prefix}")
        for w in frame.winfo_children():
            w.destroy()
        
        n, m = len(str_a), len(str_b)
        max_display = 20
        if n > max_display or m > max_display:
            ctk.CTkLabel(frame, 
                text=f"⚠ Таблица слишком большая ({n}×{m}). Показаны первые {max_display}×{max_display}.",
                text_color="orange").pack(pady=5)
            n_show, m_show = min(n, max_display), min(m, max_display)
        else:
            n_show, m_show = n, m
        
        header = ctk.CTkFrame(frame, fg_color="transparent")
        header.pack()
        ctk.CTkLabel(header, text="", width=35).pack(side="left")
        ctk.CTkLabel(header, text="ε", width=35).pack(side="left")
        for j in range(m_show):
            ctk.CTkLabel(header, text=str_b[j], width=35,
                        font=ctk.CTkFont(weight="bold")).pack(side="left")
        
        for i in range(n_show + 1):
            row = ctk.CTkFrame(frame, fg_color="transparent")
            row.pack()
            label = "ε" if i == 0 else str_a[i-1]
            ctk.CTkLabel(row, text=label, width=35,
                        font=ctk.CTkFont(weight="bold")).pack(side="left")
            for j in range(m_show + 1):
                val = dp_table[i][j]
                max_val = max(dp_table[n][m], 1)
                intensity = min(val / max_val, 1.0) if max_val > 0 else 0
                color = self._heat_color(intensity)
                ctk.CTkLabel(row, text=str(val), width=35,
                            fg_color=color, corner_radius=4).pack(side="left", padx=1, pady=1)
    
    def _heat_color(self, intensity):
        r = int(46 + (231 - 46) * intensity)
        g = int(204 - (204 - 76) * intensity)
        b = int(113 - (113 - 80) * intensity)
        return f"#{r:02x}{g:02x}{b:02x}"
    
    # Отрисовка операций
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