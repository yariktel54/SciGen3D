import os
import requests
from PIL import Image, ImageTk
import webbrowser
from io import BytesIO
import numpy as np
from stl import mesh
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

# Глобальні змінні
combined_pixels = None
map_filename = None
current_service = "SRTM 90"  # Змінна для зберігання обраного сервісу (SRTM 30 або SRTM 90)
rgb_gradient = np.array([[248, 245, 254],[248, 245, 254],[248, 245, 254],[251, 248, 254],[255, 254, 254],[255, 254, 254],[255, 254, 254],[255, 254, 252],[255, 254, 252],[255, 254, 252],[254, 254, 252],[249, 253, 255],[249, 253, 255],[249, 253, 255],[251, 254, 255],[252, 255, 255],[252, 255, 255],[252, 255, 255],[252, 254, 253],[252, 254, 253],[252, 254, 253],[253, 254, 254],[252, 253, 255],[252, 253, 255],[252, 253, 255],[253, 254, 251],[254, 255, 250],[254, 255, 250],[254, 255, 251],[255, 254, 255],[255, 254, 255],[255, 254, 255],[254, 253, 255],[253, 252, 255],[253, 252, 255],[253, 252, 255],[255, 255, 252],[255, 255, 252],[255, 255, 252],[255, 255, 253],[255, 255, 254],[255, 255, 254],[255, 255, 254],[251, 251, 255],[250, 250, 255],[250, 250, 255],[250, 250, 255],[248, 248, 253],[248, 248, 253],[248, 248, 253],[245, 245, 250],[242, 242, 246],[242, 242, 246],[242, 242, 246],[238, 238, 240],[238, 238, 240],[238, 238, 240],[234, 234, 236],[225, 225, 227],[225, 225, 227],[225, 225, 227],[217, 217, 219],[213, 213, 215],[213, 213, 215],[212, 212, 214],[204, 204, 206],[204, 204, 206],[204, 204, 206],[197, 197, 199],[191, 191, 193],[191, 191, 193],[191, 191, 193],[183, 183, 185],[182, 182, 184],[182, 182, 184],[179, 179, 181],[172, 172, 174],[172, 172, 174],[172, 172, 174],[168, 167, 170],[166, 165, 168],[166, 165, 168],[165, 164, 168],[155, 155, 158],[155, 155, 158],[155, 155, 158],[151, 151, 154],[145, 146, 150],[145, 146, 150],[145, 146, 150],[136, 137, 141],[135, 136, 140],[135, 136, 140],[132, 133, 137],[123, 124, 128],[123, 124, 128],[123, 124, 128],[115, 114, 120],[110, 108, 114],[110, 108, 114],[110, 109, 114],[111, 110, 114],[111, 110, 114],[111, 110, 114],[112, 108, 113],[112, 107, 111],[112, 107, 111],[112, 107, 111],[113,  95, 100],[113,  92,  97],[113,  92,  97],[113,  91,  96],[114,  87,  93],[114,  87,  93],[114,  87,  93],[115,  83,  89],[116,  81,  87],[116,  81,  87],[116,  81,  87],[116,  76,  81],[116,  76,  81],[116,  76,  81],[116,  74,  79],[116,  72,  74],[116,  72,  74],[116,  72,  74],[118,  68,  69],[118,  67,  68],[118,  67,  68],[119,  66,  67],[121,  60,  62],[121,  60,  62],[121,  60,  62],[123,  57,  60],[124,  54,  57],[124,  54,  57],[124,  54,  57],[126,  50,  51],[126,  50,  51],[126,  50,  51],[125,  47,  48],[123,  43,  43],[123,  43,  43],[123,  43,  43],[123,  38,  39],[123,  37,  38],[123,  37,  38],[123,  36,  37],[123,  33,  35],[123,  33,  35],[123,  33,  35],[122,  32,  32],[121,  31,  30],[121,  31,  30],[121,  31,  30],[124,  33,  32],[124,  33,  32],[124,  33,  32],[126,  33,  30],[130,  33,  26],[130,  33,  26],[130,  33,  26],[138,  37,  24],[140,  39,  24],[140,  39,  24],[141,  40,  24],[139,  43,  22],[139,  43,  22],[139,  43,  22],[137,  43,  20],[135,  42,  18],[135,  42,  18],[135,  42,  18],[137,  46,  17],[137,  46,  17],[137,  46,  17],[138,  48,  17],[141,  51,  17],[141,  51,  17],[141,  51,  17],[143,  53,  15],[143,  54,  14],[143,  54,  14],[144,  54,  13],[144,  52,   7],[144,  52,   7],[144,  52,   7],[147,  55,   9],[151,  58,  11],[151,  58,  11],[151,  58,  11],[156,  60,  12],[157,  61,  12],[157,  61,  12],[157,  61,  11],[158,  62,  10],[158,  62,  10],[158,  62,  10],[159,  64,  11],[160,  65,  11],[160,  65,  11],[159,  65,  11],[156,  62,   1],[156,  62,   1],[156,  62,   1],[157,  62,   0],[158,  62,   0],[158,  62,   0],[158,  62,   0],[169,  79,  18],[171,  81,  21],[171,  81,  21],[173,  86,  21],[180,  99,  20],[180,  99,  20],[180,  99,  20],[177, 104,  28],[175, 108,  33],[175, 108,  33],[176, 108,  33],[185, 118,  41],[185, 118,  41],[185, 118,  41],[189, 119,  46],[194, 120,  52],[194, 120,  52],[194, 120,  52],[197, 133,  61],[198, 136,  63],[198, 136,  63],[197, 139,  64],[196, 147,  70],[196, 147,  70],[196, 147,  70],[199, 153,  73],[200, 157,  75],[200, 157,  75],[200, 157,  75],[210, 168,  86],[210, 168,  86],[210, 168,  86],[214, 172,  89],[221, 178,  96],[221, 178,  96],[221, 178,  96],[220, 182,  99],[219, 183,  99],[219, 183,  99],[220, 185, 101],[224, 195, 108],[224, 195, 108],[224, 195, 108],[223, 200, 115],[222, 204, 121],[222, 204, 121],[222, 204, 121],[212, 205, 121],[212, 205, 121],[212, 205, 121],[212, 206, 122],[211, 209, 124],[211, 209, 124],[211, 209, 124],[199, 203, 114],[195, 201, 111],[195, 201, 111],[193, 200, 111],[180, 192, 111],[180, 192, 111],[180, 192, 111],[174, 191, 109],[168, 189, 107],[168, 189, 107],[168, 189, 107],[147, 179,  89],[146, 178,  88],[146, 178,  88],[143, 177,  89],[137, 175,  93],[137, 175,  93],[137, 175,  93],[123, 172,  83],[118, 171,  79],[118, 171,  79],[116, 170,  78],[105, 163,  75],[105, 163,  75],[105, 163,  75],[ 97, 159,  74],[ 89, 156,  73],[ 89, 156,  73],[ 89, 156,  73],[ 74, 150,  68],[ 73, 150,  67],[ 73, 150,  67],[ 67, 148,  64],[ 55, 142,  58],[ 55, 142,  58],[ 55, 142,  58],[ 47, 139,  56],[ 44, 137,  55],[ 44, 137,  55],[ 42, 136,  54],[ 31, 126,  49],[ 31, 126,  49],[ 31, 126,  49],[ 26, 121,  47],[ 22, 117,  44],[ 22, 117,  44],[ 22, 117,  44],[ 15, 113,  45],[ 14, 113,  45],[ 14, 113,  45],[ 14, 113,  46],[ 16, 115,  50],[ 16, 115,  50],[ 16, 115,  50],[ 15, 115,  51],[ 15, 115,  51],[ 15, 115,  51],[ 15, 115,  51],[ 12, 113,  53],[ 12, 113,  53],[ 12, 113,  53],[ 11, 113,  54],[ 10, 112,  56],[ 10, 112,  56],[ 10, 112,  56],[ 11, 111,  59],[ 11, 111,  59],[ 11, 111,  59],[ 10, 111,  59],[  9, 109,  59],[  9, 109,  59],[  9, 109,  59],[  8, 106,  58],[  7, 105,  58],[  7, 105,  58],[  7, 105,  58],[ 13, 108,  63],[ 13, 108,  63],[ 13, 108,  63],[ 11, 107,  63],[  8, 105,  62],[  8, 105,  62],[  8, 105,  62],[  2, 103,  61],[  0, 102,  60],[  0, 102,  60],[  0,  99,  60],[  1,  92,  61],[  1,  92,  61],[  1,  92,  61],[  6, 102,  72],[  9, 108,  79],[  9, 108,  79],[  9, 108,  79]])
# Функція для створення чорного тайлу (якщо тайл не завантажується)
def generate_black_tile(size):
    return Image.new('RGB', (size, size), (0, 0, 0))

# Функція для створення трикутників
def add_triangles(v1, v2, v3, v4, vertices, faces):
    vertices.append(v1)
    vertices.append(v2)
    vertices.append(v3)
    faces.append([len(vertices) - 3, len(vertices) - 2, len(vertices) - 1])

    vertices.append(v2)
    vertices.append(v3)
    vertices.append(v4)
    faces.append([len(vertices) - 3, len(vertices) - 2, len(vertices) - 1])

# Функція для завантаження тайлів з https://e4ftl01.cr.usgs.gov (SRTM 30)
def merge_tiles_srtm_30(tile_size):
    global combined_pixels, current_service
    current_service = "SRTM 30"  # Зберігаємо вибір сервісу
    try:
        coordinates = coordinates_entry.get()
        lat, lon = map(float, coordinates.split(','))
    except ValueError:
        messagebox.showerror("Помилка", "Неправильний формат введення координат. Введіть широту та довготу через кому.")
        return

    lat_prefix = 'N' if lat >= 0 else 'S'
    lon_prefix = 'E' if lon >= 0 else 'W'

    lat_int = abs(int(lat))
    lon_int = abs(int(lon))

    tiles = []
    for i in range(tile_size):
        row_tiles = []
        for j in range(tile_size):
            lat_tile = lat_int - i
            lon_tile = lon_int + j

            url_tile = f"https://e4ftl01.cr.usgs.gov/MEASURES/SRTMGL1.003/2000.02.11/{lat_prefix}{lat_tile:02d}{lon_prefix}{lon_tile:03d}.SRTMGL1.2.jpg"
            response_tile = requests.get(url_tile)
            if response_tile.status_code == 200:
                img_tile = Image.open(BytesIO(response_tile.content)).convert('RGB')
                row_tiles.append(np.array(img_tile))
            else:
                black_tile = generate_black_tile(3601)
                row_tiles.append(np.array(black_tile))
        tiles.append(row_tiles)

    width, height = tiles[0][0].shape[:2]
    combined_img = Image.new('RGB', (width * tile_size, height * tile_size))

    combined_pixels = np.zeros((height * tile_size, width * tile_size, 3), dtype=np.uint8)

    for i, row_tiles in enumerate(tiles):
        for j, img_tile in enumerate(row_tiles):
            img_tile = Image.fromarray(img_tile)
            combined_img.paste(img_tile, (j * width, i * height))

            combined_pixels[i * height:(i + 1) * height, j * width:(j + 1) * width] = np.array(img_tile)

    # Масштабування для перегляду
    combined_img = combined_img.resize((300, 300))
    combined_img_tk = ImageTk.PhotoImage(combined_img)

    combined_image_label.config(image=combined_img_tk)
    combined_image_label.image = combined_img_tk

    messagebox.showinfo("Успіх", "Тайли успішно завантажені (SRTM 30)!")


# Функція для завантаження тайлів з http://srtm.csi.cgiar.org (SRTM 90)
def merge_tiles_srtm_90(tile_size):
    global combined_pixels, current_service
    current_service = "SRTM 90"  # Зберігаємо вибір сервісу
    try:
        coordinates = coordinates_entry.get()
        lat, lon = map(float, coordinates.split(','))
    except ValueError:
        messagebox.showerror("Помилка", "Неправильний формат введення координат. Введіть широту та довготу через кому.")
        return

    # Визначення початкового тайлу на основі координат (SRTM 90 система координат)
    if lon > 0:
        x_start = int(37 + (lon / 5))
    else:
        x_start = int(37 - (lon / -5))

    if lat > 0:
        y_start = int(13 - (lat / 5))
    else:
        y_start = int(13 + (lat / -5))

    # Завантаження декількох тайлів та їх об'єднання
    tiles = []
    for i in range(tile_size):
        row_tiles = []
        for j in range(tile_size):
            x = x_start + j
            y = y_start + i
            url_tile = f"https://srtm.csi.cgiar.org/wp-content/uploads/files/image/srtm_th_{x:02d}_{y:02d}.jpg"
            response_tile = requests.get(url_tile)
            if response_tile.status_code == 200:
                img_tile = Image.open(BytesIO(response_tile.content)).convert('RGB')
                row_tiles.append(np.array(img_tile))
            else:
                black_tile = generate_black_tile(3601)
                row_tiles.append(np.array(black_tile))
        tiles.append(row_tiles)

    width, height = tiles[0][0].shape[:2]
    combined_img = Image.new('RGB', (width * tile_size, height * tile_size))

    combined_pixels = np.zeros((height * tile_size, width * tile_size, 3), dtype=np.uint8)

    for i, row_tiles in enumerate(tiles):
        for j, img_tile in enumerate(row_tiles):
            img_tile = Image.fromarray(img_tile)
            combined_img.paste(img_tile, (j * width, i * height))

            combined_pixels[i * height:(i + 1) * height, j * width:(j + 1) * width] = np.array(img_tile)

    # Масштабування для перегляду
    combined_img = combined_img.resize((300, 300))
    combined_img_tk = ImageTk.PhotoImage(combined_img)

    combined_image_label.config(image=combined_img_tk)
    combined_image_label.image = combined_img_tk

    messagebox.showinfo("Успіх", "Тайли успішно завантажені (SRTM 90)!")


# Функція для завантаження користувацької карти
def upload_custom_map():
    global combined_pixels, map_filename, current_service
    # Оновлюємо current_service на основі обраного сервісу через перемикач
    if service_var.get() == 1:
        current_service = "SRTM 30"
    elif service_var.get() == 2:
        current_service = "SRTM 90"
    
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.png")])
    if file_path:
        try:
            img_tile = Image.open(file_path)
            combined_pixels = np.array(img_tile.convert('RGB'))
            img_tile_resized = img_tile.resize((300, 300))
            img_tk = ImageTk.PhotoImage(img_tile_resized)
            combined_image_label.config(image=img_tk)
            combined_image_label.image = img_tk
            map_filename = os.path.splitext(os.path.basename(file_path))[0]

            # Виводимо повідомлення, що карта завантажена
            messagebox.showinfo("Успіх", f"Карта '{map_filename}' успішно завантажена! Режим: {current_service}")

        except Exception as e:
            messagebox.showerror("Помилка", f"Не вдалося завантажити зображення: {str(e)}")

def create_3d_model():
    global combined_pixels, current_service
    try:
        step = int(step_entry.get())  # Мін: 1, Макс: 100
    except ValueError:
        messagebox.showerror("Помилка", "Введіть правильне число для кроку пікселів.")
        return

    if combined_pixels is None:
        messagebox.showerror("Помилка", "Спершу завантажте тайли або власну карту!")
        return

    if current_service is None:
        messagebox.showerror("Помилка", "Виберіть режим (SRTM 30 або SRTM 90) перед генерацією 3D моделі.")
        return

    platform_thickness = float(platform_entry.get())  # Мін: 0.1, Макс: 10
    height_scale = float(height_entry.get())  # Мін: 0.1, Макс: 10
    invert = 1  # Отримуємо значення перемикача інвертування

    # Ініціалізуємо змінну height_map
    height_map = None

    # Різна обробка для SRTM 30 (чорно-біле) та SRTM 90 (кольорове)
    if current_service == "SRTM 30":
        # Обробка SRTM 30 (чорно-біле)
        height_map = np.mean(combined_pixels, axis=2)  # Визначаємо висоту на основі яскравості пікселів
    elif current_service == "SRTM 90":
        # Обробка SRTM 90 (кольорове)
        height_map = np.zeros((combined_pixels.shape[0], combined_pixels.shape[1]))
        for i in range(combined_pixels.shape[0]):
            for j in range(combined_pixels.shape[1]):
                pixel = combined_pixels[i, j]
                if np.all(pixel[:3] > [200, 200, 180]):  # Якщо піксель більше за [200, 200, 180]
                    height_map[i, j] = 357  # Присвоюємо значення 357
                else:
                    distances = np.linalg.norm(rgb_gradient - pixel[:3], axis=1)
                    height_map[i, j] = np.argmin(distances)

        if invert:
            height_map = np.max(height_map) - height_map  # Інвертуємо висоти

        # Фільтрація значень більше 150, встановлюючи їх як 0
        height_map[height_map > 150] = 0

    else:
        messagebox.showerror("Помилка", "Невідомий режим. Виберіть SRTM 30 або SRTM 90.")
        return

    if height_map is None:
        messagebox.showerror("Помилка", "Не вдалося обробити висотну карту.")
        return

    height, width = height_map.shape
    z = height_map * height_scale

    vertices = []
    faces = []

    # Генерація рельєфу
    for i in range(0, height - step, step):
        for j in range(0, width - step, step):
            v1 = [i, j, z[i, j] + platform_thickness]
            v2 = [i + step, j, z[i + step, j] + platform_thickness]
            v3 = [i, j + step, z[i, j + step] + platform_thickness]
            v4 = [i + step, j + step, z[i + step, j + step] + platform_thickness]

            add_triangles(v1, v2, v3, v4, vertices, faces)

    # Додаємо платформу
    for i in range(0, height - step, step):
        for j in range(0, width - step, step):
            v1 = [i, j, 0]
            v2 = [i + step, j, 0]
            v3 = [i, j + step, 0]
            v4 = [i + step, j + step, 0]

            add_triangles(v1, v2, v3, v4, vertices, faces)

    # Додаємо стінки
    # Ліва стінка
    for i in range(0, height - step, step):
        v1 = [i, 0, 0]
        v2 = [i + step, 0, 0]
        v3 = [i, 0, z[i, 0] + platform_thickness]
        v4 = [i + step, 0, z[i + step, 0] + platform_thickness]
        add_triangles(v1, v2, v3, v4, vertices, faces)

    # Права стінка
    for i in range(0, height - step, step):
        v1 = [i, width - 1, 0]
        v2 = [i + step, width - 1, 0]
        v3 = [i, width - 1, z[i, width - 1] + platform_thickness]
        v4 = [i + step, width - 1, z[i + step, width - 1] + platform_thickness]
        add_triangles(v1, v2, v3, v4, vertices, faces)

    # Нижня стінка
    for j in range(0, width - step, step):
        v1 = [0, j, 0]
        v2 = [0, j + step, 0]
        v3 = [0, j, z[0, j] + platform_thickness]
        v4 = [0, j + step, z[0, j + step] + platform_thickness]
        add_triangles(v1, v2, v3, v4, vertices, faces)

    # Верхня стінка
    for j in range(0, width - step, step):
        v1 = [height - 1, j, 0]
        v2 = [height - 1, j + step, 0]
        v3 = [height - 1, j, z[height - 1, j] + platform_thickness]
        v4 = [height - 1, j + step, z[height - 1, j + step] + platform_thickness]
        add_triangles(v1, v2, v3, v4, vertices, faces)

    vertices = np.array(vertices)
    faces = np.array(faces)

    # Створення STL-файлу
    terrain = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
    for i, face in enumerate(faces):
        for j in range(3):
            terrain.vectors[i][j] = vertices[face[j], :]

    stl_filename = f"{map_filename}.stl" if map_filename else "terrain.stl"
    terrain.save(stl_filename)
    messagebox.showinfo("Успіх", f"STL файл збережено як '{stl_filename}'.")
    os.startfile(stl_filename)

def toggle_additional():
    if additional_frame.winfo_ismapped():
        additional_frame.grid_remove()
    else:
        additional_frame.grid()

def open_google_maps():
    coordinates = coordinates_entry.get()
    base_url = "https://www.google.com/maps/"
    webbrowser.open(base_url)

# Створюємо інтерфейс на Tkinter
root = tk.Tk()
root.title("3D модель рельєфу")

container = tk.Frame(root)
container.grid(row=0, column=0, padx=10, pady=10)

# Поле для введення координат
tk.Label(container, text="Координати (широта, довгота):").grid(row=0, column=0, sticky=tk.W)
coordinates_entry = tk.Entry(container)
coordinates_entry.grid(row=0, column=1, padx=10, pady=10)
coordinates_entry.insert(0, "42.002998157718095, 18.024234089115303")


# Кнопка для завантаження тайлів на основі обраного сервісу
tk.Button(container, text="Завантажити тайли", command=lambda: merge_tiles_srtm_30(int(tile_size_entry.get())) if service_var.get() == 1 else merge_tiles_srtm_90(int(tile_size_entry.get()))).grid(row=3, columnspan=2)

# Поле для зображення об'єднаної карти
combined_image_label = tk.Label(container)
combined_image_label.grid(row=4, columnspan=2)

# Кнопка для завантаження власної карти
tk.Button(container, text="Завантажити власну карту", command=upload_custom_map).grid(row=6, columnspan=2)

# Кнопка для створення 3D моделі
tk.Button(container, text="Створити 3D модель", command=create_3d_model).grid(row=7, columnspan=2)

# Кнопка для показу/приховування додаткового блоку
toggle_button = tk.Button(container, text="Додатково ▼", command=toggle_additional)
toggle_button.grid(row=8, columnspan=2, padx=10, pady=10)

# Додатковий блок (початково прихований)
additional_frame = tk.Frame(container)
tk.Label(additional_frame, text="Крок пікселів (1-100):").grid(row=0, column=0, sticky=tk.W)
step_entry = tk.Entry(additional_frame)
step_entry.grid(row=0, column=1, padx=10, pady=10)
step_entry.insert(0, "10")

tk.Label(additional_frame, text="Товщина платформи (0.1-10):").grid(row=1, column=0, sticky=tk.W)
platform_entry = tk.Entry(additional_frame)
platform_entry.grid(row=1, column=1, padx=10, pady=10)
platform_entry.insert(0, "1")

tk.Label(additional_frame, text="Масштаб висоти (0.1-10):").grid(row=2, column=0, sticky=tk.W)
height_entry = tk.Entry(additional_frame)
height_entry.grid(row=2, column=1, padx=10, pady=10)
height_entry.insert(0, "0.1")

tk.Label(additional_frame, text="Розмір сітки тайлів (2 для 2x2, 3 для 3x3):").grid(row=3, column=0, sticky=tk.W)
tile_size_entry = tk.Entry(additional_frame)
tile_size_entry.grid(row=3, column=1, padx=10, pady=10)
tile_size_entry.insert(0, "1")

tk.Label(additional_frame, text="Виберіть сервіс для завантаження:").grid(row=4, column=0, sticky=tk.W)
service_var = tk.IntVar(value=1)  # Початково вибрано SRTM 30
tk.Radiobutton(additional_frame, text="SRTM 30 (чорно-біле)", variable=service_var, value=1).grid(row=4, column=1, sticky=tk.W)
tk.Radiobutton(additional_frame, text="SRTM 90 (кольорове)", variable=service_var, value=2).grid(row=4, column=2, sticky=tk.W)

map_button = tk.Button(container, text="Відкрити карти", command=open_google_maps)
map_button.grid(row=5, columnspan=2, padx=10, pady=10)

# Початково приховуємо додатковий блок
additional_frame.grid_remove()

root.mainloop()
