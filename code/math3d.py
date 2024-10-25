import numpy as np
from stl import mesh
import tkinter as tk
from tkinter import messagebox
import sympy as sp
import os  # Додано для отримання повного шляху

# Функція для додавання трикутників
def add_triangles(v1, v2, v3, v4, vertices, faces):
    vertices.append(v1)
    vertices.append(v2)
    vertices.append(v3)
    faces.append([len(vertices) - 3, len(vertices) - 2, len(vertices) - 1])

    vertices.append(v2)
    vertices.append(v3)
    vertices.append(v4)
    faces.append([len(vertices) - 3, len(vertices) - 2, len(vertices) - 1])

# Функція для виправлення введення користувача
def fix_expression(expression):
    # Заміна символу кореня на sqrt()
    expression = expression.replace("√", "sqrt")
    expression = expression.replace("^", "**")

    expression = expression.replace(" ", "")

    expression = expression.replace(")x", ")*x")
    expression = expression.replace(")y", ")*y")
    expression = expression.replace("xy", "x*y")
    expression = expression.replace("yx", "y*x")

    expression = expression.replace(")c", ")*c")
    expression = expression.replace(")s", ")*s")
    expression = expression.replace(")t", ")*t")
    expression = expression.replace("xc", "x*c")
    expression = expression.replace("xs", "x*s")
    expression = expression.replace("xt", "x*t")
    expression = expression.replace("yc", "y*c")
    expression = expression.replace("ys", "y*s")
    expression = expression.replace("yt", "y*t")

    expression = expression.replace(")(", ")*(")

    expression = expression.replace("1x", "1*x")
    expression = expression.replace("2x", "2*x")
    expression = expression.replace("3x", "3*x")
    expression = expression.replace("4x", "4*x")
    expression = expression.replace("5x", "5*x")
    expression = expression.replace("6x", "6*x")
    expression = expression.replace("7x", "7*x")
    expression = expression.replace("8x", "8*x")
    expression = expression.replace("9x", "9*x")
    expression = expression.replace("0x", "0*x")

    expression = expression.replace("1y", "1*y")
    expression = expression.replace("2y", "2*y")
    expression = expression.replace("3y", "3*y")
    expression = expression.replace("4y", "4*y")
    expression = expression.replace("5y", "5*y")
    expression = expression.replace("6y", "6*y")
    expression = expression.replace("7y", "7*y")
    expression = expression.replace("8y", "8*y")
    expression = expression.replace("9y", "9*y")
    expression = expression.replace("0y", "0*y")
    
    expression = expression.replace("1t", "1*t")
    expression = expression.replace("2t", "2*t")
    expression = expression.replace("3t", "3*t")
    expression = expression.replace("4t", "4*t")
    expression = expression.replace("5t", "5*t")
    expression = expression.replace("6t", "6*t")
    expression = expression.replace("7t", "7*t")
    expression = expression.replace("8t", "8*t")
    expression = expression.replace("9t", "9*t")
    expression = expression.replace("0t", "0*t")
    
    expression = expression.replace("1c", "1*c")
    expression = expression.replace("2c", "2*c")
    expression = expression.replace("3c", "3*c")
    expression = expression.replace("4c", "4*c")
    expression = expression.replace("5c", "5*c")
    expression = expression.replace("6c", "6*c")
    expression = expression.replace("7c", "7*c")
    expression = expression.replace("8c", "8*c")
    expression = expression.replace("9c", "9*c")
    expression = expression.replace("0c", "0*c")
    
    expression = expression.replace("1s", "1*s")
    expression = expression.replace("2s", "2*s")
    expression = expression.replace("3s", "3*s")
    expression = expression.replace("4s", "4*s")
    expression = expression.replace("5s", "5*s")
    expression = expression.replace("6s", "6*s")
    expression = expression.replace("7s", "7*s")
    expression = expression.replace("8s", "8*s")
    expression = expression.replace("9s", "9*s")
    expression = expression.replace("0s", "0*s")
    # Додавання знаків множення між змінними та числами
    expression = sp.sympify(expression, evaluate=False)
    print(str(expression))
    return str(expression)

# Функція для створення 3D моделі на основі функції z = f(x, y)
def create_3d_model():
    try:
        formula = function_entry.get()  # Отримуємо формулу
        formula = fix_expression(formula)  # Виправляємо введення
        x_size = int(x_size_entry.get())  # Мін: 1, Макс: 100
        y_size = int(y_size_entry.get())  # Мін: 1, Макс: 100
        platform_thickness = float(platform_entry.get())  # Мін: 0.1, Макс: 10
        height_scale = float(height_entry.get())  # Мін: 0.1, Макс: 10
        z_offset = float(offset_entry.get())  # Мін: 0, Макс: 100
        quality_factor = float(quality_entry.get())  # Мін: 1, Макс: 10
        apply_height_filter = filter_var.get()  # Чи застосовувати фільтр висоти

        if not (1 <= x_size <= 100 and 1 <= y_size <= 100):
            raise ValueError("Розмір по X і Y повинен бути в діапазоні [1, 100].")
        if not (0.1 <= platform_thickness <= 10):
            raise ValueError("Товщина платформи повинна бути в діапазоні [0.1, 10].")
        if not (0.1 <= height_scale <= 10):
            raise ValueError("Масштаб висоти повинен бути в діапазоні [0.1, 10].")
        if not (0 <= z_offset <= 100):
            raise ValueError("Вертикальний відступ повинен бути в діапазоні [0, 100].")
        if not (1 <= quality_factor <= 10):
            raise ValueError("Якість моделі повинна бути в діапазоні [1, 10].")

        step = 1 / quality_factor  # Зменшення кроку підвищує якість

    except ValueError as ve:
        messagebox.showerror("Помилка", f"Введіть правильні числові значення: {ve}")
        return

    # Створюємо символічні змінні x і y
    x, y = sp.symbols('x y')

    try:
        # Перетворюємо формулу на вираз SymPy
        expr = sp.sympify(formula)
    except sp.SympifyError as e:
        messagebox.showerror("Помилка у формулі", f"Неможливо перетворити формулу: {e}")
        return

    # Створюємо сітку для x та y
    x_vals = np.arange(-x_size / 2, x_size / 2, step)
    y_vals = np.arange(-y_size / 2, y_size / 2, step)
    x_vals, y_vals = np.meshgrid(x_vals, y_vals)

    # Створюємо функцію для обчислення значень z
    z_func = sp.lambdify((x, y), expr, 'numpy')

    try:
        # Обробка можливого ділення на нуль у виразі
        x_vals[x_vals == 0] = np.finfo(float).eps  # Уникаємо ділення на нуль
        z_vals = z_func(x_vals, y_vals) * height_scale + z_offset  # Масштаб і зсув

        # Обмеження значень Z за допомогою if
        for i in range(z_vals.shape[0]):
            for j in range(z_vals.shape[1]):
                if apply_height_filter:  # Якщо фільтр висоти активний
                    if z_vals[i, j] > ((x_size + y_size) / 2) + z_offset:
                        z_vals[i, j] = ((x_size + y_size) / 2) + z_offset - 20
                    elif z_vals[i, j] < ((x_size + y_size) / -2) + z_offset:
                        z_vals[i, j] = ((x_size + y_size) / -2) + z_offset + 20
    except Exception as e:
        messagebox.showerror("Помилка у формулі", f"Помилка при обчисленні: {e}")
        return

    # Створення STL
    vertices = []
    faces = []

    # Додаємо рельєф до моделі (рельєф + верхня поверхня платформи)
    for i in range(x_vals.shape[0] - 1):
        for j in range(y_vals.shape[1] - 1):
            v1 = [x_vals[i, j], y_vals[i, j], z_vals[i, j] + platform_thickness]
            v2 = [x_vals[i + 1, j], y_vals[i + 1, j], z_vals[i + 1, j] + platform_thickness]
            v3 = [x_vals[i, j + 1], y_vals[i, j + 1], z_vals[i, j + 1] + platform_thickness]
            v4 = [x_vals[i + 1, j + 1], y_vals[i + 1, j + 1], z_vals[i + 1, j + 1] + platform_thickness]

            add_triangles(v1, v2, v3, v4, vertices, faces)

    # Додаємо верхню поверхню платформи (поверхня без рельєфу)
    for i in range(x_vals.shape[0] - 1):
        for j in range(y_vals.shape[1] - 1):
            v1 = [x_vals[i, j], y_vals[i, j], platform_thickness]
            v2 = [x_vals[i + 1, j], y_vals[i + 1, j], platform_thickness]
            v3 = [x_vals[i, j + 1], y_vals[i, j + 1], platform_thickness]
            v4 = [x_vals[i + 1, j + 1], y_vals[i + 1, j + 1], platform_thickness]

            add_triangles(v1, v2, v3, v4, vertices, faces)

    # Додаємо основу платформи (з нульовою висотою)
    for i in range(x_vals.shape[0] - 1):
        for j in range(y_vals.shape[1] - 1):
            v1 = [x_vals[i, j], y_vals[i, j], 0]
            v2 = [x_vals[i + 1, j], y_vals[i + 1, j], 0]
            v3 = [x_vals[i, j + 1], y_vals[i, j + 1], 0]
            v4 = [x_vals[i + 1, j + 1], y_vals[i + 1, j + 1], 0]

            add_triangles(v1, v2, v3, v4, vertices, faces)

    # Додаємо стінки платформи для усіх чотирьох сторін
    for i in range(x_vals.shape[0] - 1):
        # Ліва і права стінки
        v1 = [x_vals[i, 0], y_vals[i, 0], 0]
        v2 = [x_vals[i + 1, 0], y_vals[i + 1, 0], 0]
        v3 = [x_vals[i, 0], y_vals[i, 0], platform_thickness]
        v4 = [x_vals[i + 1, 0], y_vals[i + 1, 0], platform_thickness]
        add_triangles(v1, v2, v3, v4, vertices, faces)

        v1 = [x_vals[i, -1], y_vals[i, -1], 0]
        v2 = [x_vals[i + 1, -1], y_vals[i + 1, -1], 0]
        v3 = [x_vals[i, -1], y_vals[i, -1], platform_thickness]
        v4 = [x_vals[i + 1, -1], y_vals[i + 1, -1], platform_thickness]
        add_triangles(v1, v2, v3, v4, vertices, faces)

    # Передня і задня стінки
    for j in range(y_vals.shape[1] - 1):
        v1 = [x_vals[0, j], y_vals[0, j], 0]
        v2 = [x_vals[0, j + 1], y_vals[0, j + 1], 0]
        v3 = [x_vals[0, j], y_vals[0, j], platform_thickness]
        v4 = [x_vals[0, j + 1], y_vals[0, j + 1], platform_thickness]
        add_triangles(v1, v2, v3, v4, vertices, faces)

        v1 = [x_vals[-1, j], y_vals[-1, j], 0]
        v2 = [x_vals[-1, j + 1], y_vals[-1, j + 1], 0]
        v3 = [x_vals[-1, j], y_vals[-1, j], platform_thickness]
        v4 = [x_vals[-1, j + 1], y_vals[-1, j + 1], platform_thickness]
        add_triangles(v1, v2, v3, v4, vertices, faces)

    # Створення STL
    vertices = np.array(vertices)
    faces = np.array(faces)

    terrain = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
    for i, face in enumerate(faces):
        for j in range(3):
            terrain.vectors[i][j] = vertices[face[j], :]

    # Збереження STL файлу з повним шляхом
    file_name = "terrain_function_with_offset.stl"
    full_path = os.path.join(os.getcwd(), file_name)
    terrain.save(full_path)

    messagebox.showinfo("Успіх", f"STL файл збережено як '{full_path}'.")
    os.startfile(file_name)

# Функції для вставки математичних операторів у поле формули
def insert_sqrt():
    function_entry.insert(tk.END, '√(')  # Замість sqrt()

def insert_power():
    function_entry.insert(tk.END, '(^2)')

def insert_sin():
    function_entry.insert(tk.END, 'sin(')

def insert_cos():
    function_entry.insert(tk.END, 'cos(')

def insert_tan():
    function_entry.insert(tk.END, 'tan(')


# Функція для показу/приховування розділу "Додаткове"
def toggle_additional():
    if additional_frame.winfo_ismapped():
        additional_frame.grid_remove()
    else:
        additional_frame.grid()

# Створюємо інтерфейс на Tkinter
root = tk.Tk()
root.title("3D модель за функцією z = f(x, y)")

container = tk.Frame(root)
container.grid(row=0, column=0, padx=10, pady=10)

# Поля для введення параметрів
tk.Label(container, text="Формула z = f(x, y):").grid(row=0, column=0, sticky=tk.W)
function_entry = tk.Entry(container)
function_entry.grid(row=0, column=1, padx=10, pady=0)
function_entry.insert(0, "(sin(x) + cos(y))/x")  # Приклад формули

# Додаємо кнопки для вставки поширених математичних функцій
button_container = tk.Frame(root)
button_container.grid(row=1, column=0, padx=10, pady=0)

tk.Button(button_container, text="√", command=insert_sqrt).grid(row=0, column=0)
tk.Button(button_container, text="^", command=insert_power).grid(row=0, column=1)
tk.Button(button_container, text="sin", command=insert_sin).grid(row=0, column=2)
tk.Button(button_container, text="cos", command=insert_cos).grid(row=0, column=3)
tk.Button(button_container, text="tan", command=insert_tan).grid(row=0, column=4)

# Кнопка для показу/приховування розділу "Додаткове"
toggle_button = tk.Button(root, text="Додаткове ▼", command=toggle_additional)
toggle_button.grid(row=3, column=0, padx=10, pady=10)

# Додаємо розділ "Додаткове" для числових параметрів
additional_frame = tk.LabelFrame(root, text="Додаткове", padx=10, pady=10)
additional_frame.grid(row=4, column=0, padx=10, pady=10)
additional_frame.grid_remove()  # Початково приховуємо

tk.Label(additional_frame, text="Розмір по X (1-100):").grid(row=0, column=0, sticky=tk.W)
x_size_entry = tk.Entry(additional_frame)
x_size_entry.grid(row=0, column=1)
x_size_entry.insert(0, "20")

tk.Label(additional_frame, text="Розмір по Y (1-100):").grid(row=1, column=0, sticky=tk.W)
y_size_entry = tk.Entry(additional_frame)
y_size_entry.grid(row=1, column=1)
y_size_entry.insert(0, "20")

tk.Label(additional_frame, text="Товщина платформи (0.1-10):").grid(row=2, column=0, sticky=tk.W)
platform_entry = tk.Entry(additional_frame)
platform_entry.grid(row=2, column=1)
platform_entry.insert(0, "1")

tk.Label(additional_frame, text="Масштаб висоти (0.1-10):").grid(row=3, column=0, sticky=tk.W)
height_entry = tk.Entry(additional_frame)
height_entry.grid(row=3, column=1)
height_entry.insert(0, "1")

tk.Label(additional_frame, text="Вертикальний відступ (0-100):").grid(row=4, column=0, sticky=tk.W)
offset_entry = tk.Entry(additional_frame)
offset_entry.grid(row=4, column=1)
offset_entry.insert(0, "20")

tk.Label(additional_frame, text="Якість моделі (1-10):").grid(row=5, column=0, sticky=tk.W)
quality_entry = tk.Entry(additional_frame)
quality_entry.grid(row=5, column=1)
quality_entry.insert(0, "5")

# Додаємо чекбокс для фільтру висоти
filter_var = tk.IntVar(value=1) 
tk.Checkbutton(additional_frame, text="Застосувати фільтр висоти", variable=filter_var).grid(row=6, columnspan=2)

# Кнопка для створення 3D моделі
tk.Button(root, text="Створити 3D модель", command=create_3d_model).grid(row=2, column=0, columnspan=2)

root.mainloop()
