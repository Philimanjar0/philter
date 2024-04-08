# set the name of the installer
Outfile "install_philter.exe"
 
InstallDir "C:\Program Files\philter" ; $InstDir default value
RequestExecutionLevel Admin

Page Directory
Page InstFiles

Section
SetOutPath "$InstDir"
File "convert_philter.exe"
WriteRegStr HKCR "SystemFileAssociations\.philter\shell\Convert to .filter\command" "" "$InstDir\convert_philter.exe $\"%1$\""
WriteUninstaller "$INSTDIR\uninstall.exe"
WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\philter" \
                 "DisplayName" "philter"
WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\philter" \
                 "UninstallString" "$\"$INSTDIR\uninstall.exe$\""
SectionEnd

Section "uninstall"
    Delete $InstDir\uninstall.exe
    Delete $InstDir\convert_philter.exe
    DeleteRegKey HKCR "SystemFileAssociations\.philter"
    DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\philter"
    RMDir $InstDir
SectionEnd