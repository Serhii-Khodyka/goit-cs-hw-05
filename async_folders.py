import argparse
import asyncio
import logging
from aiofile import async_open
from aiopath import AsyncPath
import aioshutil

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def read_folder(source_folder: AsyncPath, output_folder: AsyncPath):
    async for entry in source_folder.iterdir():
        if await entry.is_dir():
            await read_folder(entry, output_folder)
        elif await entry.is_file():
            await copy_file(entry, output_folder)

async def copy_file(file_path: AsyncPath, output_folder: AsyncPath):
    file_extension = file_path.suffix.lstrip('.')
    target_folder = output_folder / file_extension

    try:
        await target_folder.mkdir(parents=True, exist_ok=True)
        destination = target_folder / file_path.name
        await aioshutil.copy(file_path, destination)
        logging.info(f'Copied {file_path} to {destination}')
    except Exception as e:
        logging.error(f'Failed to copy {file_path} to {destination}: {e}')

def main():
    parser = argparse.ArgumentParser(description='Asynchronous file sorter based on file extension')
    parser.add_argument('source_folder', type=str, help='Source folder to read files from')
    parser.add_argument('output_folder', type=str, help='Output folder to store sorted files')

    args = parser.parse_args()
    source_folder = AsyncPath(args.source_folder)
    output_folder = AsyncPath(args.output_folder)

    asyncio.run(read_folder(source_folder, output_folder))

if __name__ == '__main__':
    main()
