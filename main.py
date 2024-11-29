from tkinter import filedialog, messagebox
import os
from pathlib import Path
from zipfile import ZipFile
import subprocess
import json
import re
import shutil
import requests as req

def folder_organizer(steamcmd_exe_path, jogo, jogo_modsfolder_path, mod):
    downloaded_mods_path = f"{Path(steamcmd_exe_path).parent.resolve()}/steamapps/workshop/content/{jogo}"

    os.system(f"clear")
    os.system(f"COLOR 9")
    os.system('echo Todos os mods foram baixados com sucesso!')

    if os.path.exists(downloaded_mods_path):
        subfolders = [f for f in os.listdir(downloaded_mods_path) if os.path.isdir(os.path.join(downloaded_mods_path, f))]
            
        for subfolder in subfolders:
            source_path = os.path.join(downloaded_mods_path, subfolder)
            destination_mod_path = os.path.join(jogo_modsfolder_path, subfolder)
            
            os.system(f"clear")
            os.system(f"COLOR D")
            os.system(f"echo Movendo {source_path} para {destination_mod_path}")
            try:
                shutil.move(source_path, destination_mod_path)
                os.system(f"clear")
                os.system(f"COLOR 9")
                os.system(f'Mod {mod} movido com sucesso\n para a pasta {jogo_modsfolder_path}')

            except Exception as exc:
                os.system(f"clear")
                os.system(f"COLOR 4")
                os.system(f"echo Erro ao mover {subfolder}: {exc}")
    else:
        os.system(f"clear")
        os.system(f"COLOR 4")
        os.system(f"echo A pasta para o mod {mod} não foi encontrada.")

def execution(steamcmd_exe_path):
    jogo = str(input("Para qual jogo quer instalar mods? [Link da Página na Steam]\n"))

    #Obter nome do jogo
    nome_jogo = re.search(r'/app/\d+/([^/]+)/', jogo).group(1)
  
    #Obter código do jogo na pag steam
    jogo = re.findall(r'\d+', jogo)
    jogo = [int(num) for num in jogo][0]

    while os.path.isdir(jogo_modsfolder_path:=input(f"Qual o caminho para a pasta de mods do {nome_jogo}?\n")) is False:
        pass

    mods = []

    print("Quais mods você quer instalar? [Digite 'Sair' para fechar.]")
    while True:
        mod = re.findall(r'\d+', question:=str(input("Link do mod na Steam: ")))
        
        if mod:
            mod = int(mod[0])

        if question.lower() == 'sair':
            break

        mods.append(mod)

    os.system(f"clear") 
    os.system("COLOR 9")
    os.system(f"echo Os seguintes mod serão instalados: {mods}")

    for mod in mods:
        try:
            process = subprocess.Popen(
                [steamcmd_exe_path, 
                 "+login anonymous", 
                 f"+workshop_download_item {jogo} {mod}",
                 "+quit",
                 "+exit",
                 "+shutdown",
                 ], shell=True)
            
        except subprocess.CalledProcessError as exc:
            messagebox.showerror(title='ERRO', message=exc)
        
        finally:
            folder_organizer(steamcmd_exe_path, jogo, jogo_modsfolder_path, mod)
    
def unzip(steamcmd_zip_path):
    with ZipFile(steamcmd_zip_path, 'r') as zip_ref:
        zip_ref.extractall(path=(steamcmd_folder_path:=Path(steamcmd_zip_path).parent.resolve()))
        zip_ref.close()
    os.remove(steamcmd_zip_path)
    
    execution(steamcmd_exe_path:=fr"{steamcmd_folder_path}/steamcmd.exe")

    with open(r"C:\SMD.json", "w+", encoding="utf-8") as file:
        json.dump({"steamcmd_path": steamcmd_exe_path}, file)
        file.close()

def get_steamcmd():
    with req.request(stream=True, timeout=None, method='GET', url="https://steamcdn-a.akamaihd.net/client/installer/steamcmd.zip") as r:
        #print(r.raise_for_status(), r.headers, len(r.content))
        with open(steamcmd_zip_path:=f"{filedialog.asksaveasfilename(initialdir=os.getcwd, title='Selecione o local para download', filetypes=[('Zip File', '*.zip')], defaultextension='.zip')}", 'wb') as f:
            f.write(r.content)
            #print(steamcmd_path)
            f.close()

        r.close()

    unzip(steamcmd_zip_path)

def start():
    if os.path.isfile(steamcmd_exe_path:=r"C:\SMD.json"):
        with open(steamcmd_exe_path, "r", encoding="utf-8") as file:
            data = json.load(file)
        if os.path.isfile(data.get("steamcmd_path", "")):
            return execution(data["steamcmd_path"])
    else:    
        entry = "Você possui o SteamCMD? [S/N]\n"
        
        if (resposta:=input(entry).lower()) == "n":
            get_steamcmd()

        elif resposta == "s":
            while os.path.isfile(path:=input("Qual o caminho para o arquivo steamcmd.exe?\n")) is False:
                pass
            
            with open(r"C:\SMD.json", "w+", encoding="utf-8") as file:
                json.dump({"steamcmd_path": path}, file)
                file.close()
                execution(path)

        else:
            start()

start()
