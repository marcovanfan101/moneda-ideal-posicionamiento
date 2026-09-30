"""
Script maestro: ejecuta todo el pipeline desde cero.

Uso:
    python scripts/01_run_all.py
"""

import sys
import os

# Agregar la raiz del proyecto al path para importar src y config
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.pipeline import run_all

if __name__ == "__main__":
    run_all()
