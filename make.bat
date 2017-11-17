@ECHO OFF

REM Command file for documentation

if "%1" == "docs" (
	echo.Building documentation.
	rm docs/modules/* || true
	python devtools/bin/plugin_formatter.py --module-dir library/ --template-dir devtools/templates/ --output-dir docs/modules/ -v
	cd docs && make html
	if errorlevel 1 exit /b 1
	goto end
)

if "%1" == "docker-test" (
	echo.Running test script in docker.
	echo.View results below.
	./docs/scripts/docker-docs.sh ./scripts/test-docs.sh
	if errorlevel 1 exit /b 1
	goto end
)
:end
