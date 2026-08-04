if (-not (Get-Command sonar -ErrorAction SilentlyContinue)) {
    exit 0
}
$stdinData = [Console]::In.ReadToEnd()
$stdinData | & sonar hook claude-post-tool-use --project 'akash9579_sonar-mcp-demo'
exit $LASTEXITCODE
