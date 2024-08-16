"""
Figuring out layout system in GNOME
"""
import subprocess


def getActiveLayout() -> str:
    layout = 'usss'
    command = ['gsettings',
               'get',
               'org.gnome.desktop.input-sources',
               'mru-sources']
    
    try:
        result = subprocess.run(command,
                                capture_output=True,
                                text=True,
                                check=True).stdout
        print(result)
        result = result.split("'")
        result = [x for x in result if x != 'xkb' and x[0].isalpha()]
        layout = result[0]
    except Exception as e:
        print('Something went wrong')
        print(e)

    return layout


if __name__ == '__main__':
    layout = getActiveLayout()
    print(layout)
