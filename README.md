# Simpleclip
Simpleclip (sclip) is a simple command interface for text-only (for now) clipboard history managing, functional for X11  (for now).
Simpleclip is built in python, using the cli toolkit [Click](https://github.com/pallets/click). It does not have any additional dependencies.
It does not access the system clipboard by itself, so it is thought as a complementary tool to combine with xclip in X11, wl-clipboard in Wayland or other similar tools.

## Install
The package may be installed from this git repository using `pip` or `pipx`. You can use any of these three commands depending on your needs:
```sh
pip install git+https://github.com/Padelvi/simpleclip
pip install --user git+https://github.com/Padelvi/simpleclip
pipx install git+https://github.com/Padelvi/simpleclip
```
If you are interested in installing Simpleclip for development, the easiest approach is to clone the repository. For that purposes, a Conda environment file is provided.

In addition to the program, it is recommended to install 

## Usage

### Useful aliases
As wew have mentioned, simpleclip does not access any system clipboard directly. Instead, it is designed to work with two commands: `fzf` to display and select clipboard entries, and `xclip`, to copy and obtain entries. Support for `xsel` and wayland similar tools is not available yet.
To integrate the three commands, 

### Shell completion
For shell completion, refer to [this click docs guide](https://click.palletsprojects.com/en/stable/shell-completion/) for your shell of choice, using `sclip` as the program name.

## Files and configuration
