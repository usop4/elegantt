import os

def detectfont():
    import glob
    fontdirs = [
        '/usr/share/fonts',
        '/Library/Fonts',
        '/System/Library/Fonts',
        'c:/windows/fonts',
        '/usr/local/share/font-*',
    ]
    fontfiles = [
        'ipaexg.ttf',
        'DejaVuSans.ttf',
        'NotoSansCJK-Regular.ttc',
    ]

    fontpath = None
    globber = (glob.glob(d) for d in fontdirs)
    for fontdir in sum(globber, []):
        for root, _, files in os.walk(fontdir):
            for font in fontfiles:
                if font in files:
                    fontpath = os.path.join(root, font)
                    break

    return fontpath


if __name__ == '__main__':
    print("utils.py")
