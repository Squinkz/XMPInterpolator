import math

# ============================================================ #
# ============================================================ #
#
#    easing functions borrowed (stolen) from Angel's Tween library
#      -- https://github.com/Angel-foxxo/TweenVS-source1/tree/main
#
#    which in turn was taken from
#      -- https://easings.net/
#
#    visual examples of easing behavior can be found at https://easings.net/
#
# ============================================================ #
# ============================================================ #

class Ease:

    @staticmethod
    def Linear(t):
        return t

    @staticmethod
    def EaseInSine(t):
        return 1.0 - math.cos((t * math.pi) / 2.0)

    @staticmethod
    def EaseOutSine(t):
        return math.sin((t * math.pi) / 2.0)

    @staticmethod
    def EaseInOutSine(t):
        return -(math.cos(math.pi * t) - 1.0) / 2.0

    @staticmethod
    def EaseInCubic(t):
        return t * t * t

    @staticmethod
    def EaseOutCubic(t):
        return 1.0 - math.pow(1.0 - t, 3.0)

    @staticmethod
    def EaseInOutCubic(t):
        return (4.0 * t * t * t) if t < 0.5 else (1.0 - math.pow(-2.0 * t + 2.0, 3.0) / 2.0)

    @staticmethod
    def EaseInQuint(t):
        return t ** 5

    @staticmethod
    def EaseOutQuint(t):
        return 1.0 - math.pow(1.0 - t, 5.0)

    @staticmethod
    def EaseInOutQuint(t):
        return (16.0 * t ** 5) if t < 0.5 else 1.0 - math.pow(-2.0 * t + 2.0, 5.0) / 2.0

    @staticmethod
    def EaseInCircle(t):
        return 1.0 - math.sqrt(1.0 - t * t)

    @staticmethod
    def EaseOutCircle(t):
        return math.sqrt(1.0 - (t - 1.0) ** 2)

    @staticmethod
    def EaseInOutCircle(t):
        return (1.0 - math.sqrt(1.0 - (2.0 * t) ** 2)) / 2.0 if t < 0.5 \
            else (math.sqrt(1.0 - (-2.0 * t + 2.0) ** 2) + 1.0) / 2.0

    @staticmethod
    def EaseInElastic(t):
        c4 = (2.0 * math.pi) / 3.0
        if t == 0:
            return 0.0
        if t == 1.0:
            return 1.0
        return -math.pow(2.0, 10.0 * t - 10.0) * math.sin((t * 10.0 - 10.75) * c4)

    @staticmethod
    def EaseOutElastic(t):
        c4 = (2.0 * math.pi) / 3.0
        if t == 0:
            return 0.0
        if t == 1.0:
            return 1.0
        return math.pow(2.0, -10.0 * t) * math.sin((t * 10.0 - 0.75) * c4) + 1.0

    @staticmethod
    def EaseInOutElastic(t):
        c5 = (2.0 * math.pi) / 4.5
        if t == 0:
            return 0.0
        if t == 1.0:
            return 1.0
        if t < 0.5:
            return -(math.pow(2.0, 20.0 * t - 10.0) * math.sin((20.0 * t - 11.125) * c5)) / 2.0
        return (math.pow(2.0, -20.0 * t + 10.0) * math.sin((20.0 * t - 11.125) * c5)) / 2.0 + 1.0

    @staticmethod
    def EaseInQuad(t):
        return t * t

    @staticmethod
    def EaseOutQuad(t):
        return 1.0 - (1.0 - t) * (1.0 - t)

    @staticmethod
    def EaseInOutQuad(t):
        return (2.0 * t * t) if t < 0.5 else 1.0 - math.pow(-2.0 * t + 2.0, 2.0) / 2.0

    @staticmethod
    def EaseInQuart(t):
        return t ** 4

    @staticmethod
    def EaseOutQuart(t):
        return 1.0 - math.pow(1.0 - t, 4.0)

    @staticmethod
    def EaseInOutQuart(t):
        return (8.0 * t ** 4) if t < 0.5 else 1.0 - math.pow(-2.0 * t + 2.0, 4.0) / 2.0

    @staticmethod
    def EaseInExpo(t):
        return 0.0 if t == 0 else math.pow(2.0, 10.0 * t - 10.0)

    @staticmethod
    def EaseOutExpo(t):
        return 1.0 if t == 1.0 else 1.0 - math.pow(2.0, -10.0 * t)

    @staticmethod
    def EaseInOutExpo(t):
        if t == 0:
            return 0.0
        if t == 1.0:
            return 1.0
        return math.pow(2.0, 20.0 * t - 10.0) / 2.0 if t < 0.5 else (2.0 - math.pow(2.0, -20.0 * t + 10.0)) / 2.0

    @staticmethod
    def EaseInBack(t):
        c1 = 1.70158
        c3 = c1 + 1.0
        return c3 * t ** 3 - c1 * t ** 2

    @staticmethod
    def EaseOutBack(t):
        c1 = 1.70158
        c3 = c1 + 1.0
        return 1.0 + c3 * (t - 1.0) ** 3 + c1 * (t - 1.0) ** 2

    @staticmethod
    def EaseInOutBack(t):
        c1 = 1.70158
        c2 = c1 * 1.525
        return (math.pow(2.0 * t, 2.0) * ((c2 + 1.0) * 2.0 * t - c2)) / 2.0 if t < 0.5 \
            else (math.pow(2.0 * t - 2.0, 2.0) * ((c2 + 1.0) * (t * 2.0 - 2.0) + c2) + 2.0) / 2.0

    @staticmethod
    def EaseInBounce(t):
        return 1.0 - Ease.EaseOutBounce(1.0 - t)

    @staticmethod
    def EaseOutBounce(t):
        n1 = 7.5625
        d1 = 2.75
        if t < 1.0 / d1:
            return n1 * t * t
        elif t < 2.0 / d1:
            t -= 1.5 / d1
            return n1 * t * t + 0.75
        elif t < 2.5 / d1:
            t -= 2.25 / d1
            return n1 * t * t + 0.9375
        else:
            t -= 2.625 / d1
            return n1 * t * t + 0.984375

    @staticmethod
    def EaseInOutBounce(t):
        return (1.0 - Ease.EaseOutBounce(1.0 - 2.0 * t)) / 2.0 if t < 0.5 \
            else (1.0 + Ease.EaseOutBounce(2.0 * t - 1.0)) / 2.0