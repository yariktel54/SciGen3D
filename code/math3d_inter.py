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
    return str(expression)

# Функція для створення 3D моделі на основі функції z = f(x, y)
def create_3d_model():
    try:
        formula = function_entry.get()
        formula = fix_expression(formula)
        x_size = int(x_size_entry.get())
        y_size = int(y_size_entry.get())
        platform_thickness = float(platform_entry.get())
        height_scale = float(height_entry.get())
        z_offset = float(offset_entry.get())
        quality_factor = float(quality_entry.get())
        apply_height_filter = filter_var.get()

        if not (1 <= x_size <= 100 and 1 <= y_size <= 100):
            raise ValueError("The size in X and Y should be in the range [1, 100].")
        if not (0.1 <= platform_thickness <= 10):
            raise ValueError("The thickness of the platform should be in the range [0.1, 10].")
        if not (0.1 <= height_scale <= 10):
            raise ValueError("The height scale should be in the range [0.1, 10].")
        if not (0 <= z_offset <= 100):
            raise ValueError("The vertical offset should be in the range [0, 100].")
        if not (1 <= quality_factor <= 10):
            raise ValueError("The quality of the model should be in the range [1, 10].")

        step = 1 / quality_factor

    except ValueError as ve:
        messagebox.showerror("Error", f"Enter the correct numerical values: {ve}")
        return

    x, y = sp.symbols('x y')

    try:
        expr = sp.sympify(formula)
    except sp.SympifyError as e:
        messagebox.showerror("An error in the formula", f"Unable to convert formula: {e}")
        return

    x_vals = np.arange(-x_size / 2, x_size / 2, step)
    y_vals = np.arange(-y_size / 2, y_size / 2, step)
    x_vals, y_vals = np.meshgrid(x_vals, y_vals)

    z_func = sp.lambdify((x, y), expr, 'numpy')

    try:
        x_vals[x_vals == 0] = np.finfo(float).eps
        z_vals = z_func(x_vals, y_vals) * height_scale + z_offset

        for i in range(z_vals.shape[0]):
            for j in range(z_vals.shape[1]):
                if apply_height_filter:
                    if z_vals[i, j] > ((x_size + y_size) / 2) + z_offset:
                        z_vals[i, j] = ((x_size + y_size) / 2) + z_offset - 20
                    elif z_vals[i, j] < ((x_size + y_size) / -2) + z_offset:
                        z_vals[i, j] = ((x_size + y_size) / -2) + z_offset + 20
    except Exception as e:
        messagebox.showerror("An error in the formula", f"Calculation error: {e}")
        return

    vertices = []
    faces = []

    # Додаємо рельєф до моделі
    for i in range(x_vals.shape[0] - 1):
        for j in range(y_vals.shape[1] - 1):
            v1 = [x_vals[i, j], y_vals[i, j], z_vals[i, j] + platform_thickness]
            v2 = [x_vals[i + 1, j], y_vals[i + 1, j], z_vals[i + 1, j] + platform_thickness]
            v3 = [x_vals[i, j + 1], y_vals[i, j + 1], z_vals[i, j + 1] + platform_thickness]
            v4 = [x_vals[i + 1, j + 1], y_vals[i + 1, j + 1], z_vals[i + 1, j + 1] + platform_thickness]

            # Верхня сторона графіка
            faces.append([len(vertices), len(vertices) + 1, len(vertices) + 2])
            faces.append([len(vertices) + 1, len(vertices) + 3, len(vertices) + 2])

            # Нижня сторона графіка (зворотний порядок вершин)
            faces.append([len(vertices), len(vertices) + 2, len(vertices) + 1])
            faces.append([len(vertices) + 1, len(vertices) + 2, len(vertices) + 3])

            vertices.extend([v1, v2, v3, v4])

    # Додаємо верхню поверхню платформи (залишаємо як було)
    for i in range(x_vals.shape[0] - 1):
        for j in range(y_vals.shape[1] - 1):
            v1 = [x_vals[i, j], y_vals[i, j], platform_thickness]
            v2 = [x_vals[i + 1, j], y_vals[i + 1, j], platform_thickness]
            v3 = [x_vals[i, j + 1], y_vals[i, j + 1], platform_thickness]
            v4 = [x_vals[i + 1, j + 1], y_vals[i + 1, j + 1], platform_thickness]

            faces.append([len(vertices), len(vertices) + 2, len(vertices) + 1])
            faces.append([len(vertices) + 1, len(vertices) + 2, len(vertices) + 3])
            vertices.extend([v1, v2, v3, v4])

    # Додаємо перевернуту основу платформи
    for i in range(x_vals.shape[0] - 1):
        for j in range(y_vals.shape[1] - 1):
            v1 = [x_vals[i, j], y_vals[i, j], 0]
            v2 = [x_vals[i + 1, j], y_vals[i + 1, j], 0]
            v3 = [x_vals[i, j + 1], y_vals[i, j + 1], 0]
            v4 = [x_vals[i + 1, j + 1], y_vals[i + 1, j + 1], 0]

            faces.append([len(vertices), len(vertices) + 1, len(vertices) + 2])  # Перевернутий порядок
            faces.append([len(vertices) + 1, len(vertices) + 3, len(vertices) + 2])  # Перевернутий порядок
            vertices.extend([v1, v2, v3, v4])

    # Додаємо стінки платформи
    for i in range(x_vals.shape[0] - 1):
        # Ліва стінка
        v1 = [x_vals[i, 0], y_vals[i, 0], 0]
        v2 = [x_vals[i + 1, 0], y_vals[i + 1, 0], 0]
        v3 = [x_vals[i, 0], y_vals[i, 0], platform_thickness]
        v4 = [x_vals[i + 1, 0], y_vals[i + 1, 0], platform_thickness]
        faces.append([len(vertices), len(vertices) + 2, len(vertices) + 1])
        faces.append([len(vertices) + 3, len(vertices) + 1, len(vertices) + 2])
        vertices.extend([v1, v2, v3, v4])

        # Права стінка
        v1 = [x_vals[i, -1], y_vals[i, -1], 0]
        v2 = [x_vals[i + 1, -1], y_vals[i + 1, -1], 0]
        v3 = [x_vals[i, -1], y_vals[i, -1], platform_thickness]
        v4 = [x_vals[i + 1, -1], y_vals[i + 1, -1], platform_thickness]
        faces.append([len(vertices), len(vertices) + 1, len(vertices) + 2])
        faces.append([len(vertices) + 1, len(vertices) + 3, len(vertices) + 2])
        vertices.extend([v1, v2, v3, v4])

    for j in range(y_vals.shape[1] - 1):
        # Передня стінка
        v1 = [x_vals[0, j], y_vals[0, j], 0]
        v2 = [x_vals[0, j + 1], y_vals[0, j + 1], 0]
        v3 = [x_vals[0, j], y_vals[0, j], platform_thickness]
        v4 = [x_vals[0, j + 1], y_vals[0, j + 1], platform_thickness]
        faces.append([len(vertices), len(vertices) + 1, len(vertices) + 2])
        faces.append([len(vertices) + 1, len(vertices) + 3, len(vertices) + 2])
        vertices.extend([v1, v2, v3, v4])

        # Задня стінка
        v1 = [x_vals[-1, j], y_vals[-1, j], 0]
        v2 = [x_vals[-1, j + 1], y_vals[-1, j + 1], 0]
        v3 = [x_vals[-1, j], y_vals[-1, j], platform_thickness]
        v4 = [x_vals[-1, j + 1], y_vals[-1, j + 1], platform_thickness]
        faces.append([len(vertices), len(vertices) + 2, len(vertices) + 1])
        faces.append([len(vertices) + 2, len(vertices) + 3, len(vertices) + 1])
        vertices.extend([v1, v2, v3, v4])

    vertices = np.array(vertices)
    faces = np.array(faces)

    terrain = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
    for i, face in enumerate(faces):
        for j in range(3):
            terrain.vectors[i][j] = vertices[face[j], :]

    file_name = "math.stl"
    full_path = os.path.join(os.getcwd(), file_name)
    terrain.save(full_path)

    messagebox.showinfo("Success", f"STL file saved as '{full_path}'.")
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
root.title("3D model of the z = f(x, y)")

container = tk.Frame(root)
container.grid(row=0, column=0, padx=10, pady=10)

# Поля для введення параметрів
tk.Label(container, text="Formula z = f(x, y):").grid(row=0, column=0, sticky=tk.W)
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
toggle_button = tk.Button(root, text="Additional ▼", command=toggle_additional)
toggle_button.grid(row=3, column=0, padx=10, pady=10)

# Додаємо розділ "Додаткове" для числових параметрів
additional_frame = tk.LabelFrame(root, text="Additional", padx=10, pady=10)
additional_frame.grid(row=4, column=0, padx=10, pady=10)
additional_frame.grid_remove()  # Початково приховуємо

tk.Label(additional_frame, text="Size in X (1-100):").grid(row=0, column=0, sticky=tk.W)
x_size_entry = tk.Entry(additional_frame)
x_size_entry.grid(row=0, column=1)
x_size_entry.insert(0, "20")

tk.Label(additional_frame, text="Size in Y (1-100):").grid(row=1, column=0, sticky=tk.W)
y_size_entry = tk.Entry(additional_frame)
y_size_entry.grid(row=1, column=1)
y_size_entry.insert(0, "20")

tk.Label(additional_frame, text="Platform thickness (0.1-10):").grid(row=2, column=0, sticky=tk.W)
platform_entry = tk.Entry(additional_frame)
platform_entry.grid(row=2, column=1)
platform_entry.insert(0, "1")

tk.Label(additional_frame, text="Height scale (0.1-10):").grid(row=3, column=0, sticky=tk.W)
height_entry = tk.Entry(additional_frame)
height_entry.grid(row=3, column=1)
height_entry.insert(0, "1")

tk.Label(additional_frame, text="Vertical indentation (0-100):").grid(row=4, column=0, sticky=tk.W)
offset_entry = tk.Entry(additional_frame)
offset_entry.grid(row=4, column=1)
offset_entry.insert(0, "20")

tk.Label(additional_frame, text="Model quality (1-10):").grid(row=5, column=0, sticky=tk.W)
quality_entry = tk.Entry(additional_frame)
quality_entry.grid(row=5, column=1)
quality_entry.insert(0, "5")

# Додаємо чекбокс для фільтру висоти
filter_var = tk.IntVar(value=0) 
tk.Checkbutton(additional_frame, text="Apply height filter", variable=filter_var).grid(row=6, columnspan=2)

# Кнопка для створення 3D моделі
tk.Button(root, text="Create a 3D model", command=create_3d_model).grid(row=2, column=0, columnspan=2)

root.mainloop()
