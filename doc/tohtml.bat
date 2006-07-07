xcopy /Y /S /I ..\demo\*.py html\demo
xcopy /Y /I ..\COPYING html\COPYING.txt
rst2chtml --raw-enabled --no-xml-declaration --no-section-subtitles --file-insertion-enabled --no-generator -v --stylesheet=css/python.css --link-stylesheet index.rst html/index.html
