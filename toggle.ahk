SendMode("Input")  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir(A_ScriptDir)  ; Ensures a consistent starting directory.

; Define the paths to your executables
CameraAppPath := "D:\source\ComputerVision\ip_camera_streaming\dist\rtsp.exe"
FlutterAppPath := "D:\source\ComputerVision\ip_camera_streaming\HMI_09_06_2024\flutter_application_1.exe"

; Start the Flutter app maximized
Run(FlutterAppPath)
WinWait("ahk_exe flutter_application_1.exe")  ; Wait until the Flutter app is active
WinMaximize("ahk_exe flutter_application_1.exe")  ; Maximize the Flutter app

; Introduce a small delay to ensure Flutter app is fully loaded
Sleep(2000)  ; Wait for 2 seconds (2000 milliseconds) to ensure Flutter is fully maximized

; Start rtsp.exe minimized
Run(CameraAppPath, , "Min")  ; Run rtsp.exe minimized in the background

; Define the F1 key to toggle between the apps
F1::
{
    if WinActive("ahk_exe flutter_application_1.exe")  ; If the Flutter app is active
    {
        WinMinimize("ahk_exe flutter_application_1.exe")  ; Minimize the Flutter app
        WinRestore("ahk_exe rtsp.exe")  ; Restore and activate rtsp.exe
        WinActivate("ahk_exe rtsp.exe")
        WinMaximize("ahk_exe rtsp.exe")
    }
    else  ; If rtsp.exe is active
    {
        WinMinimize("ahk_exe rtsp.exe")  ; Minimize rtsp.exe
        WinRestore("ahk_exe flutter_application_1.exe")  ; Restore and activate the Flutter app
        WinActivate("ahk_exe flutter_application_1.exe")
        WinMaximize("ahk_exe flutter_application_1.exe")
    }
}
return
