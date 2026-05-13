import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime


class MovieLibrary:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Library - Личная кинотека")
        self.root.geometry("850x550")
        self.root.resizable(True, True)

        # Убеждаемся, что окно появляется поверх других
        self.root.lift()
        self.root.attributes('-topmost', True)
        self.root.after(100, lambda: self.root.attributes('-topmost', False))

        self.data_file = "movies.json"
        self.movies = []
        self.load_data()

        # Создаём все элементы интерфейса
        self.create_input_fields()
        self.create_buttons()
        self.create_filters()
        self.create_table()

        # Загружаем данные в таблицу
        self.refresh_table()

    def create_input_fields(self):
        """Создание полей для ввода данных"""
        # Основной фрейм для ввода
        input_frame = ttk.LabelFrame(self.root, text="📝 Добавление нового фильма", padding=10)
        input_frame.pack(fill="x", padx=10, pady=5)

        # Название
        ttk.Label(input_frame, text="Название:", font=("Arial", 10)).grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.entry_title = ttk.Entry(input_frame, width=30, font=("Arial", 10))
        self.entry_title.grid(row=0, column=1, padx=5, pady=5)

        # Жанр
        ttk.Label(input_frame, text="Жанр:", font=("Arial", 10)).grid(row=0, column=2, sticky="e", padx=5, pady=5)
        self.entry_genre = ttk.Entry(input_frame, width=20, font=("Arial", 10))
        self.entry_genre.grid(row=0, column=3, padx=5, pady=5)

        # Год
        ttk.Label(input_frame, text="Год выпуска:", font=("Arial", 10)).grid(row=1, column=0, sticky="e", padx=5,
                                                                             pady=5)
        self.entry_year = ttk.Entry(input_frame, width=10, font=("Arial", 10))
        self.entry_year.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        # Рейтинг
        ttk.Label(input_frame, text="Рейтинг (0-10):", font=("Arial", 10)).grid(row=1, column=2, sticky="e", padx=5,
                                                                                pady=5)
        self.entry_rating = ttk.Entry(input_frame, width=10, font=("Arial", 10))
        self.entry_rating.grid(row=1, column=3, padx=5, pady=5, sticky="w")

    def create_buttons(self):
        """Создание кнопок управления"""
        button_frame = ttk.Frame(self.root)
        button_frame.pack(fill="x", padx=10, pady=5)

        # Стили для кнопок
        style = ttk.Style()
        style.configure("Add.TButton", foreground="green")
        style.configure("Delete.TButton", foreground="red")

        add_btn = ttk.Button(button_frame, text="➕ Добавить фильм", command=self.add_movie, width=18)
        add_btn.pack(side="left", padx=5)

        delete_btn = ttk.Button(button_frame, text="🗑 Удалить выбранный", command=self.delete_movie, width=18)
        delete_btn.pack(side="left", padx=5)

        save_btn = ttk.Button(button_frame, text="💾 Сохранить в JSON", command=self.save_data, width=18)
        save_btn.pack(side="left", padx=5)

        refresh_btn = ttk.Button(button_frame, text="🔄 Обновить", command=self.refresh_table, width=18)
        refresh_btn.pack(side="left", padx=5)

    def create_filters(self):
        """Создание фильтров"""
        filter_frame = ttk.LabelFrame(self.root, text="🔍 Фильтрация фильмов", padding=10)
        filter_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(filter_frame, text="По жанру:", font=("Arial", 10)).grid(row=0, column=0, sticky="e", padx=5)
        self.filter_genre = ttk.Entry(filter_frame, width=25, font=("Arial", 10))
        self.filter_genre.grid(row=0, column=1, padx=5)

        ttk.Label(filter_frame, text="По году:", font=("Arial", 10)).grid(row=0, column=2, sticky="e", padx=5)
        self.filter_year = ttk.Entry(filter_frame, width=10, font=("Arial", 10))
        self.filter_year.grid(row=0, column=3, padx=5)

        apply_btn = ttk.Button(filter_frame, text="🔍 Применить фильтр", command=self.apply_filter)
        apply_btn.grid(row=0, column=4, padx=10)

        reset_btn = ttk.Button(filter_frame, text="❌ Сбросить", command=self.reset_filter)
        reset_btn.grid(row=0, column=5, padx=5)

    def create_table(self):
        """Создание таблицы для отображения фильмов"""
        # Фрейм для таблицы и скролла
        table_frame = ttk.Frame(self.root)
        table_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Создаём скроллбары
        scroll_y = ttk.Scrollbar(table_frame, orient="vertical")
        scroll_x = ttk.Scrollbar(table_frame, orient="horizontal")

        columns = ("Название", "Жанр", "Год", "Рейтинг")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings",
                                 yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

        # Настройка колонок
        self.tree.heading("Название", text="🎬 Название")
        self.tree.heading("Жанр", text="🎭 Жанр")
        self.tree.heading("Год", text="📅 Год")
        self.tree.heading("Рейтинг", text="⭐ Рейтинг")

        self.tree.column("Название", width=250, minwidth=150)
        self.tree.column("Жанр", width=150, minwidth=100)
        self.tree.column("Год", width=80, minwidth=60, anchor="center")
        self.tree.column("Рейтинг", width=100, minwidth=80, anchor="center")

        # Настройка скроллбаров
        scroll_y.config(command=self.tree.yview)
        scroll_x.config(command=self.tree.xview)

        # Размещение
        self.tree.grid(row=0, column=0, sticky="nsew")
        scroll_y.grid(row=0, column=1, sticky="ns")
        scroll_x.grid(row=1, column=0, sticky="ew")

        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        # Привязываем событие двойного клика для редактирования (опционально)
        self.tree.bind("<Double-Button-1>", self.on_item_double_click)

    def validate_movie(self, title, genre, year_str, rating_str):
        """Валидация вводимых данных"""
        if not title or not title.strip():
            messagebox.showerror("Ошибка валидации", "❌ Название фильма не может быть пустым!")
            return False

        if not genre or not genre.strip():
            messagebox.showerror("Ошибка валидации", "❌ Жанр не может быть пустым!")
            return False

        # Проверка года
        try:
            year = int(year_str)
            current_year = datetime.now().year
            if year < 1888:
                messagebox.showerror("Ошибка валидации",
                                     "❌ Год не может быть раньше 1888 (год изобретения кинематографа)!")
                return False
            if year > current_year + 1:
                messagebox.showerror("Ошибка валидации", f"❌ Год не может быть позже {current_year + 1}!")
                return False
        except ValueError:
            messagebox.showerror("Ошибка валидации", "❌ Год должен быть целым числом!")
            return False

        # Проверка рейтинга
        try:
            rating = float(rating_str)
            if rating < 0 or rating > 10:
                messagebox.showerror("Ошибка валидации", "❌ Рейтинг должен быть в диапазоне от 0 до 10!")
                return False
        except ValueError:
            messagebox.showerror("Ошибка валидации",
                                 "❌ Рейтинг должен быть числом (можно использовать точку для десятичных)!")
            return False

        return True

    def add_movie(self):
        """Добавление нового фильма"""
        title = self.entry_title.get().strip()
        genre = self.entry_genre.get().strip()
        year_str = self.entry_year.get().strip()
        rating_str = self.entry_rating.get().strip()

        if not self.validate_movie(title, genre, year_str, rating_str):
            return

        movie = {
            "title": title,
            "genre": genre,
            "year": int(year_str),
            "rating": float(rating_str)
        }

        self.movies.append(movie)
        self.save_data()
        self.refresh_table()
        self.clear_inputs()

        messagebox.showinfo("Успех!", f"✅ Фильм \"{title}\" успешно добавлен в библиотеку!")

    def delete_movie(self):
        """Удаление выбранного фильма"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "⚠️ Пожалуйста, выберите фильм для удаления!")
            return

        # Подтверждение удаления
        item = self.tree.item(selected[0])
        title = item["values"][0]

        if messagebox.askyesno("Подтверждение удаления", f"Вы уверены, что хотите удалить фильм \"{title}\"?"):
            self.movies = [m for m in self.movies if m["title"] != title]
            self.save_data()
            self.refresh_table()
            messagebox.showinfo("Успех!", f"✅ Фильм \"{title}\" удалён из библиотеки!")

    def clear_inputs(self):
        """Очистка полей ввода"""
        self.entry_title.delete(0, tk.END)
        self.entry_genre.delete(0, tk.END)
        self.entry_year.delete(0, tk.END)
        self.entry_rating.delete(0, tk.END)

        # Устанавливаем фокус на поле названия для удобства
        self.entry_title.focus()

    def refresh_table(self, filtered_movies=None):
        """Обновление таблицы"""
        # Очищаем таблицу
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Выбираем данные для отображения
        data = filtered_movies if filtered_movies is not None else self.movies

        # Заполняем таблицу
        for movie in data:
            # Форматируем рейтинг для отображения
            rating_display = f"{movie['rating']:.1f}" if isinstance(movie['rating'], float) else str(movie['rating'])
            self.tree.insert("", tk.END, values=(
                movie["title"],
                movie["genre"],
                movie["year"],
                rating_display
            ))

    def apply_filter(self):
        """Применение фильтрации"""
        genre_filter = self.filter_genre.get().strip().lower()
        year_filter = self.filter_year.get().strip()

        filtered = self.movies.copy()

        if genre_filter:
            filtered = [m for m in filtered if genre_filter in m["genre"].lower()]

        if year_filter:
            try:
                year_int = int(year_filter)
                filtered = [m for m in filtered if m["year"] == year_int]
            except ValueError:
                messagebox.showerror("Ошибка фильтрации", "❌ Год для фильтрации должен быть целым числом!")
                return

        self.refresh_table(filtered)

        # Показываем количество найденных фильмов
        count = len(filtered)
        if count == 0:
            messagebox.showinfo("Результат фильтрации", "🔍 Фильмов, соответствующих критериям, не найдено.")

    def reset_filter(self):
        """Сброс фильтрации"""
        self.filter_genre.delete(0, tk.END)
        self.filter_year.delete(0, tk.END)
        self.refresh_table()
        messagebox.showinfo("Фильтр сброшен", "✅ Отображены все фильмы из библиотеки.")

    def on_item_double_click(self, event):
        """Обработка двойного клика по элементу (показ информации)"""
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected[0])
            title, genre, year, rating = item["values"]
            messagebox.showinfo("Информация о фильме",
                                f"🎬 Название: {title}\n"
                                f"🎭 Жанр: {genre}\n"
                                f"📅 Год: {year}\n"
                                f"⭐ Рейтинг: {rating}")

    def load_data(self):
        """Загрузка данных из JSON файла"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r", encoding="utf-8") as f:
                    self.movies = json.load(f)
                print(f"Загружено {len(self.movies)} фильмов из {self.data_file}")
            except json.JSONDecodeError:
                print("Ошибка чтения JSON файла. Создаётся новый файл.")
                self.movies = []
            except Exception as e:
                print(f"Ошибка при загрузке: {e}")
                self.movies = []
        else:
            print(f"Файл {self.data_file} не найден. Будет создан новый при сохранении.")
            self.movies = []

    def save_data(self):
        """Сохранение данных в JSON файл"""
        try:
            with open(self.data_file, "w", encoding="utf-8") as f:
                json.dump(self.movies, f, ensure_ascii=False, indent=4)
            print(f"Сохранено {len(self.movies)} фильмов в {self.data_file}")
            return True
        except Exception as e:
            messagebox.showerror("Ошибка сохранения", f"Не удалось сохранить данные: {e}")
            return False


def main():
    """Главная функция запуска приложения"""
    try:
        # Создаём корневое окно
        root = tk.Tk()

        # Устанавливаем иконку (опционально, если есть файл)
        try:
            root.iconbitmap(default='movie.ico')  # Если есть файл иконки
        except:
            pass

        # Создаём приложение
        app = MovieLibrary(root)

        # Центрируем окно на экране
        root.update_idletasks()
        width = root.winfo_width()
        height = root.winfo_height()
        x = (root.winfo_screenwidth() // 2) - (width // 2)
        y = (root.winfo_screenheight() // 2) - (height // 2)
        root.geometry(f'{width}x{height}+{x}+{y}')

        # Запускаем главный цикл
        print("Приложение Movie Library запущено!")
        root.mainloop()

    except Exception as e:
        print(f"Ошибка при запуске приложения: {e}")
        input("Нажмите Enter для выхода...")


if __name__ == "__main__":
    main()