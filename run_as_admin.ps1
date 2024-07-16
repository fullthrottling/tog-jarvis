# 관리자 권한으로 실행하는지 확인
$myWindowsID = [System.Security.Principal.WindowsIdentity]::GetCurrent()
$myWindowsPrincipal = New-Object System.Security.Principal.WindowsPrincipal($myWindowsID)
$adminRole = [System.Security.Principal.WindowsBuiltInRole]::Administrator

if (-Not ($myWindowsPrincipal.IsInRole($adminRole))) {
    # 관리자 권한으로 스크립트를 다시 실행
    Start-Process powershell.exe -ArgumentList "Start-Process powershell.exe -ArgumentList 'python src/main.py' -Verb RunAs" -Verb RunAs
    exit
} else {
    python src/main.py
}
