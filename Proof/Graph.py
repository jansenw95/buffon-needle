from manim import *
import numpy as np
import math


class Graph(Scene):
    def construct(self):
        origin = np.array([-4, -1.5, 0])

        # axis
        axes = Axes(
            x_range=[0, PI, PI/4],
            y_range=[0, .5, .1],
            x_length=8,
            y_length=3,
            tips=False
        )
        labels = axes.get_axis_labels(
            x_label=MathTex(r"\theta"),
            y_label=MathTex(r"d")
        )
        self.play(Create(axes), Create(labels))

        # axis labels
        x_labels = ["0", r"\frac{\pi}{4}", r"\frac{\pi}{2}", r"\frac{3\pi}{4}", r"\pi"]
        x_text = VGroup()
        for i in range (5):
            label = MathTex(x_labels[i]).move_to(origin + RIGHT*2*i + DOWN*0.5).scale(0.5)
            x_text.add(label)
        self.play(Write(x_text))
        
        y_labels = ["0", "0.1", "0.2", "0.3", "0.4", "0.5"]
        y_text = VGroup()
        for i in range (6):
            label = MathTex(y_labels[i]).move_to(origin + UP*.6*i + LEFT*.5).scale(0.5)
            y_text.add(label)
        self.play(Write(y_text))

        # graph the function
        curve = axes.get_graph(lambda x: np.sin(x)/2, color=BLUE)
        area = axes.get_area(curve)
        self.play(Create(curve))
        self.play(Create(area))