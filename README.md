# MKV Muxer для кино 🎬

Автоматизированный инструмент для встраивания внешних аудиодорожек и субтитров в MKV-файлы 

[![Python 3.6+](https://img.shields.io/badge/Python-3.6%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 📖 Описание

Скрипт автоматически находит и добавляет в MKV-файлы:
- Внешние аудиодорожки из папки `Sound`
- Субтитры из папки `Subs`
- Сохраняет оригинальные метаданные
- Автоматически определяет структуру каталогов

Идеально подходит для:
- Сборки финальных релизов кино и аниме
- Объединения разрозненных дорожек
- Автоматизации процесса монтажа

## ✨ Особенности

- 📁 Обработка как отдельных файлов, так и директорий
- 🔍 Автоматическое определение номеров эпизодов
- 🛡️ Защита от перезаписи оригиналов
- 📊 Статистика выполнения
- 💻 Кроссплатформенная работа (Windows/Linux/macOS)

## ⚙️ Требования

- Python 3.6+
- [MKVToolNix](https://mkvtoolnix.download/)
- Стандартная структура каталогов:
```
    /Sound
    /Group1
    EpisodeXX.aac
    /Subs
    /Group2
    EpisodeXX.ass
```


## 🚀 Установка

1. Установите MKVToolNix:
 - **Windows**: [Скачать установщик](https://mkvtoolnix.download/downloads.html#windows)
 - **macOS**: `brew install mkvtoolnix`
 - **Linux**: `sudo apt install mkvtoolnix`

2. Клонируйте репозиторий:
 ```bash
 git clone https://github.com/mercury131/combine-all-to-mkv.git
 cd combine-all-to-mkv
 ```
## 🎮 Использование 
```
python combine-mkv.py "/path/to/anime/folder"
python combine-mkv.py "/path/to/file.mkv"
or just
python muxer.py 
> Перетащите файл/папку сюда или введите путь:
 
```

## 📂 Структура выходных данных
Результаты сохраняются в папку Merged:
```
/Merged
  Episode01.mkv      # С встроенными дорожками
  Episode02.mkv
  ...
```
