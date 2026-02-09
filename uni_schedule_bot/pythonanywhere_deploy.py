#!/usr/bin/env python3
"""Скрипт для деплоя бота на PythonAnywhere"""

import os
import sys
import subprocess


def run_command(cmd):
    print(f"🚀 Выполняю: {cmd}")
    try:
        output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
        print(f"✅ Выполнено: {output.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка: {e.output.strip()}")
        return False


def main():
    print("📦 Начало деплоя бота на PythonAnywhere...")

    # Проверка, что мы находимся в правильной директории
    expected_dir = "/home/glebtokar10/uni_schedule_bot"
    if os.getcwd() != expected_dir:
        os.chdir(expected_dir)
        print(f"📁 Перешли в папку: {expected_dir}")

    # Проверка наличия всех необходимых файлов
    required_files = ["bot.py", "requirements.txt", "schedule.json", ".env"]
    for filename in required_files:
        if not os.path.exists(filename):
            print(f"❌ Файл не найден: {filename}")
            return False

    print("✅ Все необходимые файлы найдены")

    # Установка зависимостей
    if not run_command("pip install -r requirements.txt --user"):
        return False

    # Запуск бота
    print("🚀 Запуск бота...")
    # В PythonAnywhere для запуска бота в фоне используется nohup или задачи
    run_command("python3 /home/glebtokar10/uni_schedule_bot/bot.py")


if __name__ == "__main__":
    main()