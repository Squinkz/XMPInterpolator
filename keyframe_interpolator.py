import glob, re, sys
from easing import Ease
from title import Title

MODULE_NAME = "XMP Interpolator for Lightroom Develop Settings"
MODULE_VERSION = [1, 0]
MODULE_AUTHOR = 'Dieter "squink" Stassen'


def lerp(a, b, t):
    return a * (1.0 - t) + b * t


# fake enum
class Action:
    EASE = True
    SET  = False


class Parameter:
    def __init__(self, name, action = Action.EASE, actionData = Ease.Linear, namespace = "crs"):
        self.namespace = namespace
        self.name = name
        self.startValue = None
        self.endValue = None
        self.newValue = None
        self.action = action
        self.actionData = actionData
        if not self.Validate():
            err = "Incorrect data type for actionData.\nactionData must be a number for Action.SET, or an Ease function for Action.EASE"
            raise TypeError(err)

    def Validate(self):
        if self.action == Action.SET and not isinstance(self.actionData, (int, float)):
            return False
        elif self.action == Action.EASE and not callable(self.actionData):
            return False
        return True

    def GetValue(self, lines):
        pattern = re.compile(rf'{re.escape(self.namespace + ":" + self.name)}="(.*?)"')
        for line in lines:
            match = pattern.search(line)
            if match:
                return float(match.group(1))
        return None

    def SetValues(self, startLines, endLines):
        self.startValue = self.GetValue(startLines)
        self.endValue   = self.GetValue(endLines)


class KeyframeInterpolator:

    log = None

    @staticmethod
    def Confirm(files):
        fileAmount = len(files)
        msg = (f"""\nInterpolate metadata for {fileAmount} files?

    "{files[0]}" [0]
        ... ...
        ... ...
    "{files[fileAmount - 1]}" [{fileAmount - 1}]
""")
        KI.log.PrintLog(msg)
        print("")
        inp = input("|| Proceed? (y/n)\t: ").lower()
        return inp in ["y", "1"]

    @staticmethod
    def InsertParameter(content, name, value):

        block = re.search(r"<rdf:Description\b[^>]*>", content)
        if not block:
            return content

        start, end = block.span()
        modified = block.group(0)[:-1] + f'\n   {name}="{value}">'
        content = content[:start] + modified + content[end:]

        return content

    @staticmethod
    def ReplaceParameterValue(file, parameters):

        with open(file, 'r') as f: content = f.read()

        for parameter in parameters:
            name = parameter.namespace + ":" + parameter.name
            value = f"{float(parameter.newValue):.2f}" if name == "crs:Exposure2012" else f"{int(parameter.newValue)}"
            if name == "crs:Temperature":
                content, success = re.subn("crs:WhiteBalance" + '=".*"', "crs:WhiteBalance" + '="Custom"', content, count = 1)
                if not success:
                    content = KI.InsertParameter(content, "crs:WhiteBalance", "Custom")
            content, success = re.subn(name + '=".*"', name + '="' + value + '"', content, count = 1)
            if not success:
                content = KI.InsertParameter(content, name, value)

        with open(file, 'w') as f: f.write(content)

    @staticmethod
    def InterpolateKeyframes(files, startKey, endKey, parameters):

        KI.log.PrintLogLine()
        KI.log.PrintLogTime(f"Reading frame {startKey} to frame {endKey}...")

        with open(files[startKey], 'r') as f: startLines = f.read().splitlines()
        with open(files[endKey],   'r') as f: endLines   = f.read().splitlines()

        for parameter in parameters:
            parameter.SetValues(startLines, endLines)

            if parameter.startValue == None:
                err = f'Parameter "{parameter.name}" was not found in XMP file for keyframe {startKey}'
                KI.log.PrintLogError(err)
                sys.exit()
            if parameter.endValue == None:
                err = f'Parameter "{parameter.name}" was not found in XMP file for keyframe {endKey}'
                KI.log.PrintLogError(err)
                sys.exit()

            KI.log.PrintLogLine()
            KI.log.PrintLog(f'"{parameter.name}" first value is {parameter.startValue}')
            KI.log.PrintLog(f'"{parameter.name}" final value is {parameter.endValue}')

        for i in range(startKey, endKey):
            KI.log.PrintLogLine()
            t = (i - startKey) / (endKey - startKey)
            for parameter in parameters:
                if parameter.action == Action.EASE:
                    parameter.newValue = lerp(parameter.startValue, parameter.endValue, parameter.actionData(t))
                    KI.log.PrintLogTime(f'Interpolated "{parameter.name}" for frame {i} to {parameter.newValue:.2f}')
                else:
                    parameter.newValue = parameter.actionData
                    KI.log.PrintLogTime(f'Set "{parameter.name}" for frame {i} to {parameter.actionData}')

            KI.ReplaceParameterValue(files[i], parameters)
            KI.log.PrintLogTime(f'Wrote XMP for frame {i}')

        KI.log.PrintLogLine()
        KI.log.PrintLogBar()

    @staticmethod
    def Run(settings, logger, confirmed = False):

        KI.log = logger

        print(Title(MODULE_NAME, MODULE_VERSION, MODULE_AUTHOR))
        KI.log.Log(Title(MODULE_NAME, MODULE_VERSION, MODULE_AUTHOR, clamp = False))

        files = sorted(glob.glob(settings["directory"] + "/*.xmp"))

        if not len(files):
            err = f"No XMP files found in {settings["directory"]}"
            KI.log.PrintLogError(err)
            sys.exit()

        keyframes = settings["keyframes"]

        if len(keyframes) < 2:
            err = "Keyframe list has fewer than 2 keyframes"
            KI.log.PrintLogError(err)
            sys.exit()

        for i, keyframe in enumerate(keyframes):
            if keyframe < 0 or keyframe > len(files) - 1:
                err = f"Keyframe index is out of bounds [index: {i}, value: {keyframe}]\n||\t\tOnly values 0 - {len(files) - 1} are valid"
                KI.log.PrintLogError(err)
                sys.exit()

        if confirmed or KI.Confirm(files):

            KI.log.PrintLogLine()
            KI.log.PrintLogTime(f"Beginning interpolation for {len(files)} files...")
            KI.log.PrintLogLine()
            KI.log.PrintLogBar()

            for i in range(len(keyframes) - 1):
                KI.InterpolateKeyframes(files, keyframes[i], keyframes[i + 1], settings["parameters"])

            KI.log.PrintLogLine()
            KI.log.PrintLogTime("Interpolation complete")
            KI.log.PrintLogLine()
            KI.log.PrintLogBar()
            KI.log.PrintLogBar()

            return True

        else:
            return False

KI = KeyframeInterpolator