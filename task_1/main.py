import asyncio
import aiofiles
import os
from pathlib import Path
import shutil
import logging
import argparse

# Налаштування логування
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


async def read_folder(source_path, dest_path):
    # Перевірка наявності вихідної папки
    if not os.path.exists(source_path):
        logging.error(f"Source folder {source_path} does not exist.")
        return

    # Створення цільової папки, якщо вона не існує
    os.makedirs(dest_path, exist_ok=True)

    tasks = []
    for root, _, files in os.walk(source_path):
        for file in files:
            source_file = Path(root) / file
            tasks.append(copy_file(source_file, dest_path))

    await asyncio.gather(*tasks)


async def copy_file(source_file, dest_path):
    try:
        ext = source_file.suffix[1:] if source_file.suffix else "no_extension"
        target_dir = Path(dest_path) / ext
        os.makedirs(target_dir, exist_ok=True)
        target_file = target_dir / source_file.name

        async with aiofiles.open(source_file, "rb") as src, aiofiles.open(
            target_file, "wb"
        ) as dst:
            content = await src.read()
            await dst.write(content)
        logging.info(f"Copied {source_file} to {target_file}")
    except Exception as e:
        logging.error(f"Failed to copy {source_file}: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Asynchronously sort files based on their extensions."
    )
    parser.add_argument("source_folder", type=str, help="Path to the source folder.")
    parser.add_argument("output_folder", type=str, help="Path to the output folder.")
    args = parser.parse_args()

    source_path = Path(args.source_folder)
    dest_path = Path(args.output_folder)

    asyncio.run(read_folder(source_path, dest_path))


if __name__ == "__main__":
    main()
