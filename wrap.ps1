$machineStatsPath = 'C:\Users\Tidal\Downloads\machine_stats-master\machine_stats-master\windows'
$measurementsPath  = 'C:\Users\Tidal\Downloads\machine-stats-measurements-script-main\machine-stats-measurements-script-main'
$userName = 'tidaldemo.com\Tidal'
$CpuUtilizationTimeout = 1

cd $machineStatsPath
& ("$machineStatsPath\runner.ps1") -UserName $userName -CpuUtilizationTimeout $CpuUtilizationTimeout > "$measurementsPath/stats.json"
cd $measurementsPath
& python "$measurementsPath\script.py" 
