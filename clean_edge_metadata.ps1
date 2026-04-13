# clean_edge_metadata.ps1
# Uruchom w katalogu repo. Tworzy kopie .bak przed modyfikacją.

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

# Wzorce do wyszukania (regex)
$patterns = @(
    "# User's Edge browser tabs metadata",
    "edge_all_open_tabs"
)

# Funkcje pomocnicze
function Log($m) { Write-Host "[INFO] $m" -ForegroundColor Cyan }
function Warn($m) { Write-Host "[WARN] $m" -ForegroundColor Yellow }
function Err($m)  { Write-Host "[ERROR] $m" -ForegroundColor Red }

# 1) Znajdź pliki zawierające wzorce
Log "Szukam plików zawierających metadane..."
$foundFiles = @()
foreach ($p in $patterns) {
    try {
        $res = git grep -l --no-color -e $p 2>$null
        if ($res) { $foundFiles += $res }
    } catch {
        # git grep zwraca kod błędu gdy brak wyników; ignorujemy
    }
}
$foundFiles = $foundFiles | Sort-Object -Unique

if (-not $foundFiles -or $foundFiles.Count -eq 0) {
    Log "Brak plików zawierających wskazane metadane. Kończę."
    exit 0
}

Log "Znaleziono pliki:"
$foundFiles | ForEach-Object { Write-Host " - $_" }

# 2) Dla każdego pliku: kopia zapasowa i oczyszczenie
foreach ($file in $foundFiles) {
    if (-not (Test-Path $file)) {
        Warn "Plik nie istnieje (pomiń): $file"
        continue
    }

    $bak = "$file.bak"
    Copy-Item -LiteralPath $file -Destination $bak -Force
    Log "Kopia zapasowa utworzona: $bak"

    $content = Get-Content -Raw -LiteralPath $file

    # Usuń wszystko od linii z "# User's Edge browser tabs metadata" do końca
    $content = $content -replace "(?s)# User's Edge browser tabs metadata.*$",""

    # Usuń bloki zaczynające się od "edge_all_open_tabs" do końca
    $content = $content -replace "(?s)edge_all_open_tabs\s*=\s*

\[.*$",""

    # Dodatkowo usuń pojedyncze linie zawierające fragmenty typu <WebsiteContent_...>
    $content = $content -replace "<WebsiteContent_[^>]*>",""

    # Trim i zapisz
    $content = $content.TrimEnd() + "`n"
    Set-Content -LiteralPath $file -Value $content -Encoding UTF8
    Log "Oczyszczono: $file"
}

# 3) Dodaj .gitattributes i .gitignore minimalne wpisy (jeśli brak)
if (-not (Test-Path ".gitattributes")) {
    @"
# Binary
*.exe binary
*.dll binary

# Text files
*.md text eol=crlf
*.ps1 text eol=crlf
*.sh text eol=lf
"@ | Set-Content -LiteralPath ".gitattributes" -Encoding UTF8
    Log "Utworzono .gitattributes"
} else {
    Log ".gitattributes już istnieje — pomijam tworzenie"
}

if (-not (Test-Path ".gitignore")) {
    @(
        ".gradle/",
        "build/",
        ".idea/",
        "*.iml",
        "*.bak"
    ) | Set-Content -LiteralPath ".gitignore" -Encoding UTF8
    Log "Utworzono .gitignore"
} else {
    Log ".gitignore już istnieje — pomijam tworzenie"
}

# 4) Ustaw core.autocrlf lokalnie i wymuś renormalizację
try { git config core.autocrlf true } catch {}
Log "Wymuszam renormalizację plików (git add --renormalize .)"
git add --renormalize .

# 5) Commit i push (bez przepisywania historii, jeśli możliwe)
git add -A
$porcelain = git status --porcelain
if (-not $porcelain) {
    Log "Brak zmian do zatwierdzenia po oczyszczeniu."
    exit 0
}

$commitMsg = "Remove accidental Edge browser metadata and normalize line endings"
git commit -m $commitMsg

Log "Próbuję wypchnąć zmiany do origin..."
try {
    git push origin
    Log "Push zakończony pomyślnie."
} catch {
    Warn "Standardowy push nie powiódł się. Próbuję ustawić upstream i wypchnąć z --force-with-lease..."
    $branch = (git rev-parse --abbrev-ref HEAD).Trim()
    if ($branch) {
        git push --force-with-lease --set-upstream origin $branch
        Log "Push z --force-with-lease wykonany."
    } else {
        Err "Nie udało się ustalić bieżącej gałęzi. Wypchnięcie wymaga ręcznej interwencji."
    }
}

Log "Zakończono. Kopie zapasowe plików znajdują się obok oryginałów z rozszerzeniem .bak"
