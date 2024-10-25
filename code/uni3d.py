import os
import math
import requests
from PIL import Image, ImageTk
from io import BytesIO
import numpy as np
from stl import mesh
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

# Список градієнту 
rgb_gradient = np.array([[248, 245, 254],[248, 245, 254],[248, 245, 254],[251, 248, 254],[255, 254, 254],[255, 254, 254],[255, 254, 254],[255, 254, 252],[255, 254, 252],[255, 254, 252],[254, 254, 252],[249, 253, 255],[249, 253, 255],[249, 253, 255],[251, 254, 255],[252, 255, 255],[252, 255, 255],[252, 255, 255],[252, 254, 253],[252, 254, 253],[252, 254, 253],[253, 254, 254],[252, 253, 255],[252, 253, 255],[252, 253, 255],[253, 254, 251],[254, 255, 250],[254, 255, 250],[254, 255, 251],[255, 254, 255],[255, 254, 255],[255, 254, 255],[254, 253, 255],[253, 252, 255],[253, 252, 255],[253, 252, 255],[255, 255, 252],[255, 255, 252],[255, 255, 252],[255, 255, 253],[255, 255, 254],[255, 255, 254],[255, 255, 254],[251, 251, 255],[250, 250, 255],[250, 250, 255],[250, 250, 255],[248, 248, 253],[248, 248, 253],[248, 248, 253],[245, 245, 250],[242, 242, 246],[242, 242, 246],[242, 242, 246],[238, 238, 240],[238, 238, 240],[238, 238, 240],[234, 234, 236],[225, 225, 227],[225, 225, 227],[225, 225, 227],[217, 217, 219],[213, 213, 215],[213, 213, 215],[212, 212, 214],[204, 204, 206],[204, 204, 206],[204, 204, 206],[197, 197, 199],[191, 191, 193],[191, 191, 193],[191, 191, 193],[183, 183, 185],[182, 182, 184],[182, 182, 184],[179, 179, 181],[172, 172, 174],[172, 172, 174],[172, 172, 174],[168, 167, 170],[166, 165, 168],[166, 165, 168],[165, 164, 168],[155, 155, 158],[155, 155, 158],[155, 155, 158],[151, 151, 154],[145, 146, 150],[145, 146, 150],[145, 146, 150],[136, 137, 141],[135, 136, 140],[135, 136, 140],[132, 133, 137],[123, 124, 128],[123, 124, 128],[123, 124, 128],[115, 114, 120],[110, 108, 114],[110, 108, 114],[110, 109, 114],[111, 110, 114],[111, 110, 114],[111, 110, 114],[112, 108, 113],[112, 107, 111],[112, 107, 111],[112, 107, 111],[113,  95, 100],[113,  92,  97],[113,  92,  97],[113,  91,  96],[114,  87,  93],[114,  87,  93],[114,  87,  93],[115,  83,  89],[116,  81,  87],[116,  81,  87],[116,  81,  87],[116,  76,  81],[116,  76,  81],[116,  76,  81],[116,  74,  79],[116,  72,  74],[116,  72,  74],[116,  72,  74],[118,  68,  69],[118,  67,  68],[118,  67,  68],[119,  66,  67],[121,  60,  62],[121,  60,  62],[121,  60,  62],[123,  57,  60],[124,  54,  57],[124,  54,  57],[124,  54,  57],[126,  50,  51],[126,  50,  51],[126,  50,  51],[125,  47,  48],[123,  43,  43],[123,  43,  43],[123,  43,  43],[123,  38,  39],[123,  37,  38],[123,  37,  38],[123,  36,  37],[123,  33,  35],[123,  33,  35],[123,  33,  35],[122,  32,  32],[121,  31,  30],[121,  31,  30],[121,  31,  30],[124,  33,  32],[124,  33,  32],[124,  33,  32],[126,  33,  30],[130,  33,  26],[130,  33,  26],[130,  33,  26],[138,  37,  24],[140,  39,  24],[140,  39,  24],[141,  40,  24],[139,  43,  22],[139,  43,  22],[139,  43,  22],[137,  43,  20],[135,  42,  18],[135,  42,  18],[135,  42,  18],[137,  46,  17],[137,  46,  17],[137,  46,  17],[138,  48,  17],[141,  51,  17],[141,  51,  17],[141,  51,  17],[143,  53,  15],[143,  54,  14],[143,  54,  14],[144,  54,  13],[144,  52,   7],[144,  52,   7],[144,  52,   7],[147,  55,   9],[151,  58,  11],[151,  58,  11],[151,  58,  11],[156,  60,  12],[157,  61,  12],[157,  61,  12],[157,  61,  11],[158,  62,  10],[158,  62,  10],[158,  62,  10],[159,  64,  11],[160,  65,  11],[160,  65,  11],[159,  65,  11],[156,  62,   1],[156,  62,   1],[156,  62,   1],[157,  62,   0],[158,  62,   0],[158,  62,   0],[158,  62,   0],[169,  79,  18],[171,  81,  21],[171,  81,  21],[173,  86,  21],[180,  99,  20],[180,  99,  20],[180,  99,  20],[177, 104,  28],[175, 108,  33],[175, 108,  33],[176, 108,  33],[185, 118,  41],[185, 118,  41],[185, 118,  41],[189, 119,  46],[194, 120,  52],[194, 120,  52],[194, 120,  52],[197, 133,  61],[198, 136,  63],[198, 136,  63],[197, 139,  64],[196, 147,  70],[196, 147,  70],[196, 147,  70],[199, 153,  73],[200, 157,  75],[200, 157,  75],[200, 157,  75],[210, 168,  86],[210, 168,  86],[210, 168,  86],[214, 172,  89],[221, 178,  96],[221, 178,  96],[221, 178,  96],[220, 182,  99],[219, 183,  99],[219, 183,  99],[220, 185, 101],[224, 195, 108],[224, 195, 108],[224, 195, 108],[223, 200, 115],[222, 204, 121],[222, 204, 121],[222, 204, 121],[212, 205, 121],[212, 205, 121],[212, 205, 121],[212, 206, 122],[211, 209, 124],[211, 209, 124],[211, 209, 124],[199, 203, 114],[195, 201, 111],[195, 201, 111],[193, 200, 111],[180, 192, 111],[180, 192, 111],[180, 192, 111],[174, 191, 109],[168, 189, 107],[168, 189, 107],[168, 189, 107],[147, 179,  89],[146, 178,  88],[146, 178,  88],[143, 177,  89],[137, 175,  93],[137, 175,  93],[137, 175,  93],[123, 172,  83],[118, 171,  79],[118, 171,  79],[116, 170,  78],[105, 163,  75],[105, 163,  75],[105, 163,  75],[ 97, 159,  74],[ 89, 156,  73],[ 89, 156,  73],[ 89, 156,  73],[ 74, 150,  68],[ 73, 150,  67],[ 73, 150,  67],[ 67, 148,  64],[ 55, 142,  58],[ 55, 142,  58],[ 55, 142,  58],[ 47, 139,  56],[ 44, 137,  55],[ 44, 137,  55],[ 42, 136,  54],[ 31, 126,  49],[ 31, 126,  49],[ 31, 126,  49],[ 26, 121,  47],[ 22, 117,  44],[ 22, 117,  44],[ 22, 117,  44],[ 15, 113,  45],[ 14, 113,  45],[ 14, 113,  45],[ 14, 113,  46],[ 16, 115,  50],[ 16, 115,  50],[ 16, 115,  50],[ 15, 115,  51],[ 15, 115,  51],[ 15, 115,  51],[ 15, 115,  51],[ 12, 113,  53],[ 12, 113,  53],[ 12, 113,  53],[ 11, 113,  54],[ 10, 112,  56],[ 10, 112,  56],[ 10, 112,  56],[ 11, 111,  59],[ 11, 111,  59],[ 11, 111,  59],[ 10, 111,  59],[  9, 109,  59],[  9, 109,  59],[  9, 109,  59],[  8, 106,  58],[  7, 105,  58],[  7, 105,  58],[  7, 105,  58],[ 13, 108,  63],[ 13, 108,  63],[ 13, 108,  63],[ 11, 107,  63],[  8, 105,  62],[  8, 105,  62],[  8, 105,  62],[  2, 103,  61],[  0, 102,  60],[  0, 102,  60],[  0,  99,  60],[  1,  92,  61],[  1,  92,  61],[  1,  92,  61],[  6, 102,  72],[  9, 108,  79],[  9, 108,  79],[  9, 108,  79]])

# Чорно-білий градієнт
bw_gradient = np.array([[i, i, i] for i in range(256)])

custom_gradient = None  # Змінна для зберігання власного градієнта
map_filename = None  # Змінна для зберігання назви файлу карти

combined_pixels = None  # Глобальна змінна для збереження об'єднаних пікселів

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

# Фільтрація пікселів
def filter_pixel(pixel):
    filter_black = filter_black_var.get()
    filter_white = filter_white_var.get()
    filter_transparent = filter_transparent_var.get()

    if filter_white and np.all(pixel[:3] == [255, 255, 255]):  # Білий піксель (RGB: 255, 255, 255)
        return True
    if filter_black and np.all(pixel[:3] == [0, 0, 0]):  # Чорний піксель (RGB: 0, 0, 0)
        return True
    if filter_transparent and len(pixel) == 4 and pixel[3] == 0:  # Прозорий піксель (альфа канал 0)
        return True
    return False

# Функція для завантаження користувацької фізичної карти
def upload_custom_map():
    global combined_pixels, map_filename
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.png")])
    if file_path:
        try:
            img_tile = Image.open(file_path)
            combined_pixels = np.array(img_tile)
            img_tile_resized = img_tile.resize((300, 300))
            img_tk = ImageTk.PhotoImage(img_tile_resized)
            combined_image_label.config(image=img_tk)
            combined_image_label.image = img_tk
            map_filename = os.path.splitext(os.path.basename(file_path))[0]  # Отримуємо назву файлу без розширення
        except Exception as e:
            messagebox.showerror("Помилка", f"Не вдалося завантажити зображення: {str(e)}")

# Функція для завантаження користувацького градієнту
def upload_custom_gradient():
    global custom_gradient
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.png")])
    if file_path:
        try:
            img = Image.open(file_path).convert("RGB")
            column = 5  # Стовпчик, який використовуватимемо для витягування градієнту
            width, height = img.size
            colors = []

            for y in range(height):
                r, g, b = img.getpixel((column, y))
                colors.append([r, g, b])

            custom_gradient = np.array(colors, dtype=np.uint8)
            messagebox.showinfo("Успіх", "Користувацький градієнт завантажено!")
        except Exception as e:
            messagebox.showerror("Помилка", f"Не вдалося завантажити зображення градієнта: {str(e)}")

# Основна функція для створення 3D моделі та STL з використанням об'єднаних пікселів
def create_3d_model():
    global combined_pixels
    try:
        step = int(step_entry.get())  # Мін: 1, Макс: 100
    except ValueError:
        messagebox.showerror("Помилка", "Введіть правильне число для кроку пікселів.")
        return

    if combined_pixels is None:
        messagebox.showerror("Помилка", "Спершу завантажте власну карту!")
        return

    platform_thickness = float(platform_entry.get())  # Мін: 0.1, Макс: 10
    height_scale = float(height_entry.get())  # Мін: 0.1, Макс: 10
    apply_height_filter = filter_var.get()

    # Вибір градієнта для обробки
    if gradient_var.get() == "RGB":
        selected_gradient = rgb_gradient
    elif gradient_var.get() == "Чорно-білий":
        selected_gradient = bw_gradient
    else:
        if custom_gradient is not None:
            selected_gradient = custom_gradient
        else:
            messagebox.showerror("Помилка", "Будь ласка, завантажте користувацький градієнт!")
            return

    gradient_indices = np.zeros((combined_pixels.shape[0] // step, combined_pixels.shape[1] // step), dtype=int)

    for i in range(0, combined_pixels.shape[0], step):
        if i // step >= gradient_indices.shape[0]:
            break
        for j in range(0, combined_pixels.shape[1], step):
            if j // step >= gradient_indices.shape[1]:
                break
            pixel = combined_pixels[i, j]
            if filter_pixel(pixel):
                continue

            distances = np.apply_along_axis(lambda color: np.linalg.norm(pixel[:3] - color), 1, selected_gradient)
            gradient_indices[i // step, j // step] = np.argmin(distances)

    height, width = gradient_indices.shape

    # Інвертування висоти, якщо вибрано
    z = np.max(gradient_indices) - gradient_indices if invert_var.get() else gradient_indices
    if apply_height_filter == 1:
        z[z > 150] = 0
    z = z * height_scale

    vertices = []
    faces = []

    # Додаємо рельєф до моделі
    for i in range(height - 1):
        for j in range(width - 1):
            v1 = [i, j, z[i, j] + platform_thickness]
            v2 = [i + 1, j, z[i + 1, j] + platform_thickness]
            v3 = [i, j + 1, z[i, j + 1] + platform_thickness]
            v4 = [i + 1, j + 1, z[i + 1, j + 1] + platform_thickness]

            add_triangles(v1, v2, v3, v4, vertices, faces)

    # Додаємо платформу
    for i in range(height - 1):
        for j in range(width - 1):
            v1 = [i, j, 0]
            v2 = [i + 1, j, 0]
            v3 = [i, j + 1, 0]
            v4 = [i + 1, j + 1, 0]

            add_triangles(v1, v2, v3, v4, vertices, faces)

    # Додаємо стінки
    for i in range(height - 1):
        v1 = [i, 0, 0]
        v2 = [i + 1, 0, 0]
        v3 = [i, 0, z[i, 0] + platform_thickness]
        v4 = [i + 1, 0, z[i + 1, 0] + platform_thickness]
        add_triangles(v1, v2, v3, v4, vertices, faces)

        v1 = [i, width - 1, 0]
        v2 = [i + 1, width - 1, 0]
        v3 = [i, width - 1, z[i, width - 1] + platform_thickness]
        v4 = [i + 1, width - 1, z[i + 1, width - 1] + platform_thickness]
        add_triangles(v1, v2, v3, v4, vertices, faces)

    for j in range(width - 1):
        v1 = [0, j, 0]
        v2 = [0, j + 1, 0]
        v3 = [0, j, z[0, j] + platform_thickness]
        v4 = [0, j + 1, z[0, j + 1] + platform_thickness]
        add_triangles(v1, v2, v3, v4, vertices, faces)

        v1 = [height - 1, j, 0]
        v2 = [height - 1, j + 1, 0]
        v3 = [height - 1, j, z[height - 1, j] + platform_thickness]
        v4 = [height - 1, j + 1, z[height - 1, j + 1] + platform_thickness]
        add_triangles(v1, v2, v3, v4, vertices, faces)

    vertices = np.array(vertices)
    faces = np.array(faces)

    terrain = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
    for i, face in enumerate(faces):
        for j in range(3):
            terrain.vectors[i][j] = vertices[face[j], :]

    # Зберігаємо STL з ім'ям, відповідним до файлу карти
    stl_filename = f"{map_filename}.stl" if map_filename else "terrain.stl"
    terrain.save(stl_filename)
    messagebox.showinfo("Успіх", f"STL файл збережено як '{stl_filename}'.")
    os.startfile(stl_filename)

# Функція для показу/приховування розділу "Додатково"
def toggle_additional():
    if additional_frame.winfo_ismapped():
        additional_frame.grid_remove()
    else:
        additional_frame.grid()

def upload_test_map():
    global combined_pixels, map_filename
    response_tile = requests.get("https://gisrsstudy.com/wp-content/uploads/2020/03/DEM-data.jpg")
    if response_tile.status_code == 200:
        img_tile = Image.open(BytesIO(response_tile.content)).convert('RGB')
    combined_pixels = np.array(img_tile)
    img_tile_resized = img_tile.resize((300, 300))
    img_tk = ImageTk.PhotoImage(img_tile_resized)
    combined_image_label.config(image=img_tk)
    combined_image_label.image = img_tk
    map_filename = "Тестова картинка"

# Створюємо інтерфейс на Tkinter
root = tk.Tk()
root.title("3D модель рельєфу")

container = tk.Frame(root)
container.grid(row=0, column=0, padx=10, pady=10)

tk.Button(container, text="Завантажити тестову карту", command=upload_test_map).grid(row=0, column=0, padx=10, pady=10)

# Кнопка для завантаження власної карти
tk.Button(container, text="Завантажити власну карту", command=upload_custom_map).grid(row=1, column=0)

# Поле для зображення об'єднаної карти
combined_image_label = tk.Label(container)
combined_image_label.grid(row=2, column=0)

# Кнопка для показу/приховування розділу "Додатково"
toggle_button = tk.Button(root, text="Додатково ▼", command=toggle_additional)
toggle_button.grid(row=3, column=0, padx=10, pady=10)

# Додаємо розділ "Додатково"
additional_frame = tk.LabelFrame(root, text="Додатково", padx=10, pady=10)
additional_frame.grid(row=2, column=0, padx=10, pady=10)
additional_frame.grid_remove()  # Початково приховуємо

tk.Label(additional_frame, text="Крок пікселів (1-100):").grid(row=0, column=0, sticky=tk.W)
step_entry = tk.Entry(additional_frame)
step_entry.grid(row=0, column=1)
step_entry.insert(0, "3")

tk.Label(additional_frame, text="Товщина платформи (0.1-10):").grid(row=1, column=0, sticky=tk.W)
platform_entry = tk.Entry(additional_frame)
platform_entry.grid(row=1, column=1)
platform_entry.insert(0, "1")

tk.Label(additional_frame, text="Масштаб висоти (0.1-10):").grid(row=2, column=0, sticky=tk.W)
height_entry = tk.Entry(additional_frame)
height_entry.grid(row=2, column=1)
height_entry.insert(0, "0.1")

filter_var = tk.IntVar(value=0)  # Створюємо змінну, яка за замовчуванням має значення 1 (відмічений стан)
tk.Checkbutton(additional_frame, text="Застосувати фільтр висоти", variable=filter_var).grid(row=3, columnspan=2)

# Додаємо перемикачі для фільтрації білого, чорного і прозорого
filter_black_var = tk.IntVar(value=0)
tk.Checkbutton(additional_frame, text="Фільтрувати чорний", variable=filter_black_var).grid(row=4, columnspan=2)

filter_white_var = tk.IntVar(value=0)
tk.Checkbutton(additional_frame, text="Фільтрувати білий", variable=filter_white_var).grid(row=5, columnspan=2)

filter_transparent_var = tk.IntVar(value=0)
tk.Checkbutton(additional_frame, text="Фільтрувати прозорий", variable=filter_transparent_var).grid(row=6, columnspan=2)

# Додаємо вибір градієнта
tk.Label(additional_frame, text="Тип градієнта:").grid(row=7, column=0, sticky=tk.W)
gradient_var = tk.StringVar(value="Чорно-білий")
gradient_menu = tk.OptionMenu(additional_frame, gradient_var, "RGB", "Чорно-білий", "Користувацький")
gradient_menu.grid(row=7, column=1)

# Кнопка для завантаження користувацького градієнта
tk.Button(additional_frame, text="Завантажити градієнт", command=upload_custom_gradient).grid(row=8, columnspan=2)

# Додаємо перемикач для інвертування
invert_var = tk.IntVar(value=0)
tk.Checkbutton(additional_frame, text="Інвертувати висоту", variable=invert_var).grid(row=9, columnspan=2)

# Кнопка для створення 3D моделі
tk.Button(container, text="Створити 3D модель", command=create_3d_model).grid(row=5, column=0)

root.mainloop()
