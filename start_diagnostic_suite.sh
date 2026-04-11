#!/bin/bash

echo "============================================================"
echo "DIAGNOSTIC PRO SUITE ULTIMATE EDITION"
echo "Wersja: 2.0.0"
echo "============================================================"

cd "Grazyna_MPPS_V21_Ultimate_Turbo_Complete"

echo "Uruchamianie systemu diagnostycznego..."
python3 CORE/PROFESSIONAL_CONTROL_PANEL.html

if [ $? -ne 0 ]; then
    echo "Błąd uruchamiania systemu!"
    exit 1
fi

echo "System uruchomiony pomyślnie!"
