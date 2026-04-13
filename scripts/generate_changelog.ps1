$log = git log --pretty=format:"* %s (%h)" --no-merges
Set-Content -Path CHANGELOG.md -Value "# Changelog

$log"
