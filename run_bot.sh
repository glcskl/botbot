#!/bin/bash

# Script to kill all conflicting Python processes and run the bot

echo "🔍 Checking for running Python processes..."
pkill -f python3 2>/dev/null || true
pkill -f bash 2>/dev/null || true
pkill -f zsh 2>/dev/null || true
pkill -f deploy.sh 2>/dev/null || true

# Wait for processes to terminate
sleep 2

echo "✅ All conflicting processes terminated"

echo "📦 Navigating to bot directory..."
cd uni_schedule_bot

echo "🚀 Starting bot..."
./deploy.sh