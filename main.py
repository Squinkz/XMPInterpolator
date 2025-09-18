from keyframe_interpolator import Parameter, Action, KeyframeInterpolator
from xmp_extractor import XMPExtractor
from easing import Ease
from print_and_log import Logger
import os

# ============================================================ #
# ============================================================ #

settings = {

    # ============================================================ #
    # directory (string)
    # ============================================================ #
    # location of images or xml files on disk
    # paste the folder path between the quotes
    # don't remove the first 'r'
    #
    #   eg: r"C:\Pictures\TimelapseFrames",
    #
    # ============================================================ #
    "directory":
        r"C:\Pictures\TimelapseFrames",

    # ============================================================ #
    # parameters (list of Parameter)
    # ============================================================ #
    # a list of parameters to interpolate or set.
    # if only the parameter name is specified, linear interpolation is used
    # else, a different easing function can be specified.
    # a list of easing function names can be found in easing.py
    #
    # instead of interpolating, the value can be instead be set to a constant value
    #       (use either Action.EASE to interpolate or Action.SET to set a parameter)
    #
    #   examples:
    #
    #       linear interpolation between keyframes for temperature:
    #
    #               Parameter("crs:Temperature"),
    #
    #
    #       quadratic interpolation between keyframes for temperature:
    #
    #               Parameter("crs:Temperature", Action.EASE, Ease.EaseInQuad),
    #           or
    #               Parameter("crs:Temperature", actionData = Ease.EaseInQuad),
    #
    #
    #       set all temperature values to 5500k:
    #
    #               Parameter("crs:Temperature", Action.SET, 5500)
    #
    #
    #     Note: Develop setting keys should all live in the crs namespace.
    #           this script will prepend "crs:" to all keys. alternate namespaces
    #           can be specified in the constructor
    #
    #       eg. Parameter("SomeKey", namespace = "abc"),
    #
    #           though this should not be necessary for Lightroom XMLs
    # ============================================================ #
    "parameters":
    [
        Parameter("Temperature"),
        Parameter("Tint", Action.SET, -17),
        Parameter("Exposure2012", actionData = Ease.EaseInOutQuad),

        # Basic:
        # Parameter("Temperature"),
        # Parameter("Tint"),
        # Parameter("Exposure2012"),
        # Parameter("Contrast2012"),
        # Parameter("Highlights2012"),
        # Parameter("Shadows2012"),
        # Parameter("Whites2012"),
        # Parameter("Blacks2012"),
        # Parameter("Texture"),
        # Parameter("Clarity2012"),
        # Parameter("Dehaze"),
        # Parameter("Vibrance"),
        # Parameter("Saturation"),

        # Tone Curve
        # Parameter("ParametricShadows"),
        # Parameter("ParametricDarks"),
        # Parameter("ParametricLights"),
        # Parameter("ParametricHighlights"),
        # Parameter("ParametricShadowSplit"),
        # Parameter("ParametricMidtoneSplit"),
        # Parameter("ParametricHighlightSplit"),

        # Detail:
        # Parameter("Sharpness"),
        # Parameter("SharpenRadius"),
        # Parameter("SharpenDetail"),
        # Parameter("SharpenEdgeMasking"),
        # Parameter("LuminanceSmoothing"),
        # Parameter("ColorNoiseReduction"),
        # Parameter("ColorNoiseReductionDetail"),
        # Parameter("ColorNoiseReductionSmoothness"),

        # Color Mixer
        # Parameter("HueAdjustmentRed"),
        # Parameter("HueAdjustmentOrange"),
        # Parameter("HueAdjustmentYellow"),
        # Parameter("HueAdjustmentGreen"),
        # Parameter("HueAdjustmentAqua"),
        # Parameter("HueAdjustmentBlue"),
        # Parameter("HueAdjustmentPurple"),
        # Parameter("HueAdjustmentMagenta"),
        # Parameter("SaturationAdjustmentRed"),
        # Parameter("SaturationAdjustmentOrange"),
        # Parameter("SaturationAdjustmentYellow"),
        # Parameter("SaturationAdjustmentGreen"),
        # Parameter("SaturationAdjustmentAqua"),
        # Parameter("SaturationAdjustmentBlue"),
        # Parameter("SaturationAdjustmentPurple"),
        # Parameter("SaturationAdjustmentMagenta"),
        # Parameter("LuminanceAdjustmentRed"),
        # Parameter("LuminanceAdjustmentOrange"),
        # Parameter("LuminanceAdjustmentYellow"),
        # Parameter("LuminanceAdjustmentGreen"),
        # Parameter("LuminanceAdjustmentAqua"),
        # Parameter("LuminanceAdjustmentBlue"),
        # Parameter("LuminanceAdjustmentPurple"),
        # Parameter("LuminanceAdjustmentMagenta"),

        # other parameters are available and able to be interpolated,
        # such as crop, split toning etc.
        # not all, though. check your xmp files in a text editor
        # for parameter names and their data types.
        # ONLY floats and integers can be interpolated.
        # other data types can be used if using Action.SET
    ],

    # ============================================================ #
    # keyframes (list of int)
    # ============================================================ #
    # a list of keyframe indices in the image sequence
    # the list is zero-indexed, so the first image is index 0,
    # second image is index 1, third is index 2 etc.
    # ============================================================ #
    "keyframes":
        [0, 50, 100, 250],

    # ============================================================ #
    # extractXMPfromImages (bool)
    # ============================================================ #
    # whether the script should extract metadata from the image files
    # and write that to external XML files. This is needed if your raw
    # files are DNG or DNG-based (such as GPR - GoPro Raw), since
    # lightroom doesn't write XML sidecars for those files and
    # instead embeds the metadata in the image itself
    # ============================================================ #
    "extractXMPfromImages":
        True,

    # ============================================================ #
    # imageExtension (string)
    # ============================================================ #
    # the file extension of your images.
    # only needed if "extractXMPfromImages" is set to True
    # ============================================================ #
    "imageExtension":
        "gpr",

}


# ============================================================ #
# ============================================================ #


def ValidateDirectory(dir):
    if not os.path.exists(dir):
        err = f'Input setting "directory": {dir} does not exist'
        raise FileNotFoundError(err)
    if not os.path.isdir(dir):
        err = f'Input setting "directory": {dir} is not a directory'
        raise NotADirectoryError(err)


if (__name__ == "__main__"):

    ValidateDirectory(settings["directory"])

    log = Logger(settings["directory"], "interpolator")

    confirmed = False

    if settings["extractXMPfromImages"]:
        confirmed = XMPExtractor.Run(settings, log)

    KeyframeInterpolator.Run(settings, log, confirmed)

    log.Close()