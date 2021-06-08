from manim import *
import numpy as np
import math


class Proof(Scene):
    def construct(self):
        paper_left = -5
        paper_right = 5
        paper_bottom = -2
        paper_top = 2

        # lines
        line_bottom = Line([paper_left, paper_bottom, 0], [
            paper_right, paper_bottom, 0])
        line_top = Line([paper_left, paper_top, 0], [
            paper_right, paper_top, 0])
        self.add(line_bottom, line_top)

        #line dist
        line_dist_brace = BraceBetweenPoints([-4, paper_bottom, 0], [-4, paper_top, 0], direction=[-1, 0, 0])
        line_dist_brace_text = line_dist_brace.get_tex("1")
        line_group = VGroup(line_dist_brace, line_dist_brace_text)
        self.play(Write(line_group))


        # needle
        needle_len = 4
        center = [1, .5, 0]
        center_proj = [center[0], paper_top, 0]
        angle = math.pi/6
        transform = [math.cos(angle)*needle_len/2,
                    math.sin(angle)*needle_len/2, 0]
        needle_left = [a-b for a, b in zip(center, transform)]
        needle_right = [a+b for a, b in zip(center, transform)]
        needle = Line(needle_left, needle_right).set_color(RED)
        self.play(Create(needle))

        #needle len label ###############FIX
        needle_len_brace = BraceBetweenPoints(needle_left, needle_right, direction=needle.copy().rotate(PI/2).get_unit_vector())
        needle_len_text = needle_len_brace.get_tex("1")
        self.play(Write(needle_len_brace), Write(needle_len_text))
        self.remove(needle_len_brace, needle_len_text)
        self.wait()

        # distance from center to line
        dist_brace = BraceBetweenPoints(center, center_proj, direction=[-1, 0, 0])
        dist_brace_text = dist_brace.get_tex("d")
        self.play(Write(dist_brace), Write(dist_brace_text))

        # right angle
        base_line = Line(center, [needle_right[0], center[1], 0])
        side_line = Line([needle_right[0], center[1], 0], needle_right)
        angle = Angle(base_line, needle, radius=.8)
        angle_label = MathTex(r"\theta ").scale(0.8).next_to(angle, RIGHT).shift(UP*0.08)
        self.play(Create(base_line), Create(side_line), Create(angle), Write(angle_label))

        # right angle side label
        angle_label = MathTex(r"\frac{1}{2} \sin \theta ").scale(0.8).next_to(side_line, RIGHT)
        self.play(Write(angle_label))
        
        # move the diagram to the right
        diagram_shift = 3
        new_line_bottom = Line([paper_left+diagram_shift, paper_bottom, 0], [
            paper_right, paper_bottom, 0])
        new_line_top = Line([paper_left+diagram_shift, paper_top, 0], [
            paper_right, paper_top, 0])
        self.play(Transform(line_bottom, new_line_bottom), Transform(line_top, new_line_top), line_group.animate.shift(RIGHT*diagram_shift))
