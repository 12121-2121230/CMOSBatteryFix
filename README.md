## Windows Stealth Time Sync (Invisible Service)
A zero-UI background utility for Windows that fixes clock drift and dead CMOS battery issues. It runs invisibly as a .pyw process, ensuring your system clock stays perfectly synced without manual intervention or visible windows. 
 ## ⚠️ CRITICAL: DEAD CMOS BATTERY INSTRUCTIONS




If your laptop/PC's CMOS battery is already dead, your system may not have internet or stable enough settings to download this directly.
Follow these steps:
1. Use another laptop/PC that has a working internet connection. 
2. Download the file and save it onto a USB drive. 
3. Plug the USB into the laptop/PC with the dead CMOS. 
4. Import/Copy the file to the local drive before running. Note: This script will force the time to stay correct even if the internal battery can't save it during reboots.
## ✨ Features 
* Auto-Installer: Automatically creates a Windows Task Scheduler entry on the first run. 
* AC/Battery Support: Forced to run even when the laptop is not plugged in (overrides default Windows power restrictions). 
* UAC Bypass: After the first run, it starts at every boot with Admin rights without asking for permission. 
* Zero UI: No windows, no logs, no taskbar icons. Completely invisible. 
* Dual-Boot Fix: Forces Windows to treat the hardware clock as UTC (Fixes Linux/Windows time mismatch). * Single Instance Lock: Uses a system-level handle to ensure only one copy runs at a time.
*  ## 🚀 How to Use 
1. Ensure Python is installed. 
2.Download time_sync.pyw. 
3. Double-click the file. [Only once]
4. Click "Yes" on the Windows Admin prompt. 
5. That’s it. The script is now running and scheduled to start every time you turn on your computer.
*  ## 🛑 How to Remove 
1. Open Task Manager and end pythonw.exe. 
2. Open Command Prompt (Admin) and run: schtasks /delete /tn "StealthTimeSync" /f 
[Note: Use with care as this modifies System Registry values to ensure high-frequency time synchronization.] Enjoy and ***BYE!***
