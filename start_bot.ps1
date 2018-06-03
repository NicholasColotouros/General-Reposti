#credit to KeikakuB for this script

$FILE = 'bot.pid'
# Kill the bot if needed
Try
{
    $ID = Get-Content -Path $FILE
    Stop-Process -Id $ID
}
Catch
{
    $_.Exception.Message
}
# Start the bot
$app = Start-Process -passthru -nonewwindow python general-reposti.py
# Store its pid in 'bot.pid' file
echo $app.Id > $FILE