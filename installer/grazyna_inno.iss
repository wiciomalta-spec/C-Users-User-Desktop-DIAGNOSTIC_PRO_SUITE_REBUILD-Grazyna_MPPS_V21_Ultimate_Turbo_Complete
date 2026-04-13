#define MyAppName "GRAZYNA DIAGNOSTIC SUITE"
#define MyAppExeName "GRAZYNA_DIAGNOSTIC_SUITE.exe"
#define MyAppVersion "0.1.0"

[Setup]
AppName={#MyAppName}
AppVersion={#MyAppVersion}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
OutputBaseFilename=GRAZYNA_DIAGNOSTIC_SUITE_Inno_Installer
Compression=lzma
SolidCompression=yes

[Files]
Source: "..\release\GRAZYNA_DIAGNOSTIC_SUITE.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{commondesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Uruchom GRAZYNA DIAGNOSTIC SUITE"; Flags: nowait postinstall skipifsilent
