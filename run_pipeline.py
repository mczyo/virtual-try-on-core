import subprocess
import sys # This lets us find the exact venv Python

scripts = ["scraper.py", "bg_remover.py", "standardizer.py", "mask_maker.py"]

print("🛠️ STARTING MASTER VTON PIPELINE...")
for script in scripts:
    print(f"\n▶️ EXECUTION: {script}")
    
    # We replace "python" with sys.executable to lock it inside the venv
    result = subprocess.run([sys.executable, script])
    
    if result.returncode == 0:
        print(f"✅ {script} finished successfully.")
    else:
        print(f"❌ {script} FAILED. Stopping pipeline.")
        break

print("\n🏆 ALL TASKS COMPLETE. DATASET IS READY FOR THE CLOUD.")