from manim import *
import numpy as np
import math


class Intro(Scene):
    def construct(self):
        big_pi = MathTex("\\pi").scale(10)
        self.play(Write(big_pi))