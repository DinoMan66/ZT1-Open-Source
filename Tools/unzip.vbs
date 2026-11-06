' unzip.vbs <zipfile> <destfolder> - extracts with the Windows shell (no extra tools on XP)
Set fso = CreateObject("Scripting.FileSystemObject")
Set sh = CreateObject("Shell.Application")
src = fso.GetAbsolutePathName(WScript.Arguments(0))
dst = WScript.Arguments(1)
If Not fso.FolderExists(dst) Then fso.CreateFolder(dst)
Set items = sh.NameSpace(src).Items
n = items.Count
sh.NameSpace(dst).CopyHere items, 4 + 16 + 1024
Do While sh.NameSpace(dst).Items.Count < n
  WScript.Sleep 500
Loop
WScript.Sleep 3000
WScript.Echo "extracted " & n & " top-level items to " & dst
