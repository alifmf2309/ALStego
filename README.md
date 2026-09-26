# ALStego (Beta Version) 1.0.0  

ALStego is a Command Line Interface (CLI) based File Steganography Toolkit written in pure Python. It is designed to inject `.ZIP` payload files into various host file formats (such as `.mp3`, `.mp4`, `.jpg`, `.png`, `.txt`) without the need for complex third-party libraries.

---

## Key Features
1. Binary ZIP Injection :
  Securely inserts ZIP files into binary host files.
2. Extension & EOCD Analysis :
  Scans and detects hidden ZIP payloads (*End of Central Directory*) inside host files.
3. Payload Extraction :
  Automatically extracts hidden data back into the `Export` folder.
4. Real-Time Telemetry Banner :
  Displays live device information (Hostname, MAC Address, Local IP, Public IP, automatic Timezone via GeoIP, and a responsive time display).
5. Dual Language Support :
  Supports interactive Indonesian and English.
6. Zero External Dependencies :
  Built using Python's built-in libraries, making it lightweight and can be run directly without installing heavy additional modules.

---

## Requirements

Make sure your computer has Python 3.14 or the latest version installed.

---

## How to Use The Program

1. Download the Repository

Choose one of the methods below:
* Using Git (run this command in a terminal/command prompt) :
```bash
[root@localhost ~]# git clone https://github.com/alifmf2309/ALStego.git
```
* Download directly through this GitHub repository page.

#

2. Enter the Project Directory
Open a terminal or command prompt, then navigate to the cloned or extracted project folder :
```bash
[root@localhost ~]# cd ALStego
```

#

3. Run The Program
```bash
[root@localhost ALStego]# python main.py
```
---

## Documentation
1. Language Menu
   > This is the initial menu. You must select the language you wish to use, but if you do not wish to continue, you can exit the program.
<p align=center>
  <img width="741" height="381" alt="Language" src="https://github.com/user-attachments/assets/58d61701-128d-4cf8-a5a5-8a4b94b570b2" />
</p>

#

2. Indonesian Menu
   > The following is a display of the menu in Indonesian.
<p align=center>
  <img width="741" height="381" alt="ID" src="https://github.com/user-attachments/assets/04999005-f66d-4d89-94c4-78e68c020705" />
</p>

#

3. English Menu
   > The following is a display of the menu in English.
<p align=center>
  <img width="741" height="381" alt="ENG" src="https://github.com/user-attachments/assets/5a86ee21-9d84-43f1-8c05-60cd1cd09b4b" />
</p>
