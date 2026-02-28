import os
import sys
import json
import requests
import subprocess
import time
import shutil
import tempfile
from packaging import version
import config

class AutoUpdater:
    """Jarvis auto-update tizimi"""
    
    def __init__(self):
        self.current_version = config.APP_VERSION
        self.update_url = config.UPDATE_URL
        self.is_compiled = getattr(sys, 'frozen', False) # .exe ichidami?
        self.is_git = self._check_git()

    def _check_git(self):
        """Git repozitoriyasini tekshirish"""
        try:
            # updater.py jarvis/core ichida joylashgan
            # .git esa loyiha ildizida joylashgan (../../.git)
            root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            return os.path.exists(os.path.join(root_dir, ".git"))
        except:
            return False

    def check_for_updates(self):
        """Yangi versiyani tekshirish"""
        try:
            print(f"[Updater] Tekshirilmoqda: {self.update_url}")
            # Cache-ni chetlab o'tish uchun vaqt tamg'asi qo'shamiz
            resp = requests.get(f"{self.update_url}?t={int(time.time())}", timeout=5)
            if resp.status_code == 200:
                data = resp.json()
                latest_version = data.get("version", "1.0.0")
                
                if version.parse(latest_version) > version.parse(self.current_version):
                    print(f"[Updater] Yangi versiya topildi: {latest_version}")
                    return {
                        "update_available": True,
                        "version": latest_version,
                        "download_url": data.get("download_url"),
                        "changelog": data.get("changelog", "Yaxshilanishlar kiritildi.")
                    }
            return {"update_available": False}
        except Exception as e:
            print(f"[Updater] Tekshirishda xato: {e}")
            return {"update_available": False, "error": str(e)}

    def download_update(self, download_url, progress_callback=None):
        """Yangilanishni vaqtinchalik joyga yuklab olish"""
        try:
            print(f"[Updater] Yuklab olinmoqda: {download_url}")
            temp_dir = tempfile.gettempdir()
            new_exe_name = "JarvisPro_new.exe"
            temp_path = os.path.join(temp_dir, new_exe_name)
            
            resp = requests.get(download_url, stream=True, timeout=30)
            total_size = int(resp.headers.get('content-length', 0))
            
            downloaded = 0
            with open(temp_path, "wb") as f:
                for chunk in resp.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        if progress_callback:
                            percent = (downloaded / total_size) if total_size > 0 else 0
                            progress_callback(percent)
            
            return temp_path
        except Exception as e:
            print(f"[Updater] Yuklab olishda xato: {e}")
            return None

    def apply_update(self, new_exe_path):
        """Yangilanishni qo'llash"""
        if self.is_git:
            return self.apply_git_update()
            
        if not self.is_compiled:
            return "Dastur .exe holatida emas va Git repozitoriyasi topilmadi. Manuel yangilang."

        try:
            current_exe = sys.executable
            # Batch skriptini yaratamiz
            # Bu skript: kutadi, o'chiradi, ko'chiradi, ishga tushiradi va o'zini o'chiradi
            
            updater_bat = os.path.join(tempfile.gettempdir(), "jarvis_updater.bat")
            
            batch_content = f"""
@echo off
setlocal
echo Jarvis yangilanmoqda...
echo Asosiy dastur yopilishini kutmoqda...
timeout /t 2 /nobreak > nul

:retry
del /f /q "{current_exe}"
if exist "{current_exe}" (
    echo Fayl hali ham ochiq, qayta urinib ko'rilmoqda...
    timeout /t 1 /nobreak > nul
    goto retry
)

move /y "{new_exe_path}" "{current_exe}"
echo Yangi versiya muvaffaqiyatli o'rnatildi.
start "" "{current_exe}"

del "%~f0"
"""
            with open(updater_bat, "w") as f:
                f.write(batch_content)
            
            # Batch skriptini fon rejimida ishga tushiramiz
            subprocess.Popen(["cmd.exe", "/c", updater_bat], 
                             creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0)
            
            # Asosiy dasturni darhol yopamiz
            sys.exit(0)
            
        except Exception as e:
            print(f"[Updater] Apply xatosi: {e}")
            return False
            
    def apply_git_update(self):
        """Git orqali yangilash (developers uchun) triumph"""
        try:
            print("[Updater] Git pull bajarilmoqda...")
            # Git pull command
            result = subprocess.run(["git", "pull", "origin", "main"], 
                                   capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                print("[Updater] Git update muvaffaqiyatli.")
                return True
            else:
                print(f"[Updater] Git update xatosi: {result.stderr}")
                return False
        except Exception as e:
            print(f"[Updater] Git update xatosi: {e}")
            return False

# Singleton instance
updater = AutoUpdater()
