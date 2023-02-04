
# bright-wallpaper-killer

*This is a straightforward bash script that does not eliminate or erase any wallpaper, but instead, it moves wallpapers with high white color percentages (25%) or high brightness (80 mean) to a designated container located in the current directory.*

https://user-images.githubusercontent.com/96896184/216736436-8a1bad99-47f1-4afc-ac46-93dc1d7dbb6a.mp4

## Explanations
The script operates mainly with two variables: mean and white_percent.
 - mean
    With the usage of the command `identify -verbose 0001.png | grep "mean" | awk '{print $2}' ` you can extract see the valuers for the color's intensity (RGB). 
    High colors = high brightness. I set a limit of 80 on [this line](https://github.com/U-L-M-S/bright-wallpaper-killer/blob/main/killer.sh#L21)
    
  - white_percent
     The percentage of white color in a picture can be extracted using the command `convert "$file" -format "%[fx:mean*100]" info:`. The script is very strict and only allows for 25% of the picture to be white. [line](https://github.com/U-L-M-S/bright-wallpaper-killer/blob/main/killer.sh#L28) 
    

## Requirements
The requirements necessary to run this script are `find`, `wc`, `identify`, `awk`, `bc` and they can be easily installed with:
### Debian based version:
```bash
sudo apt update
sudo apt install -y imagemagick bc
```
### Arch based version:
```bash
sudo pacman -Syu imagemagick bc
```

## Usage
To use this script, you need to do three steps:\
1- clone
`git clone https://github.com/U-L-M-S/bright-wallpaper-killer` \
2- move
`mv bright-wallpaper-killer/killer.sh move/to/your/wallpapers/path`\
3- execute
`./killer.sh`\

If you get any error like "**permission denied**" or something like this. Try to `chmod +x killer.sh`


## Tests
This script was used and tested on `bash` and `zsh` shells


