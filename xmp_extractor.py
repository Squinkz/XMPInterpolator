import os, glob, subprocess
from title import Title

MODULE_NAME = "Metadata Extractor"
MODULE_VERSION = [1, 0]
MODULE_AUTHOR = 'Dieter "squink" Stassen'

# this module just calls exiftool and asks it to do all the hard work

class XMPExtractor:

    log = None

    @staticmethod
    def Confirm(files, ext):
        fileAmount = len(files)
        XE.log.PrintLog(f"""\nExtract metadata to XMP for {fileAmount} images?

    "{files[0]}" [0]
        ... ...
        ... ...
    "{files[fileAmount - 1]}" [{fileAmount - 1}]

WARNING:    This will overwrite any existing XMP files
            associated with a .{ext} file
""")
        print("")
        inp = input("|| Proceed? (y/n)\t: ").lower()
        return inp in ["y", "1"]

    @staticmethod
    def ExtractMetadataToXMP(dir, ext):

        for file in glob.glob(os.path.join(dir, f"*.{ext}")):
            xmp = os.path.splitext(file)[0] + ".xmp"
            if os.path.exists(xmp):
                os.remove(xmp)

        command = [
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "exiftool.exe"),
            "-tagsfromfile", "%d%f." + ext,
            "-xmp",
            "-ext", ext,
            "-o", "%d%f.xmp",
            dir
        ]

        XE.log.PrintLogLine()
        XE.log.PrintLogTime("Extracting metadata and writing XMP files...")

        result = subprocess.run(command, capture_output = True, text = True)

        if result.returncode == 0:
            XE.log.PrintLogTime("XMP extraction complete:")
            XE.log.PrintLogLine()
            XE.log.PrintLog(result.stdout)
        else:
            XE.log.PrintLogTime("Error running exiftool:")
            XE.log.PrintLogLine()
            XE.log.PrintLog(result.stderr)
        XE.log.PrintLogBar()

    @staticmethod
    def Run(settings, logger, confirmed = False):

        XE.log = logger

        print(Title(MODULE_NAME, MODULE_VERSION, MODULE_AUTHOR))
        XE.log.Log(Title(MODULE_NAME, MODULE_VERSION, MODULE_AUTHOR, clamp = False))

        files = sorted(glob.glob(os.path.join(settings["directory"], "*." + settings["imageExtension"])))

        if not len(files):
            err = f"No {settings["imageExtension"]} files found in {settings["directory"]}"
            XE.log.PrintLogError(err)
            return False

        if confirmed or XE.Confirm(files, settings["imageExtension"]):
            XE.ExtractMetadataToXMP(settings["directory"], settings["imageExtension"])
            return True
        else:
            XE.log.PrintLog("\nExtraction cancelled\n")
            XE.log.PrintLogBar()
            return False

XE = XMPExtractor