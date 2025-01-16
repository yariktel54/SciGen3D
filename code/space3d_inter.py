import os
import requests
from PIL import Image, ImageTk
from io import BytesIO
import numpy as np
from stl import mesh
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import webbrowser

# Глобальні змінні
combined_pixels = None
map_filename = None
current_service = "Black-White"
rgb_gradient = np.array([[ 62,  14,  50],[ 67,  18,  72],[ 99,  22, 104],[127,  20, 122],[144,  21, 152],[162,  25, 171],[136,  26, 182],[ 83,  27, 149],[ 29,  11, 146],[  0,   0, 202],[  0,  87, 208],[ 42, 160, 131],[ 17, 222,  30],[ 56, 193,   5],[179, 187,   0],[249, 245,   0],[245, 209,   3],[245, 164,  27],[206, 112,  25],[226,  66,  10],[244,  15,  17],[237,  55,  62],[249,  93,  97],[233, 143, 153],[227, 179, 190],[248, 206, 208],[254, 211, 223],[246, 215, 221],[235, 214, 220],[250, 238, 239]])
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

# Функція для завантаження тайлів на основі статичного списку посилань
def merge_tiles(tile_size):
    global combined_pixels, current_service
    
    selected_tile = tile_var.get()  # Отримуємо вибраний елемент зі списку
    tile_links = {
        "Phobos Mars Express HRSC DEM Global 100m": "https://astrogeology.usgs.gov/ckan/dataset/e51d60ae-0c1c-417b-aa1f-a555e66dc859/resource/8285a557-dca9-4aac-8b37-3914cfe69a10/download/phobos_me_hrsc_dem_global_2ppd_1024.jpg",
        "Moon LRO LOLA DEM 118m": "https://astrogeology.usgs.gov/ckan/dataset/8d95ec67-e637-4b48-88ed-84e1f95660fc/resource/6ce79c01-d8a2-4b54-bae1-31bf4efc6e4b/download/moon_lro_lola_global_ldem_1024.jpg",
        "Moon LRO LOLA - SELENE Kaguya TC DEM Merge 60N60S 59m": "https://astrogeology.usgs.gov/ckan/dataset/21cbb67a-ea2b-445b-8ff7-c69cae74689e/resource/5c878fad-b4c6-4822-bbbf-a8546107d01c/download/lro_lrockaguya_demmerge_60n60s_1024.jpg",
        "Mars MSL Gale Merged DEM 1m": "https://astrogeology.usgs.gov/ckan/dataset/b3d63877-8544-49bb-b0f3-532cf2c648d1/resource/a5c163e8-4e8b-4a79-839f-a1bf997af2ce/download/msl_gale_dem_mosaic_1024.jpg",
        "Charon New Horizons LORRI MVIC Global DEM 300m": "https://astrogeology.usgs.gov/ckan/dataset/f322149d-a7e0-432b-934f-dbcdf6d22800/resource/ed2aeafa-5538-40fa-8131-5b1d3792cee7/download/charon_newhorizons_global_dem_300m_jul2017_1024.jpg",
        "Pluto New Horizons LORRI - MVIC Global DEM 300m": "https://astrogeology.usgs.gov/ckan/dataset/f1332f71-8003-4a75-a330-acce6a3bf09f/resource/cc6042e5-91e6-44da-88ec-52187568870d/download/pluto_newhorizons_global_dem_300m_jul2017_1024.jpg",
        "Mars MGS MOLA - MEX HRSC Blended DEM Global 200m": "https://astrogeology.usgs.gov/ckan/dataset/6c177b5f-97af-4d70-adc3-92cf362b9890/resource/71f58b51-861b-4fe9-a096-5cb0bcf52c72/download/mars_hrsc_mola_blenddem_global_200mp_1024.jpg",
        "Enceladus Cassini Global DEM 200m Schenk": "https://astrogeology.usgs.gov/ckan/dataset/811a9e97-16f8-460d-b3aa-a8125ea3a2a5/resource/91adcdc2-fac3-4bae-8b00-ab42db8f24c2/download/enceladus_cassini_dem_global_200m_schenk2024_1024.jpg",
        "Mercury MESSENGER Global DEM 665m": "https://astrogeology.usgs.gov/ckan/dataset/75db9745-e9c5-4a6d-8dea-39f704a163cc/resource/2816dcdb-6c7c-427e-b7bb-5401e2885b0b/download/mercury_messenger_dem_global_665m_1024.jpg",
        "Lunar LRO NAC Haworth Photoclinometry DEM 1m": "https://astrogeology.usgs.gov/ckan/dataset/9f98eebc-0202-43e9-abcc-fe302867afca/resource/2ae52f42-7e41-41e4-ac0e-b6d98b6cdcf8/download/lunar_lronac_haworth_1024.jpg",
        "Mars MGS MOLA DEM 463m": "https://astrogeology.usgs.gov/ckan/dataset/83c20dbd-e2b3-4e5b-b019-f13d4fdffa38/resource/57f84b24-d56c-42dd-a34d-cf9d61a82d2c/download/mars_mgs_mola_dem_mosaic_global_1024.jpg"
    }
    try:
        url_tile = tile_links[selected_tile]
        response_tile = requests.get(url_tile)
        if response_tile.status_code == 200:
            img_tile = Image.open(BytesIO(response_tile.content)).convert('RGB')
        
        combined_pixels = np.array(img_tile)
        combined_img_resized = img_tile.resize((300, 300))
        combined_img_tk = ImageTk.PhotoImage(combined_img_resized)

        combined_image_label.config(image=combined_img_tk)
        combined_image_label.image = combined_img_tk

        messagebox.showinfo("Success", f"Map '{selected_tile}' successfully loaded!")

    except Exception as e:
        messagebox.showerror("Error", f"Failed to load map: {str(e)}")

# Функція для оновлення посилання на інформацію про тайл
def update_tile_info(*args):
    tile_info_links = {
        "Phobos Mars Express HRSC DEM Global 100m": "https://astrogeology.usgs.gov/search/map/phobos_mars_express_hrsc_dem_global_100m",
        "Moon LRO LOLA DEM 118m": "https://astrogeology.usgs.gov/search/map/moon_lro_lola_dem_118m",
        "Moon LRO LOLA - SELENE Kaguya TC DEM Merge 60N60S 59m": "https://astrogeology.usgs.gov/search/map/moon_lro_lola_selene_kaguya_tc_dem_merge_60n60s_59m",
        "Mars MSL Gale Merged DEM 1m": "https://astrogeology.usgs.gov/search/map/mars_msl_gale_merged_dem_1m",
        "Charon New Horizons LORRI MVIC Global DEM 300m": "https://astrogeology.usgs.gov/search/map/charon_new_horizons_lorri_mvic_global_dem_300m",
        "Pluto New Horizons LORRI - MVIC Global DEM 300m": "https://astrogeology.usgs.gov/search/map/pluto_new_horizons_lorri_mvic_global_dem_300m",
        "Mars MGS MOLA - MEX HRSC Blended DEM Global 200m": "https://astrogeology.usgs.gov/search/map/mars_mgs_mola_mex_hrsc_blended_dem_global_200m",
        "Enceladus Cassini Global DEM 200m Schenk": "https://astrogeology.usgs.gov/search/map/enceladus-cassini-global-dem-200m-schenk",
        "Mercury MESSENGER Global DEM 665m": "https://astrogeology.usgs.gov/search/map/mercury_messenger_global_dem_665m",
        "Lunar LRO NAC Haworth Photoclinometry DEM 1m": "https://astrogeology.usgs.gov/search/map/lunar_lro_nac_haworth_photoclinometry_dem_1m",
        "Mars MGS MOLA DEM 463m": "https://astrogeology.usgs.gov/search/map/mars_mgs_mola_dem_463m"
    }
    selected_tile = tile_var.get()
    tile_info_label.config(text=f"Card information: {tile_info_links[selected_tile]}")
    tile_info_label.bind("<Button-1>", lambda e: webbrowser.open(tile_info_links[selected_tile]))

# Функція для завантаження користувацької карти
def upload_custom_map():
    global combined_pixels, map_filename, current_service
    if service_var.get() == 1:
        current_service = "Black-White"
    elif service_var.get() == 2:
        current_service = "RGB"
    
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

            messagebox.showinfo("Success", f"Map '{map_filename}' downloaded successfully! Mode: {current_service}")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load image: {str(e)}")

# Функція для створення 3D моделі
def create_3d_model():
    global combined_pixels, current_service
    if service_var.get() == 1:
        current_service = "Black-White"
    elif service_var.get() == 2:
        current_service = "RGB"
    
    try:
        step = int(step_entry.get())  # Мін: 1, Макс: 100
    except ValueError:
        messagebox.showerror("Error", "Enter a valid number for the pixel pitch.")
        return

    if combined_pixels is None:
        messagebox.showerror("Error", "Download online or own map first!")
        return

    if current_service is None:
        messagebox.showerror("Error", "Select mode (Black-White or RGB) before generating 3D model.")
        return

    platform_thickness = float(platform_entry.get())  # Мін: 0.1, Макс: 10
    height_scale = float(height_entry.get())  # Мін: 0.1, Макс: 10
    invert = 1  # Отримуємо значення перемикача інвертування

    # Ініціалізуємо змінну height_map
    height_map = None

    # Різна обробка для Black-White (Black-White) та RGB (RGB)
    if current_service == "Black-White":
        # Обробка Black-White (Black-White)
        height_map = np.mean(combined_pixels, axis=2)  # Визначаємо висоту на основі яскравості пікселів
    elif current_service == "RGB":
        # Обробка RGB (RGB)
        height_map = np.zeros((combined_pixels.shape[0], combined_pixels.shape[1]))
        for i in range(combined_pixels.shape[0]):
            for j in range(combined_pixels.shape[1]):
                pixel = combined_pixels[i, j]
                if pixel[2] > pixel[0] and pixel[2] > pixel[1]:  # x - поріг яскравості
                    height_map[i, j] = 0
                else:
                    distances = np.linalg.norm(rgb_gradient - pixel[:3], axis=1)
                    height_map[i, j] = np.argmin(distances)
        height_map = np.max(height_map) - height_map
    else:
        messagebox.showerror("Error", "Unknown mode. Select Black-White or RGB.")
        return
    if height_map is None:
        messagebox.showerror("Error", "Failed to process height map.")
        return

    if size_var.get() == 1:
        # Збереження початкових розмірів перед масштабуванням
        original_height, original_width = height_map.shape

        # Перевірка розміру і масштабування при необхідності
        if original_height > 500 or original_width > 500:
            # Обчислення коефіцієнта масштабування для збереження пропорцій
            scale_factor = min(500 / original_height, 500 / original_width)
            
            # Новий розмір з урахуванням пропорцій
            new_height = int(original_height * scale_factor)
            new_width = int(original_width * scale_factor)

            resized_indices = np.zeros((new_height, new_width), dtype=height_map.dtype)

             # Вибір значень вручну з урахуванням коефіцієнта
            for new_i in range(new_height):
                for new_j in range(new_width):
                    # Обчислення відповідних індексів у вихідній матриці
                    old_i = int(new_i / scale_factor)
                    old_j = int(new_j / scale_factor)

                    # Присвоєння значення
                    resized_indices[new_i, new_j] = height_map[old_i, old_j]

            height_map = resized_indices

    # Оновлення значень height і width після масштабування
    height, width = height_map.shape

    try:
    # Отримуємо значення з Entry для максимального значення висоти та множника
        height_max_value = float(height_max.get())  
        height_x_val_value = float(height_x_val.get())  
    except ValueError:
        messagebox.showerror("Error", "Enter valid numbers for max height and multiplier.")
        return

    if height_enhancement_var.get() == 1: # Застосування операції до height_map
        height_map[height_map < height_max_value] *= height_x_val_value  

    z = height_map * height_scale

    faces = []
    vertices = []  # У випадку, якщо vertices також був змінений на ndarray

    # Генерація рельєфу
    for i in range(0, height - step, step):
        for j in range(0, width - step, step):
            v1 = [i, j, z[i, j] + platform_thickness]
            v2 = [i + step, j, z[min(i + step, height - 1), j] + platform_thickness]
            v3 = [i, j + step, z[i, min(j + step, width - 1)] + platform_thickness]
            v4 = [i + step, j + step, z[min(i + step, height - 1), min(j + step, width - 1)] + platform_thickness]

            # Додаємо трикутники для верхньої поверхні рельєфу
            faces.append([len(vertices), len(vertices) + 1, len(vertices) + 2])
            faces.append([len(vertices) + 1, len(vertices) + 3, len(vertices) + 2])
            vertices.extend([v1, v2, v3, v4])

    # Генерація платформи
    for i in range(0, height - step, step):
        for j in range(0, width - step, step):
            v1 = [i, j, 0]
            v2 = [i + step, j, 0]
            v3 = [i, min(j + step, width - 1), 0]
            v4 = [i + step, min(j + step, width - 1), 0]

            faces.append([len(vertices), len(vertices) + 2, len(vertices) + 1])
            faces.append([len(vertices) + 1, len(vertices) + 2, len(vertices) + 3])
            vertices.extend([v1, v2, v3, v4])

    # Генерація стінок
   # Додаємо стінки платформи
    for i in range(0, height - step, step):
        # Ліва стінка
        v1 = [i, 0, 0]
        v2 = [min(i + step, height - 1), 0, 0]
        v3 = [i, 0, z[i, 0] + platform_thickness]
        v4 = [min(i + step, height - 1), 0, z[min(i + step, height - 1), 0] + platform_thickness]

        faces.append([len(vertices), len(vertices) + 1, len(vertices) + 2])
        faces.append([len(vertices) + 1, len(vertices) + 3, len(vertices) + 2])
        vertices.extend([v1, v2, v3, v4])

        # Права стінка
        v1 = [i, width - 1, 0]
        v2 = [min(i + step, height - 1), width - 1, 0]
        v3 = [i, width - 1, z[i, width - 1] + platform_thickness]
        v4 = [min(i + step, height - 1), width - 1, z[min(i + step, height - 1), width - 1] + platform_thickness]

        faces.append([len(vertices), len(vertices) + 2, len(vertices) + 1])
        faces.append([len(vertices) + 2, len(vertices) + 3, len(vertices) + 1])
        vertices.extend([v1, v2, v3, v4])

    for j in range(0, width - step, step):
        # Нижня стінка
        v1 = [0, j, 0]
        v2 = [0, min(j + step, width - 1), 0]
        v3 = [0, j, z[0, j] + platform_thickness]
        v4 = [0, min(j + step, width - 1), z[0, min(j + step, width - 1)] + platform_thickness]

        faces.append([len(vertices), len(vertices) + 2, len(vertices) + 1])
        faces.append([len(vertices) + 2, len(vertices) + 3, len(vertices) + 1])
        vertices.extend([v1, v2, v3, v4])

        # Верхня стінка
        v1 = [height - 1, j, 0]
        v2 = [height - 1, min(j + step, width - 1), 0]
        v3 = [height - 1, j, z[height - 1, j] + platform_thickness]
        v4 = [height - 1, min(j + step, width - 1), z[height - 1, min(j + step, width - 1)] + platform_thickness]

        faces.append([len(vertices), len(vertices) + 1, len(vertices) + 2])
        faces.append([len(vertices) + 1, len(vertices) + 3, len(vertices) + 2])
        vertices.extend([v1, v2, v3, v4])


    # Конвертуємо у numpy.ndarray перед створенням STL-файлу
    vertices = np.array(vertices)
    faces = np.array(faces)

    # Створення STL-файлу
    terrain = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
    for i, face in enumerate(faces):
        for j in range(3):
            terrain.vectors[i][j] = vertices[face[j], :]

    stl_filename = f"{map_filename}.stl" if map_filename else "terrain.stl"
    terrain.save(stl_filename)
    messagebox.showinfo("Success", f"STL file saved as '{stl_filename}'.")
    os.startfile(stl_filename)


def toggle_additional():
    if additional_frame.winfo_ismapped():
        additional_frame.grid_remove()
    else:
        additional_frame.grid()

# Створюємо інтерфейс на Tkinter
root = tk.Tk()
root.title("3D model of the relief of the planets")

container = tk.Frame(root)
container.grid(row=0, column=0, padx=10, pady=10)

# Вибір статичного тайлу
tk.Label(container, text="Choose a card:").grid(row=0, column=0, sticky=tk.W)
tile_var = tk.StringVar()
tile_menu = ttk.Combobox(container, textvariable=tile_var)
tile_menu['values'] = ("Phobos Mars Express HRSC DEM Global 100m","Moon LRO LOLA DEM 118m","Moon LRO LOLA - SELENE Kaguya TC DEM Merge 60N60S 59m","Mars MSL Gale Merged DEM 1m","Charon New Horizons LORRI MVIC Global DEM 300m","Pluto New Horizons LORRI - MVIC Global DEM 300m","Mars MGS MOLA - MEX HRSC Blended DEM Global 200m","Enceladus Cassini Global DEM 200m Schenk","Mercury MESSENGER Global DEM 665m","Lunar LRO NAC Haworth Photoclinometry DEM 1m","Mars MGS MOLA DEM 463m")
tile_menu.grid(row=0, column=1, padx=10, pady=10)
tile_menu.current(0)

# Оновлення посилання при зміні вибору
tile_var.trace("w", update_tile_info)

# Кнопка для завантаження тайлів на основі обраного сервісу
tk.Button(container, text="Load map", command=lambda: merge_tiles(1)).grid(row=2, columnspan=2)

# Поле для зображення об'єднаної карти
combined_image_label = tk.Label(container)
combined_image_label.grid(row=4, columnspan=2)

# Кнопка для завантаження власної карти
tk.Button(container, text="Load your own map", command=upload_custom_map).grid(row=5, columnspan=2)

# Кнопка для створення 3D моделі
tk.Button(container, text="Create a 3D model", command=create_3d_model).grid(row=6, columnspan=2)

# Відображення посилання на інформацію про тайл
tile_info_label = tk.Label(container, text="Map information:", fg="blue", cursor="hand2")
tile_info_label.grid(row=7, columnspan=2)

# Кнопка для показу/приховування додаткового блоку
toggle_button = tk.Button(container, text="Additional ▼", command=toggle_additional)
toggle_button.grid(row=8, columnspan=2, padx=10, pady=10)

# Додатковий блок (початково прихований)
additional_frame = tk.Frame(container)
tk.Label(additional_frame, text="Pixel step (1-100):").grid(row=0, column=0, sticky=tk.W)
step_entry = tk.Entry(additional_frame)
step_entry.grid(row=0, column=1, padx=10, pady=10)
step_entry.insert(0, "1")

tk.Label(additional_frame, text="Platform thickness (0.1-10):").grid(row=1, column=0, sticky=tk.W)
platform_entry = tk.Entry(additional_frame)
platform_entry.grid(row=1, column=1, padx=10, pady=10)
platform_entry.insert(0, "1")

tk.Label(additional_frame, text="Height scale (0.1-10):").grid(row=2, column=0, sticky=tk.W)
height_entry = tk.Entry(additional_frame)
height_entry.grid(row=2, column=1, padx=10, pady=10)
height_entry.insert(0, "0.1")

tk.Label(additional_frame, text="Choose a processing method:").grid(row=3, column=0, sticky=tk.W)
service_var = tk.IntVar(value=1)  # Початково вибрано Black-White
tk.Radiobutton(additional_frame, text="Black-White", variable=service_var, value=1).grid(row=3, column=1, sticky=tk.W)
tk.Radiobutton(additional_frame, text="RGB", variable=service_var, value=2).grid(row=3, column=2, sticky=tk.W)

tk.Label(additional_frame, text="Size limits(bigger quality, bigger size)").grid(row=5, column=0, sticky=tk.W)
size_var = tk.IntVar(value=1)
tk.Checkbutton(additional_frame, variable=size_var).grid(row=5, column=1, sticky=tk.W)

tk.Label(additional_frame, text="Enhancement for grounds lower (max height, multiplier)").grid(row=6, column=0, sticky=tk.W)
height_enhancement_var = tk.IntVar(value=0)  # Унікальна змінна для другого Checkbutton
tk.Checkbutton(additional_frame, variable=height_enhancement_var).grid(row=6, column=1, sticky=tk.W)

# Поля для введення максимального значення висоти і множника
height_max = tk.Entry(additional_frame)
height_max.grid(row=6, column=2)
height_max.insert(0, "20")

height_x_val = tk.Entry(additional_frame)
height_x_val.grid(row=6, column=3)
height_x_val.insert(0, "1.5")

# Початково приховуємо додатковий блок
additional_frame.grid_remove()

root.mainloop()
