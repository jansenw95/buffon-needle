from manim import *
import numpy as np
import math

class Equation(Scene):
    def construct(self):
        equation = MathTex(r"\int _{0}^{\pi}\frac{1}{2}\sin\theta = \frac{\pi}{2}")
        self.play(Write(equation))
        # equation2 = MathTex(r"\int _{0}^{\pi}\frac{1}{2}\sin\theta = \frac{\pi}{2}")
        # self.play(Transform(equation, equation2))