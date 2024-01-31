import PyInstaller.__main__

PyInstaller.__main__.run([
    'DesignFolderTool_AcrylicV2.4.py',
    '--clean',
    '--onedir',
    '--contents-directory=.',
    '--windowed',
    '--noconfirm',
    '--add-data=icon;icon',
    '--add-data=paths.txt;.',
    '--icon=icon/search.ico',
    '--name=Design Folder Tool - AcrylicV2.4',
])