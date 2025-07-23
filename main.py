import os
import subprocess
import keyboard
scripts = {
    '1': 'rickblink.py',
    '2': 'rickeye.py',
    '3': 'rickface.py',
    '4': 'rickmirror.py',
    '5': 'rickpose.py',
    '6': 'rickstare.py',
    '7': 'ricktouch.py',
    '8': 'rickyawn.py',
    '9': 'rickfake.py'
}
def show_menu():
    os.system('cls'if os.name=='nt'else'clear')
    print("===== RICKROLL LAUNCHER =====")
    for i in range(1, 10):
        print(f"[{i}] Run Prank {i}")
    print("[ESC] Exit")
    print("=============================")
show_menu()
while True:
    key = keyboard.read_key()
    if key in scripts:
        print(f"\nLaunching Prank {key}...")
        subprocess.run(['python', scripts[key]])
        show_menu()
    elif key == 'esc':
        print("\nExiting launcher. Goodbye.")
        break
