import os
import re
import subprocess
import argparse
from pathlib import Path
from typing import List, Union

def select_path_interactively() -> Path:
    while True:
        path_str = input("Введите путь к файлу/папке аниме или перетащите его сюда: ").strip(' "\'')
        path = Path(path_str)
        if path.exists():
            return path
        print(f"Ошибка: Путь не существует - {path}")

def find_media_files(root_dir: Path, patterns: List[str]) -> List[Path]:
    return sorted([p for p in root_dir.rglob('*') if p.suffix.lower() in patterns])

def extract_episode_number(filename: str) -> Union[str, None]:
    # Универсальное извлечение номера эпизода через регулярное выражение
    match = re.search(r'[- _](\d{2})\b', filename)
    return match.group(1) if match else None

def get_episode_files(episode_num: str, media_files: List[Path]) -> List[Path]:
    # Используем ту же логику извлечения номера для всех файлов
    return sorted([f for f in media_files if extract_episode_number(f.name) == episode_num])

def merge_files(mkv_file: Path, audio_files: List[Path], sub_files: List[Path], output_dir: Path):
    output_file = output_dir / mkv_file.name
    temp_file = output_dir / f"temp_{mkv_file.name}"
    command = ['mkvmerge', '-o', str(temp_file), str(mkv_file)]
    
    for audio in audio_files:
        track_name = audio.parent.name.replace('[', '').replace(']', '')
        command += ['--track-name', f'0:{track_name}', str(audio)]
        
    for sub in sub_files:
        lang = sub.parent.name.replace(' ', '_').replace('[', '').replace(']', '')
        command += ['--subtitle-charset', '0:utf-8', '--track-name', f'0:{lang}', str(sub)]
        
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        temp_file.replace(output_file)
        print(f"✓ Успешно: {output_file.name}")
    except subprocess.CalledProcessError as e:
        print(f"✗ Ошибка при обработке {mkv_file.name}: {e.stderr}")
        if temp_file.exists():
            temp_file.unlink()

def process_target(target_path: Path):
    if target_path.is_file():
        root_dir = target_path.parent
        mkv_files = [target_path]
    else:
        root_dir = target_path
        mkv_files = find_media_files(root_dir, ['.mkv'])
        
    output_dir = root_dir / "Merged"
    output_dir.mkdir(exist_ok=True)
    
    # Поддержка разных аудиоформатов
    audio_files = find_media_files(root_dir / "Sound", ['.aac', '.mka'])
    sub_files = find_media_files(root_dir / "Subs", ['.ass'])
    
    for mkv in mkv_files:
        if "Extras" in str(mkv) or "Transformation" in str(mkv):
            continue
            
        ep_num = extract_episode_number(mkv.name)
        if not ep_num:
            print(f"⚠ Не удалось определить номер эпизода для {mkv.name}")
            continue
            
        print(f"\nОбработка эпизода {ep_num}: {mkv.name}")
        matching_audio = get_episode_files(ep_num, audio_files)
        matching_subs = get_episode_files(ep_num, sub_files)
        
        if matching_audio or matching_subs:
            merge_files(mkv, matching_audio, matching_subs, output_dir)
        else:
            print(f"⚠ Нет дополнительных дорожек для эпизода {ep_num}")

def main():
    parser = argparse.ArgumentParser(description='MKV Muxer для аниме')
    parser.add_argument('path', nargs='?', help='Путь к файлу/папке аниме')
    args = parser.parse_args()
    
    if args.path:
        target_path = Path(args.path).expanduser().resolve()
        if not target_path.exists():
            print(f"Ошибка: Указанный путь не существует - {target_path}")
            return
    else:
        print("Перетащите файл/папку аниме в это окно или введите путь:")
        target_path = select_path_interactively()
        
    process_target(target_path)
    print("\nГотово! Результаты в папке Merged")

if __name__ == "__main__":
    main()
