import os
import shutil

def remove_pycache_folders(root_dir):
    # Проходим по всем папкам и файлам в указанной директории
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Если папка __pycache__ найдена, удаляем её
        if '__pycache__' in dirnames:
            pycache_path = os.path.join(dirpath, '__pycache__')
            try:
                shutil.rmtree(pycache_path)
                print(f"Удалена папка: {pycache_path}")
            except Exception as e:
                print(f"Ошибка при удалении {pycache_path}: {e}")

# Укажите корневую директорию для поиска __pycache__
root_directory = './app'

# Запускаем функцию
remove_pycache_folders(root_directory)
