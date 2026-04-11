[Setup]
AppName=Grazyna MAX PRO
AppVersion=1.0
DefaultDirName={pf}\Grazyna_MAX_PRO
DefaultGroupName=Grazyna MAX PRO
OutputBaseFilename=Grazyna_MAX_PRO_Installer

[Files]
Source: "dist\grazyna_max_pro.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\libusb-1.0.dll"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Grazyna MAX PRO"; Filename: "{app}\grazyna_max_pro.exe"
