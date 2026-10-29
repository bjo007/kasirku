"""Titik masuk aplikasi Kasir Warung Pintar (desktop PySide6 & Android KivyMD).

Desktop:
    python main.py                 # jalankan aplikasi desktop
    python main.py --no-demo       # tanpa data demo (database baru kosong)
    python main.py --seed-only     # isi data demo lalu keluar
    python main.py --data-dir X    # arahkan folder data khusus

Android (build APK via Buildozer, lihat README):
    main.py otomatis mendeteksi lingkungan Android dan menjalankan
    versi mobile KivyMD dengan mesin bisnis yang sama.

Mode mobile juga bisa dicoba di desktop:  KASIR_UI=mobile python main.py
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from app.core.config import APP_NAME, APP_VERSION, get_db_path


def _on_android() -> bool:
    """True bila berjalan di dalam python-for-android."""
    return any(k in os.environ for k in ("ANDROID_ARGUMENT", "ANDROID_PRIVATE", "P4A_BOOTSTRAP"))


def _wants_mobile() -> bool:
    return _on_android() or os.environ.get("KASIR_UI", "").lower() == "mobile"


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=APP_NAME)
    parser.add_argument("--data-dir", help="Folder data khusus (default: folder data aplikasi)")
    parser.add_argument("--db", help="Path file database SQLite khusus")
    parser.add_argument("--no-demo", action="store_true", help="Jangan isi data demo")
    parser.add_argument("--seed-only", action="store_true", help="Isi data demo lalu keluar")
    parser.add_argument("--version", action="version", version=f"{APP_NAME} v{APP_VERSION}")
    return parser.parse_args(argv)


def prepare_database(args: argparse.Namespace):
    """Buat engine, jalankan migrasi, isi data bawaan. Mengembalikan Database."""
    from app.core.logging_config import setup_logging, get_logger
    setup_logging()
    log = get_logger("main")

    if args.data_dir:
        import os
        os.environ["KASIR_DATA_DIR"] = str(Path(args.data_dir).resolve())

    from app.database.database import Database
    from app.database.migrations import ensure_schema
    from app.models.base import Base
    import app.models  # noqa: F401

    db_path = Path(args.db) if args.db else get_db_path()
    db = Database(db_path)
    ensure_schema(db.engine, Base.metadata)

    from app.core import constants as C
    from app.repositories.catalog import UnitRepository
    from app.repositories.expenses import ExpenseCategoryRepository
    from app.services.auth_service import AuthService
    from app.services.settings_service import SettingsService

    auth = AuthService(db)
    auth.ensure_default_users()
    with db.session() as s:
        UnitRepository(s).ensure_defaults(C.DEFAULT_UNITS)
        ExpenseCategoryRepository(s).ensure_defaults(C.DEFAULT_EXPENSE_CATEGORIES)
    settings = SettingsService(db)
    settings.seed_defaults()

    # Data demo saat pertama kali dijalankan
    from sqlalchemy import select
    from app.models.sales import Sale
    with db.session() as s:
        has_sales = s.execute(select(Sale.id).limit(1)).scalar_one_or_none() is not None

    if (not has_sales and not args.no_demo) or args.seed_only:
        from scripts.seed_demo_data import seed_all, seed_demo_transactions
        log.info("Mengisi data demo...")
        seed_all(db)
        seed_demo_transactions(db)
    return db


def run_gui(db) -> int:
    from PySide6.QtGui import QFont
    from PySide6.QtWidgets import QApplication

    from app.core.logging_config import get_logger
    from app.core.theme import load_qss
    from app.core.app_context import AppContext
    from app.views.login_window import LoginWindow
    from app.views.main_window import MainWindow

    log = get_logger("main")
    app = QApplication.instance() or QApplication(sys.argv)
    app.setApplicationName("Kasir Warung Pintar")
    app.setStyle("Fusion")
    app.setFont(QFont("Segoe UI", 10))

    ctx = AppContext(db)
    app.setStyleSheet(load_qss(ctx.settings.get("theme", "light")))
    ctx.bus.theme_changed.connect(lambda t: app.setStyleSheet(load_qss(t)))

    while True:
        ctx.current_user = None
        result = {"action": "quit"}
        login = LoginWindow(ctx, on_success=lambda u: None)

        def on_login(user) -> None:
            ctx.current_user = user
            main = MainWindow(ctx)

            def on_logout() -> None:
                result["action"] = "logout"
                main.close()

            ctx.bus.logout_requested.connect(on_logout)
            main.show()
            login.close()

        login.on_success = on_login
        login.show()
        app.exec()  # berjalan sampai tidak ada jendela terbuka
        if result["action"] != "logout":
            break
    log.info("Aplikasi ditutup.")
    return 0


def main(argv: list[str] | None = None) -> int:
    if _wants_mobile():
        # Mode Android/mobile: database di-bootstrap di dalam MobileKasirApp
        from mobile.app import MobileKasirApp
        return MobileKasirApp().run() or 0

    args = parse_args(argv if argv is not None else sys.argv[1:])
    db = prepare_database(args)
    if args.seed_only:
        return 0
    return run_gui(db)


if __name__ == "__main__":
    sys.exit(main())
