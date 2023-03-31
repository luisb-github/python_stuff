#NoEnv
SendMode Input
SetWorkingDir %A_ScriptDir%

SendInput, ^c
ClipWait
file_paths := Clipboard
FileAppend, %file_paths%, *, UTF-8

ExitApp