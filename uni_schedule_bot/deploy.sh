#!/bin/bash

# Скрипт для запуска бота локально
cd $(dirname "$0")

echo "🔍 Проверка Python версии..."
python3 --version

echo "📦 Установка зависимостей..."
pip3 install -r requirements.txt

echo "🚀 Запуск бота..."
python3 bot.py