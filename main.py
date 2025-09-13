from rich.console import Console
from rich.panel import Panel
from rich.columns import Columns
from rich.text import Text
from rich.box import ROUNDED
from rich.status import Status
import platform
import psutil
import os
import time
import subprocess
import sys
import winreg 

is_frozen = getattr(sys, 'frozen', False)
console = Console()

ARCH_LOGO = [
"⠀⠀⣿⠲⠤⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀",
"⠀⣸⡏⠀⠀⠀⠉⠳⢄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀",
"⠀⣿⠀⠀⠀⠀⠀⠀⠀⠉⠲⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀",
"⢰⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠲⣄⠀⠀⠀⡰⠋⢙⣿⣦⡀⠀⠀⠀⠀⠀",
"⠸⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣙⣦⣮⣤⡀⣸⣿⣿⣿⣆⠀⠀⠀⠀",
"⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⣿⣿⣿⣿⠀⣿⢟⣫⠟⠋⠀⠀⠀⠀",
"⠀⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⣿⣿⣿⣿⣷⣷⣿⡁⠀⠀⠀⠀⠀⠀",
"⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⢸⣿⣿⣧⣿⣿⣆⠙⢆⡀⠀⡀⠀⠀",
"⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢾⣿⣤⣿⣿⣿⡟⠹⣿⣿⣿⣿⣷⡇⠀⠀",
"⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣧⣴⣿⣿⣿⣿⠏⣧⠀⠀",
"⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠀⢹⢳⡀",
"⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⡏⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⢨⠀⢳",
"⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠰⠀⠀",
"⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇⠸⣿⣿⣿⣿⣿⣿⣿⣿⠏⠀⠀⠀⠀⡂⠀",
"⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇⠀⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⡀⠀",
"⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⡇⢠⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⢀⠀",
"⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠃⢸⣿⣿⣿⣿⣿⣿⣿⣿⠀⠐⡢⠀⠀⠠⠀",
"⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣼⢸⣿⣿⣿⣿⣿⣿⣿⣿⠀⢀⠥⠀⠀⠐⠀",
"⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⡄⠐⠪⠀⠀⠀⠈",
"⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⡇⢈⠒⠀⠀⠀⠀",
"⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⠠⢁⠀⠀⠀⠀",
"⠀⠀⠀⠀⠀⠀⠀⢀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢘⠀⠀⠀⠀⠀",
"⠀⠀⠀⠀⠀⠀⠀⠛⠻⠿⣿⣿⣿⡿⠿⠿⢿⠿⠿⢿⣿⣿⠏⠨⠈⠀⠀⠀⠀",
]

def run_powershell_command(command):
    try:
        result = subprocess.run(
            ["powershell", "-command", command],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='ignore',
            timeout=10,
            check=False,
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            return None
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return None

def get_system_info_windows():
    uname = platform.uname()
    mem = psutil.virtual_memory()
    uptime_seconds = time.time() - psutil.boot_time()
    uptime_hours = int(uptime_seconds // 3600)

    cpu_command = "Get-CimInstance Win32_Processor | Select-Object -ExpandProperty Name"
    cpu_name = run_powershell_command(cpu_command) or "N/A"

    gpu_command = "Get-CimInstance Win32_VideoController | Select-Object -ExpandProperty Name"
    gpu_name = run_powershell_command(gpu_command) or "N/A"

    os_edition_command = "(Get-ItemProperty -Path 'HKLM:\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion').ProductName"
    windows_edition = run_powershell_command(os_edition_command) or "N/A"

    winget_version_command = "winget --version"
    winget_version = run_powershell_command(winget_version_command)
    if winget_version:
        packages = f"winget: {winget_version.strip()}"
    else:
        packages = "winget: Not installed"

    installed_ram_gb = f"{mem.total // (1024**3)} GB"

    resolution_command = "(Get-CimInstance Win32_DesktopMonitor | Select-Object -ExpandProperty ScreenHeight, ScreenWidth | Format-List | Out-String)"
    resolution_output = run_powershell_command(resolution_command)
    resolution = "N/A"
    if resolution_output:
        lines = resolution_output.strip().split("\n")
        height = next((line.split(":")[-1].strip() for line in lines if "ScreenHeight" in line), None)
        width = next((line.split(":")[-1].strip() for line in lines if "ScreenWidth" in line), None)
        if height and width:
            resolution = f"{width}x{height}"

    info = {
        "OS": f"{uname.system} {uname.release}",
        "Kernel": uname.version,
        "Uptime": f"{uptime_hours} hours",
        "Host Name": uname.node,
        "Windows Edition": windows_edition,
        "Installed RAM": installed_ram_gb,
        "Display Resolution": resolution,
        "Shell": os.environ.get('COMSPEC', 'N/A'),
        "Packages": packages,
        "Terminal": os.environ.get('WT_SESSION', 'Windows Console'),
        "CPU": cpu_name,
        "GPU": gpu_name,
        "Memory Usage": f"{mem.used // (1024**2)} MiB / {mem.total // (1024**2)} MiB",
    }
    return info

def setup_startup_entry():
    key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    script_name = "SystemInfoDisplay"
    
    command = os.path.abspath(sys.executable)
    
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_ALL_ACCESS) as key:
            winreg.SetValueEx(key, script_name, 0, winreg.REG_SZ, command)
        console.print(f"[bold green]✓[/bold green] Script successfully added to Windows startup.")
    except Exception as e:
        console.print(f"[bold red]✗[/bold red] Failed to add script to startup. You may need to run as administrator. Error: {e}")

def check_startup_entry():
    key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    script_name = "SystemInfoDisplay"
    
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path) as key:
            value, _ = winreg.QueryValueEx(key, script_name)
            return True
    except FileNotFoundError:
        return False
    except winreg.error:
        return False
    return False

def main():
    if not is_frozen and not check_startup_entry():
        setup_startup_entry()
    
    with console.status("[bold green]Loading system information...") as status:
        info = get_system_info_windows()

    console.clear()

    logo_text = Text("\n".join(ARCH_LOGO), style="bold cyan")

    info_lines = [f"[bold yellow]{k}:[/bold yellow] {v}" for k, v in info.items()]
    info_text = "\n".join(info_lines)

    info_panel = Panel.fit(info_text, title="System Info", border_style="yellow", padding=(1,2), box=ROUNDED)

    console.print(Columns([logo_text, info_panel], equal=False, expand=True, padding=(0, 1)))

    credit_text = Text("Made by pxwild", style="dim white italic", justify="right")
    console.print(credit_text)

    input("Press Enter to exit...")

if __name__ == "__main__":
    main()