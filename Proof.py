from manim import *
import numpy as np
import math


class Proof(Scene):
    def construct(self):
        # drawing diagram
        diagram = Group()
        self.draw_diagram(diagram)
        self.clear()
        self.add(diagram)
        self.play(diagram.animate.shift(RIGHT*2, UP*2).scale(0.8))

        # making graph
        graph = Group()
        self.draw_graph(graph)
        self.clear()
        self.add(graph, diagram)
        self.play(graph.animate.move_to([3.5, -2, 0]).scale(0.6))

        # making equation
        equation = self.draw_equation()
        self.clear()
        self.add(equation)

        # conclusion
        self.draw_conclusion(equation)

    def draw_diagram(self, group):
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

        # line dist
        line_dist_brace = BraceBetweenPoints(
            [-4, paper_bottom, 0], [-4, paper_top, 0], direction=[-1, 0, 0])
        line_dist_brace_text = line_dist_brace.get_tex("k")
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
        group.add(needle)

        # needle len label
        needle_len_brace = BraceBetweenPoints(
            needle_left, needle_right, direction=needle.copy().rotate(PI/2).get_unit_vector())
        needle_len_text = needle_len_brace.get_tex("l")
        self.play(Write(needle_len_brace), Write(needle_len_text))
        self.play(FadeOut(needle_len_brace), FadeOut(needle_len_text))
        self.wait()

        # distance from center to line
        dist_brace = BraceBetweenPoints(
            center, center_proj, direction=[-1, 0, 0])
        dist_brace_text = dist_brace.get_tex("d")
        self.play(Write(dist_brace), Write(dist_brace_text))
        group.add(dist_brace, dist_brace_text)

        # right angle
        base_line = Line(center, [needle_right[0], center[1], 0])
        side_line = Line([needle_right[0], center[1], 0], needle_right)
        angle = Angle(base_line, needle, radius=.8)
        angle_label = MathTex(r"\theta ").scale(
            0.8).next_to(angle, RIGHT).shift(UP*0.08)
        self.play(Create(base_line), Create(side_line),
                  Create(angle), Write(angle_label))
        group.add(base_line, side_line, angle, angle_label)

        # right angle side label
        angle_label = MathTex(r"\frac{l}{2} \sin \theta ").scale(
            0.8).next_to(side_line, RIGHT)
        self.play(Write(angle_label))
        group.add(angle_label)

        # shift left brace right
        diagram_shift = 3
        new_line_bottom = Line([paper_left+diagram_shift, paper_bottom, 0], [
            paper_right, paper_bottom, 0])
        new_line_top = Line([paper_left+diagram_shift, paper_top, 0], [
            paper_right, paper_top, 0])
        self.play(Transform(line_bottom, new_line_bottom), Transform(
            line_top, new_line_top), line_group.animate.shift(RIGHT*diagram_shift))
        group.add(new_line_bottom, new_line_top, line_group)

    def draw_graph(self, group):
        origin = np.array([-1.5, -1, 0])

        # axis
        axes = Axes(
            x_range=[0, PI, PI/4],
            y_range=[0, .7, .1],
            x_length=8,
            y_length=4,
            tips=False,
            axis_config={
                "stroke_width": 4.0
            }
        ).shift(origin)
        labels = axes.get_axis_labels(
            x_label=MathTex(r"\theta"),
            y_label=MathTex(r"d")
        )
        self.play(Create(axes), Create(labels))
        group.add(axes, labels)

        # axis labels
        x_labels = ["0", r"\frac{\pi}{4}",
                    r"\frac{\pi}{2}", r"\frac{3\pi}{4}", r"\pi"]
        x_text = []
        for i in range(len(x_labels)):
            label = MathTex(x_labels[i], ).shift(
                origin + LEFT*3.95 + DOWN*2.5 + RIGHT*2*i).scale(0.7)
            x_text.append(label)
        self.play(AnimationGroup(*[Write(x) for x in x_text], lag_ratio=0))

        y_labels = [0, 5, 7]
        y_text = [MathTex("0").shift(origin + LEFT*4.5 + DOWN*2).scale(0.7),
                  MathTex("\\frac{l}{2}").shift(origin + LEFT*4.5 +
                                                DOWN * 2 + UP*4/7*5).scale(0.7),
                  MathTex("\\frac{k}{2}").shift(origin + LEFT *
                                                4.5 + DOWN*2 + UP*4).scale(0.7),
                  ]
        self.play(AnimationGroup(*[Write(y) for y in y_text], lag_ratio=0))
        group.add(*x_text, *y_text)

        # write equation
        label = MathTex("d ", "\\leq \\frac{l\\sin\\theta}{2}").shift(origin)
        self.play(Write(label[0]))
        self.play(Write(label[1]))
        self.play(label.animate.scale(0.8).shift(.6*UP+3*RIGHT))
        group.add(label)

        # graph the function
        curve = axes.get_graph(lambda x: np.sin(x)/2, color=BLUE)
        area = axes.get_area(curve, color=BLUE)
        self.play(Create(curve))

        # dashed line
        dashed_line = DashedLine(
            origin + LEFT*4 + DOWN*2 + UP*2.9, 
            origin + DOWN*2 + RIGHT*.05 + UP*2.9, 
            dash_length=0.3, dash_spacing=0.15, color=YELLOW)
        self.play(Create(dashed_line, reversed=True))
        group.add(dashed_line)

        # adding the area
        self.play(Create(area))
        group.add(curve, area)

    def draw_equation(self):
        group = Group()
        # constructing full equations
        left_origin = [-3, 0, 0]
        prob = MathTex("\\text{Probability of intersection}", "\\\=", "{\\text{Desired area}",
                       "\\over", "\\text{Total area}}").scale(0.8).move_to(left_origin + UP*1.5)
        integral = MathTex("\\text{Area under curve} =", " \\int", "_{0}^{\\pi}",
                           "{l\\over 2}", "\\sin \\theta", " =", "l").scale(0.8).move_to(left_origin)
        area = MathTex("\\text{Total area} =", " (\\frac{k}{2})", "(\\pi)", " = ", "\\frac{k\\pi}{2}").scale(
            0.8).move_to(left_origin+DOWN*1.5)
        group.add(prob, integral, area)
        self.play(AnimationGroup(
            *[Write(x) for y in [prob, integral, area] for x in y], lag_ratio=1))
        self.play(group.animate.move_to([-3.5, 2, 0]).scale(.8))

        # making simpler probability equation
        simple_prob = MathTex("p", "=", "{\\text{Desired}", "\\over", "\\text{Total}}").move_to(left_origin + DOWN + LEFT)
        self.play(TransformFromCopy(prob, simple_prob))
        
        # filling in desired
        uneval_ex = MathTex("=", "{l", "\\over", "\\frac{k \\pi}{2}}").next_to(simple_prob, RIGHT)
        self.play(Write(uneval_ex.get_part_by_tex("=")))
        self.play(Indicate(integral), Indicate(simple_prob.get_part_by_tex("{\\text{Desired}")))
        self.play(TransformFromCopy(integral[-1], uneval_ex.get_part_by_tex("l")))
        self.play(Write(uneval_ex.get_part_by_tex("\\over")))

        self.play(Indicate(area), Indicate(simple_prob.get_part_by_tex("\\text{Total}}")))
        self.play(TransformFromCopy(area.get_part_by_tex("\\frac{k\\pi}{2}"), uneval_ex.get_part_by_tex("\\frac{k \\pi}{2}}")))

        # simplification
        eval_ex = MathTex("=", "\\frac{2l}{k\\pi}").next_to(simple_prob, RIGHT)
        self.play(Transform(uneval_ex[1:], eval_ex[1]))
        
        # replacing a few objects with one object
        pre_ex = MathTex("p", "=", "{\\text{Desired}", "\\over", "\\text{Total}}", "= \\frac{2l}{k\\pi}").align_to(simple_prob, LEFT).align_to(simple_prob, UP)
        self.clear()
        self.add(pre_ex)
        self.wait()

        # 
        final_ex = MathTex("p", " = \\frac{2l}{k", "\\pi}").move_to(ORIGIN)
        self.play(Transform(pre_ex, final_ex))
        return final_ex

    def draw_conclusion(self, final_ex):
        # solve for pi
        self.play(Swap(final_ex.get_part_by_tex("p"), final_ex.get_part_by_tex("pi}")))

        # shift up
        self.play(final_ex.animate.shift(UP))
        knl = MathTex("k, l = 1").next_to(final_ex, DOWN)
        self.play(Write(knl))
        
        # plug in
        rewritten_eq = MathTex("\\pi = \\frac{2}{p}").shift(UP)
        self.play(FadeOut(knl), Transform(final_ex, rewritten_eq))
        
        # definition of p
        p_words = MathTex("p = {\\text{\\# of intersections} \\over \\text{\\# of drops}}").shift(DOWN*.5)
        self.play(Write(p_words))
        return Group(rewritten_eq, p_words)
