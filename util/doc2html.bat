rem xcopy /Y /S /I ..\demo\*.py ..\doc\html\demo
xcopy /Y /I ..\COPYING.txt ..\doc\html\COPYING.txt
rst2chtml.py ../doc/index.rst ../doc/html/index.html
