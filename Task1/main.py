import argparse
import asyncio
import os
import shutil
import logging
from pathlib import Path
from tkinter import Tk
from tkinter import filedialog

# Налаштування логування
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logging.basicConfig(
    filename="file_sorter.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


# Отримуємо абсолютний шлях до поточної директорії
current_dir = Path(__file__).resolve().parent


# Асинхронна функція для рекурсивного читання папок
async def read_folder(source_folder, output_folder):
    try:
        logging.info(
            f"Читання файлів з {source_folder} та сортування у {output_folder}"
        )
        for root, dirs, files in os.walk(source_folder):
            if not files:
                logging.info(f"Немає файлів для обробки в {root}")
            tasks = []
            for file in files:
                source_path = Path(root) / file
                tasks.append(asyncio.create_task(copy_file(source_path, output_folder)))
            await asyncio.gather(*tasks)
    except Exception as e:
        logging.error(f"Помилка при читанні папки: {e}")


# Асинхронна функція для копіювання файлів на основі їх розширення
async def copy_file(source_path, output_folder):
    try:
        file_extension = source_path.suffix[1:]  # Отримуємо розширення файлу без крапки
        target_folder = Path(output_folder) / file_extension

        # Створюємо цільову папку, якщо її немає
        target_folder.mkdir(parents=True, exist_ok=True)

        target_path = target_folder / source_path.name
        shutil.copy2(source_path, target_path)
        logging.info(f"Файл скопійовано: {source_path} до {target_path}")
    except Exception as e:
        logging.error(f"Помилка при копіюванні файлу {source_path}: {e}")


# Функція для вибору папки через графічний інтерфейс
def select_folder(prompt):
    root = Tk()
    root.withdraw()  # Приховуємо основне вікно
    folder_selected = filedialog.askdirectory(title=prompt)
    root.destroy()  # Закриваємо вікно після вибору
    return folder_selected


# Головна асинхронна функція
async def main(source_folder=None, output_folder=None):
    # Якщо папки не передані через командний рядок, викликаємо графічний інтерфейс для вибору папки
    if not source_folder:
        source_folder = select_folder("Виберіть вихідну папку:")
    if not output_folder:
        output_folder = select_folder("Виберіть цільову папку:")

    if not source_folder or not output_folder:
        logging.error("Не було обрано папку!")
        return

    await read_folder(source_folder, output_folder)


if __name__ == "__main__":
    # Створення ArgumentParser для обробки аргументів командного рядка
    parser = argparse.ArgumentParser(
        description="Asynchronous file sorter based on file extensions."
    )
    parser.add_argument("--source_folder", type=str, help="Path to the source folder")
    parser.add_argument("--output_folder", type=str, help="Path to the output folder")

    args = parser.parse_args()

    # Якщо аргументи не передані, використовуємо графічний інтерфейс для вибору папки
    source_folder = args.source_folder if args.source_folder else None
    output_folder = args.output_folder if args.output_folder else None

    logging.info(f"Початок сортування файлів")

    # Запуск асинхронного сортування файлів
    asyncio.run(main(source_folder, output_folder))
