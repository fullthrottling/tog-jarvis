# config 폴더 안에 있는 모든 JSON 파일을 변환
$files = Get-ChildItem -Path .\config\*.json

foreach ($file in $files) {
    # 파일 이름만 추출 (확장자 제거)
    $filename = [System.IO.Path]::GetFileNameWithoutExtension($file)
    
    # quicktype을 사용하여 변환된 Python 파일을 src/jsons에 저장
    npx quicktype -o "src/jsons/$filename.py" --python "$file"
}
