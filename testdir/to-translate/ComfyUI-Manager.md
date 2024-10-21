# ComfyUI Manager

**ComfyUI-Manager** is an extension designed to enhance the usability of [ComfyUI](https://github.com/comfyanonymous/ComfyUI). It offers management functions to **install, remove, disable, and enable** various custom nodes of ComfyUI. Furthermore, this extension provides a hub feature and convenience functions to access a wide range of information within ComfyUI.

![menu](misc/menu.jpg)

## NOTICE

- V2.48.1: Security policy has been changed. Downloads of models in the list are allowed under the 'normal' security level.
- V2.47: Security policy has been changed. The former 'normal' is now 'normal-', and 'normal' no longer allows high-risk features, even if your ComfyUI is local.
- V2.37 Show a ✅ mark to accounts that have been active on GitHub for more than six months.
- V2.33 Security policy is applied.
- V2.21 [cm-cli](docs/en/cm-cli.md) tool is added.
- V2.18 to V2.18.3 is not functioning due to a severe bug. Users on these versions are advised to promptly update to V2.18.4. Please navigate to the `ComfyUI/custom_nodes/ComfyUI-Manager` directory and execute `git pull` to update.
- You can see whole nodes info on [ComfyUI Nodes Info](https://ltdrdata.github.io/) page.

## Installation

### Installation[method1] (General installation method: ComfyUI-Manager only)

To install ComfyUI-Manager in addition to an existing installation of ComfyUI, you can follow the following steps:

1. goto `ComfyUI/custom_nodes` dir in terminal(cmd)
2. `git clone https://github.com/ltdrdata/ComfyUI-Manager.git`
3. Restart ComfyUI

### Installation[method2] (Installation for portable ComfyUI version: ComfyUI-Manager only)

1. install git

- https://git-scm.com/download/win
- standalone version
- select option: use windows default console window

2. Download [scripts/install-manager-for-portable-version.bat](https://github.com/ltdrdata/ComfyUI-Manager/raw/main/scripts/install-manager-for-portable-version.bat) into installed `"ComfyUI_windows_portable"` directory
3. double click `install-manager-for-portable-version.bat` batch file

![portable-install](misc/portable-install.png)

### Installation[method3] (Installation through comfy-cli: install ComfyUI and ComfyUI-Manager at once.)

> RECOMMENDED: comfy-cli provides various features to manage ComfyUI from the CLI.

- **prerequisite: python 3, git**

Windows:

```commandline
python -m venv venv
venv\Scripts\activate
pip install comfy-cli
comfy install
```

Linux/OSX:

```commandline
python -m venv venv
. venv/bin/activate
pip install comfy-cli
comfy install
```

[translate]
