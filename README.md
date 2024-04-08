# philter
Path of Exile filter creation tool. First pass with functionality. Adds the ability to use simple variables to reduce copying many. the .philter filetype is converted into the typical .filter file used by the game.

No error checking. Be careful if you are relying on this in game. If you mess up, it will probably just dump out a garbage file.

## Installation
Download and run the installer from the [releases](https://github.com/Philimanjar0/philter/releases/latest). This will add a windows context menu on right click to automatically convert the .philter to .filter.

## Uninstallation
To uninstall, you can either:
- In Add or Remove Programs (in Windows) search for `philter` and unistall.
- Run the uninstaller directly. It is added to your chosen install directory.

## Editor
I recommend using vscode with the .filter plugin developed by Neversink. This will work for both .filter and .philter files.
https://marketplace.visualstudio.com/items?itemName=NeverSink.poe-filter-language

## Usage
### Editing the file
Declare variables in .philter with 
```
$var_name = {
    contents
}
```
Then the value within the curly braces will replace any instance of `%var_name`. Note the usages of `$` and `%`.
### Converting the file
Either:
- Right click on the file and select `convert to .filter`
- `.\convert_philter.exe your_file.philter`

## Example
Id like to use the same styling for multiple filter blocks. Id like maps and currency to both be stylized the same way, but if I want to change the styling, I dont want to have to change multiple blocks. 

Example .philter file
```
$test = {
    SetFontSize 40
    SetTextColor 0 0 0
    SetBorderColor 0 0 0
    SetBackgroundColor 0 0 0
}

Show
    Class "Maps"
    %test

Show
    Class "Stackable Currency"
    %test
```
converts to this .filter
```
Show
    SetFontSize 40
    SetTextColor 0 0 0
    SetBorderColor 0 0 0
    SetBackgroundColor 0 0 0
```

## Building
Building the executable (requires pyinstaller)
- `.\build.bat`
- alternatively: `pyinstaller --onefile .\src\convert_philter.py`
Building the installer (requires NSIS)
- NSIS > compose NSI scripts > your_script.nsi
