# [Bad Apple!!](https://www.youtube.com/watch?v=FtutLA63Cp8&list=RDFtutLA63Cp8&start_radio=1) Terminal

Essentially a Sunday project fueled by my Touhou love and Diwali holiday snacks; a terminal-based rendition of the classic **Bad Apple!** shadow video from the *Touhou Project*. This plays a video on the CLI as ASCII art with synced audio!

## Installation
1. Clone this repository:
   
```bash
git clone https://github.com/AbhinavMangalore16/badapple-terminal.git
cd badapple-terminal
``` 

2. Install dependencies:
```bash 
pip install -r requirements.txt
```

3. Run the script:
```bash
python badapple_terminal/player.py
```
## Python Package:
You can install **Bad Apple!! Terminal** directly from PyPI (once uploaded) using:
```bash 
pip install badapple-terminal
```

After installation, you can run the CLI anywhere using:
```bash
badapple_terminal
```
### A word of caution:
It might be that above command may not be recognized, so make sure you have Python installed (>=3.8) and your Python Scripts directory is in your PATH. For example in PowerShell, you can temporarily add this:
#### Temporary: 
```bash
$env:Path += ";C:\Users\<YourUsername>\AppData\Roaming\Python\Python313\Scripts"
```
However, this change is temporary and applies only to the current PowerShell session. For a permanent solution, update your system environment variables via Windows Settings, like so:

#### Permanently: 
1. Press Win + S, search Environment Variables, open Edit the system environment variables.
2. Click Environment Variables…
3. Under User variables, select Path → Edit → New
4. Add:
   ```makefile
   C:\Users\<YourUsername>\AppData\Roaming\Python\Python313\Scripts
   ```
5. Then, Click OK to save. You are good to go! 


## Credits and Acknowledgements

- Original Animation: [Alstroemeria Records](https://alst.net/) (Bad Apple!! MV)
- Source/Game Video: [Touhou Project (ZUN)](https://en.touhouwiki.net/wiki/ZUN)
- Video Courtesy: https://www.youtube.com/watch?v=FtutLA63Cp8&list=RDFtutLA63Cp8&start_radio=1
- Conversion ASCII logic (for refined grainy rendering): https://github.com/kiteco/python-youtube-code/blob/master/ascii/ascii_convert.py

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.