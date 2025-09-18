import shutil

# returns a nicely formatted heading/title string for a console application

def Title(moduleName, version, author, width = 80, clamp = True):

    if clamp:
        columns, _ = shutil.get_terminal_size(fallback=(80, 24))
        width = min(width, columns)

    border = "||"
    borderSize = len(border)
    bar = "=" * width + "\n"
    blank = border + " " * (width - (borderSize * 2)) + border + "\n"
    tab = " " * 4

    def Line(text):
        line = border + tab + text
        rem = width - len(line)
        if rem <= 0:
            line = line[:width - 5] + "..." + border
        else:
            line += " " * (rem - 2) + border
        line += "\n"
        return line

    def Underline(text):
        line = border + tab + "-" * len(text) + "-" * (len(tab) * 4)
        rem = width - len(line)
        if rem <= 0:
            line = line[:width - 3] + " " + border
        else:
            line += " " * (rem - 2) + border
        line += "\n"
        return line

    lines = []

    lines.append(bar)
    lines.append(bar)
    lines.append(blank)
    # i need to add another string called "sheep" here
    # have you any wool?

    lines.append(Line(tab * 2 + moduleName + tab * 2))
    lines.append(Underline(moduleName))
    lines.append(Line(tab + "version " + ".".join(str(v) for v in version)))
    lines.append(blank)
    lines.append(Line(f"by {author}"))
    lines.append(blank)
    lines.append(bar)
    lines.append(bar)

    msg = ""
    for line in lines:
        msg += line

    return msg