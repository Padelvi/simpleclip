# Simpleclip
Simpleclip (sclip) is a simple command interface for text-only (for now) clipboard history managing, adaptable for X11 or Wayland.
Simpleclip is built in python, using the cli toolkit [Click](https://github.com/pallets/click). It does not have any additional dependencies.
It does not access the system clipboard by itself, so it is thought as a complementary tool to combine with xclip or xsel in X11, wl-clipboard in Wayland or other similar tools. In general, any cli tool which can copy the selected content from stdin and output the clipboard content to stdout should be functional.

## Install
The package may be installed from this git repository using `pip` or `pipx`. You can use any of these three commands depending on your needs:
```sh
pip install git+https://github.com/Padelvi/simpleclip
pip install --user git+https://github.com/Padelvi/simpleclip
pipx install git+https://github.com/Padelvi/simpleclip
```
If you are interested in installing Simpleclip for development, the easiest approach is to clone the repository. For that purposes, a Conda environment file is provided. To make testing easier, you can make an alias like:
```sh
alias sclip="python3 -m sclip.main"
```
Which would work when executed from the repository root folder.

In addition to the program, `fzf` (installable [here](https://github.com/junegunn/fzf)) is required as a dependency.

## Usage

### Watcher
Section pending.

### Useful aliases
As we have mentioned, simpleclip modifies the system clipboard by using any command (xclip by default) that can copy and paste from it, communicating through stdin and stdout. It is designed to work with `fzf` to display and select clipboard entries in the terminal. The commands for copying and pasting should be written in the config file.

It is recommended to use aliases in the terminal, which combine sclip commands with fzf to directly have the main functions available in your terminal:
```sh
alias clp="sclip list | fzf | sclip format | sclip copy"
alias cld="sclip list | fzf | sclip delete"
alias clw="sclip wipe"
```

### Shell completion
For shell completion, refer to [this click docs guide](https://click.palletsprojects.com/en/stable/shell-completion/) for your shell of choice, using `sclip` as the program name.

## Files and configuration
Section pending.