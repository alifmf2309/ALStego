import os
import zipfile
import time
import sys
import msvcrt
import socket
import urllib.request
import json
import uuid
from datetime import datetime, timezone

R = '\033[31m'  # Red
G = '\033[32m'  # Green
C = '\033[36m'  # Cyan
Y = '\033[33m'  # Yellow
W = '\033[0m'   # Reset/White
B = '\033[1m'   # Bold

T = {}
LANG = 'id'

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_ip_address():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip_local = s.getsockname()[0]
        s.close()
        return ip_local
    except Exception:
        return "127.0.0.1"

def get_public_ip_and_tz():
    try:
        url = "http://ip-api.com/json/"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=3) as response:
            data = json.loads(response.read().decode())
            if data.get("status") == "success":
                return data.get("query", "N/A"), data.get("timezone", "UTC")
    except Exception:
        pass
    return "Offline / N/A", "UTC"

def get_device_info():
    try:
        device_name = socket.gethostname()
    except Exception:
        device_name = "Unknown Device"
        
    try:
        mac_num = uuid.getnode()
        mac = ':'.join(['{:02x}'.format((mac_num >> ele) & 0xff) for ele in range(0, 8*6, 8)][::-1])
        mac_address = mac.upper()
    except Exception:
        mac_address = "N/A"
        
    return device_name, mac_address

_cached_pub_ip = None
_cached_pub_tz = None
_last_ip_check = 0

def print_banner(redraw=False):
    global _cached_pub_ip, _cached_pub_tz, _last_ip_check
    
    current_time_epoch = time.time()
    if _cached_pub_ip is None or (current_time_epoch - _last_ip_check > 60):
        _cached_pub_ip, _cached_pub_tz = get_public_ip_and_tz()
        _last_ip_check = current_time_epoch

    now = datetime.now()
    current_ip = get_ip_address()
    device_name, mac_address = get_device_info()
    
    try:
        from zoneinfo import ZoneInfo
        target_tz = ZoneInfo(_cached_pub_tz)
        now_tz = datetime.now(target_tz)
        utc_offset_sec = now_tz.utcoffset().total_seconds()
        utc_offset_hours = int(utc_offset_sec // 3600)
        sign = "+" if utc_offset_hours >= 0 else "-"
        utc_formatted = f"UTC {sign}{abs(utc_offset_hours)}"
        current_time = f"{now_tz.strftime('%H:%M')} ({utc_formatted})"
    except Exception:
        utc_offset_sec = time.altzone if (time.daylight and time.localtime().tm_isdst > 0) else time.timezone
        utc_offset_hours = -utc_offset_sec // 3600
        sign = "+" if utc_offset_hours >= 0 else "-"
        utc_formatted = f"UTC {sign}{abs(utc_offset_hours)}"
        current_time = f"{now.strftime('%H:%M')} ({utc_formatted})"

    full_timezone = f"{_cached_pub_tz}"
    
    if LANG == 'en':
        day_name = now.strftime("%A")
        month_name = now.strftime("%B")
    else:
        days_id = {
            'Monday': 'Senin', 'Tuesday': 'Selasa', 'Wednesday': 'Rabu',
            'Thursday': 'Kamis', 'Friday': 'Jumat', 'Saturday': 'Sabtu', 'Sunday': 'Minggu'
        }
        months_id = {
            'January': 'Januari', 'February': 'Februari', 'March': 'Maret',
            'April': 'April', 'May': 'Mei', 'June': 'Juni',
            'July': 'Juli', 'August': 'Agustus', 'September': 'September',
            'October': 'Oktober', 'November': 'November', 'December': 'Desember'
        }
        day_name = days_id.get(now.strftime("%A"), now.strftime("%A"))
        month_name = months_id.get(now.strftime("%B"), now.strftime("%B"))
    
    day_num = now.strftime("%d")
    year_num = now.strftime("%Y")
    date_time_display = f"{day_name}, {day_num} {month_name} {year_num}"
    
    if not redraw:
        sys.stdout.write("\033[H")
    
    print(f"{R}{B}        ___   __   _____ __                  ")
    print(f"       /   | / /  / ___// /____  ____  ____ ")
    print(f"      / /| |/ /   \__ \/ __/ _ \/ __ \/ __ \\")
    print(f"     / ___ / /______/ / /_/  __/ /_/ / /_/ /")
    print(f"    /_/  |_|_____/___/\__/\___/\____/\____/ ")
    print(f"                              /____/        {W}")
    print() 
    print(f"                        {Y}Version 1.0.0 (Beta){W}")
    print() 
    print(f"    {B}--------------------------------------------------{W}")
    print(f"    {G}            File Steganography Toolkit            {W}")
    print(f"    {B}--------------------------------------------------{W}")
    print(f"    {Y}Device Name: {device_name:<30}{W}")
    print(f"    {Y}MAC Address: {mac_address:<30}{W}")
    print(f"    {Y}IP Address : {current_ip:<30}{W}")
    print(f"    {Y}Public IP  : {_cached_pub_ip:<30}{W}")
    print(f"    {Y}Time Zone  : {full_timezone:<30}{W}")
    print(f"    {Y}Local Time : {current_time:<30}{W}")
    print(f"    {Y}Date Time  : {date_time_display:<30}{W}")
    print(f"    {B}--------------------------------------------------{W}")
    print()

def spinner_anim(text, duration=1.5, show_ok=True):
    spinner = ['|', '/', '-', '\\']
    end_time = time.time() + duration
    idx = 0
    while time.time() < end_time:
        sys.stdout.write(f"\r{C}[*]{W} {text} {Y}{spinner[idx % 4]}{W}")
        sys.stdout.flush()
        time.sleep(0.1)
        idx += 1
    if show_ok:
        sys.stdout.write(f"\r{C}[*]{W} {text} {G}OK!{W}       \n")
    else:
        sys.stdout.write(f"\r{' ' * (len(text) + 15)}\r")

def progress_bar(text, duration=2.0):
    sys.stdout.write(f"{C}[*]{W} {text}\n")
    toolbar_width = 40
    for i in range(toolbar_width + 1):
        percent = int((i / toolbar_width) * 100)
        bar = '#' * i + '-' * (toolbar_width - i)
        sys.stdout.write(f"\r    {Y}[{bar}] {percent}%{W}")
        sys.stdout.flush()
        time.sleep(duration / toolbar_width)
    print()

def set_language():
    global T, LANG
    clear_screen()
    print_banner(redraw=True)
    
    print(f"    {C}[*] ALStego Initial Setup{W}")
    print(f"    {C}[1]{W} Bahasa  (ID)")
    print(f"    {C}[2]{W} English (EN)")
    print(f"    {C}[3]{W} Exit")
    
    sys.stdout.write(f"\n{Y}[?]{W} Select Language (1-3): ")
    sys.stdout.flush()
    
    choice = ""
    last_refresh = time.time()
    while True:
        if time.time() - last_refresh >= 1.0:
            sys.stdout.write("\033[s")
            print_banner()
            sys.stdout.write("\033[u")
            sys.stdout.flush()
            last_refresh = time.time()

        if msvcrt.kbhit():
            char = msvcrt.getch()
            if char in b'\r\n':
                print()
                break
            elif char == b'\x08':
                if len(choice) > 0:
                    choice = choice[:-1]
                    sys.stdout.write('\b \b')
                    sys.stdout.flush()
            else:
                try:
                    decoded = char.decode('utf-8')
                    choice += decoded
                    sys.stdout.write(decoded)
                    sys.stdout.flush()
                except UnicodeDecodeError:
                    pass
        time.sleep(0.02)
    
    if choice == '1':
        LANG = 'id'
        T = {
            'start_inj': "Memulai modul Injeksi Steganografi...",
            'choose_fmt': "Pilih format file host yang akan di-inject :",
            'pick_fmt': "Pilih format",
            'invalid': "Pilihan tidak valid.",
            'must_num': "Input harus berupa angka.",
            'back_menu': "Kembali ke Menu Utama",
            'path_host': "Path file host",
            'err_404_file': "Error: File",
            'err_404_not_found': "tidak ditemukan.",
            'err_ext': "Error: Ekstensi file tidak cocok dengan pilihan",
            'req': "dibutuhkan",
            'path_zip': "Path file ZIP (.zip) yang akan disisipkan :",
            'err_zip_fmt': "FATAL: Modul ini HANYA mendukung payload berformat .ZIP!",
            'out_name': "Nama output file (contoh: hasil",
            'proc': "Menginjeksi payload ke dalam binary...",
            'inj_ok': "INJEKSI BERHASIL!",
            'inj_ok_msg': "Payload ZIP bersarang dengan aman di",
            'sys_err': "Terjadi kesalahan sistem:",
            
            'start_chk': "Memulai modul Analisis Ekstensi...",
            'path_tgt': "Path target file untuk dianalisis :",
            'scan_eocd': "Memindai End of Central Directory (EOCD)...",
            'vuln': "TARGET VULNERABLE / ZIP PAYLOAD TERDETEKSI!",
            'hidden_list': "Isi file yang bersembunyi:",
            'neg': "Negatif. Tidak ada payload ZIP tersembunyi atau file rusak.",
            
            'start_ext': "Memulai modul Ekstraksi Payload...",
            'tgt_ext': "Path target file yang mengandung sisipan :",
            'exec_ext': "Mengeksekusi ekstraksi payload...",
            'ext_ok': "EKSTRAKSI BERHASIL!",
            'ext_ok_msg': "Data ditarik ke:",
            'ext_fail': "Gagal. Ekstraksi dibatalkan karena struktur ZIP tidak valid.",
            
            'm1': "Injeksi Binary ZIP File",
            'm2': "Analisis & Cek File Inject",
            'm3': "Ekstrak File Inject",
            'm4': "Pilih Bahasa Kembali",
            'm5': "Keluar",
            'init_msg': "Menyiapkan antarmuka sistem",
            'exit_msg': "Menutup ALStego... Tolong Gunakan Program Untuk Tujuan Yang Baik.",
            'cmd_err': "Command tidak dikenali.",
            'press_enter': "[Tekan Enter untuk kembali ke menu utama]"
        }
        spinner_anim(T['init_msg'], 1.5)
        main()
    elif choice == '2':
        LANG = 'en'
        T = {
            'start_inj': "Starting Steganography Injection module...",
            'choose_fmt': "Choose host file format to inject :",
            'pick_fmt': "Choose format",
            'invalid': "Invalid choice.",
            'must_num': "Input must be a number.",
            'back_menu': "Back to Main Menu",
            'path_host': "Host file path",
            'err_404_file': "Error: File",
            'err_404_not_found': "not found.",
            'err_ext': "Error: File extension does not match selection",
            'req': "required",
            'path_zip': "Path of ZIP file (.zip) to inject :",
            'err_zip_fmt': "FATAL: This module ONLY supports .ZIP format payloads!",
            'out_name': "Output file name (example: result",
            'proc': "Injecting payload into binary stream...",
            'inj_ok': "INJECTION SUCCESSFUL!",
            'inj_ok_msg': "ZIP payload safely nested inside",
            'sys_err': "System error occurred:",
            
            'start_chk': "Starting Extension Analysis module...",
            'path_tgt': "Target file path to analyze:",
            'scan_eocd': "Scanning End of Central Directory (EOCD)...",
            'vuln': "VULNERABLE TARGET / ZIP PAYLOAD DETECTED!",
            'hidden_list': "Hidden file contents:",
            'neg': "Negative. No hidden ZIP payload or file is corrupted.",
            
            'start_ext': "Starting Payload Extraction module...",
            'tgt_ext': "Target file path containing injection :",
            'exec_ext': "Executing payload extraction...",
            'ext_ok': "EXTRACTION SUCCESSFUL!",
            'ext_ok_msg': "Data extracted to:",
            'ext_fail': "Failed. Extraction aborted due to invalid ZIP structure.",
            
            'm1': "Inject Binary ZIP File",
            'm2': "Analyze & Check Injected File",
            'm3': "Extract Injected File",
            'm4': "Change Language",
            'm5': "Exit",
            'init_msg': "Initializing system interface",
            'exit_msg': "Shutting down ALStego... Please Use The Program For Good Purposes.",
            'cmd_err': "Unrecognized command.",
            'press_enter': "[Press Enter to return to main menu]"
        }
        spinner_anim(T['init_msg'], 1.5)
        main()
    elif choice == '3':
        print()
        spinner_anim("Shutting down ALStego... Stay safe.", 1.5)
        sys.exit()
    else:
        print(f"{R}[!] Invalid choice / Pilihan tidak valid.{W}")
        time.sleep(1)
        set_language()

def hide_file():
    clear_screen()
    print_banner(redraw=True)
    spinner_anim(T['start_inj'], 2.0, show_ok=False)
    
    host_exts = ['.mp3', '.mp4', '.jpg', '.png', '.jpeg', '.txt']
    
    print(f"\n{C}[*]{W} {T['choose_fmt']}")
    for i, ext in enumerate(host_exts, 1):
        print(f"    {C}[{i}]{W} {ext}")
    print(f"    {C}[0]{W} {T['back_menu']}")
        
    try:
        pilihan_ext_str = input(f"\n{Y}[?]{W} {T['pick_fmt']} (0-{len(host_exts)}): ")
        if pilihan_ext_str.strip() == '':
            clear_screen()
            return
        pilihan_ext = int(pilihan_ext_str)
        
        if pilihan_ext == 0:
            clear_screen()
            return
        elif 1 <= pilihan_ext <= len(host_exts):
            selected_ext = host_exts[pilihan_ext - 1]
        else:
            print(f"{R}[!] {T['invalid']}{W}")
            time.sleep(1)
            clear_screen()
            return
    except ValueError:
        print(f"{R}[!] {T['must_num']}{W}")
        time.sleep(1)
        clear_screen()
        return

    clear_screen()
    print_banner(redraw=True)
    host_file = input(f"{Y}[?]{W} {T['path_host']} ({selected_ext}): ")
    
    if not os.path.exists(host_file):
        print(f"{R}[!] {T['err_404_file']} '{host_file}' {T['err_404_not_found']}{W}")
        input(f"\n{B}{T['press_enter']}{W}")
        clear_screen()
        return
        
    _, ext = os.path.splitext(host_file)
    if ext.lower() != selected_ext:
        print(f"{R}[!] {T['err_ext']} ({selected_ext} {T['req']}).{W}")
        input(f"\n{B}{T['press_enter']}{W}")
        clear_screen()
        return

    clear_screen()
    print_banner(redraw=True)
    zip_file = input(f"{Y}[?]{W} {T['path_zip']} ")
    
    if not os.path.exists(zip_file):
        print(f"{R}[!] {T['err_404_file']} '{zip_file}' {T['err_404_not_found']}{W}")
        input(f"\n{B}{T['press_enter']}{W}")
        clear_screen()
        return
        
    if not zip_file.lower().endswith('.zip'):
        print(f"{R}[!] {T['err_zip_fmt']}{W}")
        input(f"\n{B}{T['press_enter']}{W}")
        clear_screen()
        return

    clear_screen()
    print_banner(redraw=True)
    output_filename = input(f"{Y}[?]{W} {T['out_name']}{selected_ext}): ")

    output_dir = "Inject"
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, output_filename)

    print()
    progress_bar(T['proc'], 2.5)

    try:
        with open(host_file, 'rb') as f_host:
            host_data = f_host.read()
            
        with open(zip_file, 'rb') as f_zip:
            zip_data = f_zip.read()
            
        with open(output_file, 'wb') as f_out:
            f_out.write(host_data + zip_data)
            
        print(f"{G}[+] {T['inj_ok']}{W}")
        print(f"{G}[+] {T['inj_ok_msg']} '{os.path.abspath(output_file)}'{W}")
    except Exception as e:
        print(f"{R}[!] {T['sys_err']} {e}{W}")
        
    input(f"\n{B}{T['press_enter']}{W}")
    clear_screen()

def check_file():
    clear_screen()
    print_banner(redraw=True)
    print(f"{C}[*]{W} {T['start_chk']}")
    target_file = input(f"{Y}[?]{W} {T['path_tgt']} ")
    
    if not os.path.exists(target_file):
        print(f"{R}[!] {T['err_404_file']} '{target_file}' {T['err_404_not_found']}{W}")
        clear_screen()
        return
        
    clear_screen()
    print_banner(redraw=True)
    spinner_anim(T['scan_eocd'], 1.5)

    try:
        with zipfile.ZipFile(target_file, 'r') as z:
            file_list = z.namelist()
            print(f"\n{G}[+] {T['vuln']}{W}")
            print(f"{C}[*]{W} {T['hidden_list']}")
            for item in file_list:
                print(f"    {Y}->{W} {item}")
    except zipfile.BadZipFile:
        print(f"{R}[-] {T['neg']}{W}")

def extract_file():
    clear_screen()
    print_banner(redraw=True)
    print(f"{C}[*]{W} {T['start_ext']}")
    target_file = input(f"{Y}[?]{W} {T['tgt_ext']} ")
    
    if not os.path.exists(target_file):
        print(f"{R}[!] {T['err_404_file']} '{target_file}' {T['err_404_not_found']}{W}")
        clear_screen()
        return
        
    extract_dir = "Export"
    os.makedirs(extract_dir, exist_ok=True)
        
    clear_screen()
    print_banner(redraw=True)
    spinner_anim(T['exec_ext'], 1.5)

    try:
        with zipfile.ZipFile(target_file, 'r') as z:
            z.extractall(extract_dir)
            print(f"{G}[+] {T['ext_ok']}{W}")
            print(f"{G}[+] {T['ext_ok_msg']} {os.path.abspath(extract_dir)}{W}")
    except zipfile.BadZipFile:
        print(f"{R}[-] {T['ext_fail']}{W}")
    except Exception as e:
        print(f"{R}[!] {T['sys_err']} {e}{W}")

def main():
    clear_screen()
    
    while True:
        print_banner()
        
        print(f"    {C}[1]{W} {T['m1']}")
        print(f"    {C}[2]{W} {T['m2']}")
        print(f"    {C}[3]{W} {T['m3']}")
        print(f"    {C}[4]{W} {T['m4']}")
        print(f"    {C}[5]{W} {T['m5']}")
        
        sys.stdout.write(f"\n{B}> {W}")
        sys.stdout.flush()
        
        pilihan = ""
        last_refresh = time.time()
        
        while True:
            if time.time() - last_refresh >= 1.0:
                sys.stdout.write("\033[s")
                print_banner()
                sys.stdout.write("\033[u")
                sys.stdout.flush()
                last_refresh = time.time()

            if msvcrt.kbhit():
                char = msvcrt.getch()
                if char in b'\r\n':
                    print()
                    break
                elif char == b'\x08':
                    if len(pilihan) > 0:
                        pilihan = pilihan[:-1]
                        sys.stdout.write('\b \b')
                        sys.stdout.flush()
                else:
                    try:
                        decoded = char.decode('utf-8')
                        pilihan += decoded
                        sys.stdout.write(decoded)
                        sys.stdout.flush()
                    except UnicodeDecodeError:
                        pass
            
            time.sleep(0.02)
        
        if pilihan == '1':
            hide_file()
            clear_screen()
        elif pilihan == '2':
            check_file()
            input(f"\n{B}{T['press_enter']}{W}")
            clear_screen()
        elif pilihan == '3':
            extract_file()
            input(f"\n{B}{T['press_enter']}{W}")
            clear_screen()
        elif pilihan == '4':
            set_language()
            return
        elif pilihan == '5':
            print()
            spinner_anim(T['exit_msg'], 1.5)
            sys.exit()
        else:
            print(f"{R}[!] {T['cmd_err']}{W}")
            input(f"\n{B}{T['press_enter']}{W}")
            clear_screen()

if __name__ == "__main__":
    if os.name == 'nt':
        os.system('') 

    set_language()
    main()