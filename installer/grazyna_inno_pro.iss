#define MyAppName "GRAZYNA DIAGNOSTIC SUITE"
#define MyAppExeName "GRAZYNA_DIAGNOSTIC_SUITE.exe"
#define MyAppVersion "0.2.0"

[Setup]
AppName={#MyAppName}
AppVersion={#MyAppVersion}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
OutputBaseFilename=GRAZYNA_DIAGNOSTIC_SUITE_Inno_Installer_PRO
Compression=lzma
SolidCompression=yes

[Files]
Source: "..\release\GRAZYNA_DIAGNOSTIC_SUITE.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\source\plugins\*"; DestDir: "{app}\plugins"; Flags: recursesubdirs ignoreversion

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{commondesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Uruchom GRAZYNA DIAGNOSTIC SUITE PRO"; Flags: nowait postinstall skipifsilent
