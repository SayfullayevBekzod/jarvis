import os
import subprocess
import sys
import shutil

# Add jarvis directory to sys.path to import config
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "jarvis"))
try:
    import config
except ImportError:
    # Fallback for localized environments
    sys.path.insert(0, os.path.abspath("jarvis"))
    import config

def compile_jarvis():
    print("==================================================")
    print("   JARVIS - EXE KOMPILYATSIYA QILISH (BETA)   ")
    print("==================================================")
    
    # 1. PyInstaller borligini tekshirish
    try:
        import PyInstaller
        print("[1] PyInstaller topildi.")
    except ImportError:
        print("[1] PyInstaller topilmadi. O'rnatilmoqda...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("[1] PyInstaller muvaffaqiyatli o'rnatildi.")

    # 2. Path'lar
    root_dir = os.path.dirname(os.path.abspath(__file__))
    main_script = os.path.join(root_dir, "jarvis", "main.py")
    assets_dir = os.path.join(root_dir, "jarvis", "assets")
    
    # Windowsda separator ';'
    separator = ";" if os.name == "nt" else ":"
    
    # 3. PyInstaller buyrug'i
    # --onefile: Hamma narsani bitta .exe ichiga yig'adi
    # --noconsole: GUI bilan ochiladi, terminal ko'rinmaydi
    # --add-data: Asset'larni paket ichiga qo'shish
    # --clean: Keshni tozalash
    
    # --hidden-import: Ba'zi dinamik importlarni qo'shish
    
    version_str = config.APP_VERSION.replace(".", "_")
    exe_name = f"JarvisPro_v{version_str}"
    
    cmd = [
        "pyinstaller",
        "--onefile",
        "--noconsole",
        f"--name={exe_name}",
        f"--add-data={assets_dir}{separator}jarvis/assets",
        "--hidden-import=requests",
        "--hidden-import=packaging",
        "--hidden-import=google.generativeai",
        "--hidden-import=edge_tts",
        "--clean",
        main_script
    ]
    
    print(f"\n[2] Kompilyatsiya boshlandi...")
    print(f"Buyruq: {' '.join(cmd)}")
    
    try:
        subprocess.check_call(cmd)
        print("\n" + "="*50)
        print(">>> MUVAFFAQIYATLI YAKUNLANDI!")
        print("[OK] EXE fayl 'dist/' papkasiga saqlandi (JarvisPro.exe).")
        print("="*50)
        
        # 4. Cleanup (build papkasi va .spec faylni o'chirish - ixtiyoriy)
        answer = input("\nBuild va .spec fayllarini o'chirib tashlaymi? (y/n): ")
        if answer.lower() == 'y':
            spec_file = os.path.join(root_dir, "JarvisPro.spec")
            build_dir = os.path.join(root_dir, "build")
            
            if os.path.exists(spec_file): os.remove(spec_file)
            if os.path.exists(build_dir): shutil.rmtree(build_dir)
            print("Tozalandi.")
            
    except Exception as e:
        print(f"\n[X] Xatolik yuz berdi: {e}")

if __name__ == "__main__":
    compile_jarvis()
