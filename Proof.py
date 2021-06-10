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
            [-5, paper_bottom, 0], [-5, paper_top, 0], direction=[-1, 0, 0])
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
        diagram_shift = 4
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
        area = MathTex("\\text{Total area} =", " (\\frac{k}{2})(\\pi)", " = ", "{k", "\\pi", "\\over 2}}").scale(
            0.8).move_to(left_origin+DOWN*1.5)
        group.add(prob, integral, area)
        self.play(AnimationGroup(
            *[Write(x) for y in [prob, integral, area] for x in y], lag_ratio=1))
        self.play(group.animate.move_to([-3.5, 2, 0]).scale(.8))

        # making simpler probability equation
        simple_prob = MathTex("p", "=", "{\\text{Desired}", "\\over", "\\text{Total}}").move_to(left_origin + DOWN + LEFT)
        self.play(TransformFromCopy(prob, simple_prob))
        
        # filling in desired
        uneval_ex = MathTex("=", "{l", "\\over", "{k", "\\pi", "\\over 2}}").next_to(simple_prob, RIGHT)
        self.play(Write(uneval_ex.get_part_by_tex("=")))
        self.play(Indicate(integral), Indicate(simple_prob.get_part_by_tex("{\\text{Desired}")))
        self.play(TransformFromCopy(integral[-1], uneval_ex.get_part_by_tex("l")))
        self.play(Write(uneval_ex.get_part_by_tex("\\over")))

        self.play(Indicate(area), Indicate(simple_prob.get_part_by_tex("\\text{Total}}")))
        self.play(AnimationGroup(TransformFromCopy(area.get_parts_by_tex("{k")[1], uneval_ex.get_part_by_tex("{k")), 
                                TransformFromCopy(area.get_parts_by_tex("\\pi")[1], uneval_ex.get_part_by_tex("\\pi")), 
                                TransformFromCopy(area.get_part_by_tex("\\over 2"), uneval_ex.get_part_by_tex("\\over 2}}")), lag_ratio=0))
        self.wait(0.5)
        # simplification
        eval_ex = MathTex("=", "{2", "l", "\\over", "k", "\\pi}").next_to(simple_prob, RIGHT)
        self.play(AnimationGroup(Transform(uneval_ex.get_part_by_tex("="), eval_ex.get_part_by_tex("=")),
                                Transform(uneval_ex.get_part_by_tex("{l"), eval_ex.get_part_by_tex("l")),
                                Transform(uneval_ex.get_part_by_tex("{k"), eval_ex.get_part_by_tex("k")),
                                Transform(uneval_ex.get_part_by_tex("\\pi"), eval_ex.get_part_by_tex("\\pi")),
                                Transform(uneval_ex.get_part_by_tex("\\over 2"), eval_ex.get_part_by_tex("{2")),
                                Transform(uneval_ex.get_part_by_tex("\\over"), eval_ex.get_part_by_tex("\\over"))), lag_ratio=0.5)
        
        # replacing a few objects with one object
        pre_ex = MathTex("p", "=", "{\\text{Desired}", "\\over", "\\text{Total}}", "=", "{2", "l", "\\over", "k", "\\pi}").align_to(simple_prob, LEFT).align_to(simple_prob, UP)

        final_ex = MathTex("p", "=", "{2", "l", "\\over", "k", "\\pi}").move_to(ORIGIN)

        # make sure everything is aligned before resetting
        for x in range(0, 6):
            pre_ex[x+5].move_to(eval_ex[x].get_center())

        # remove everything
        animations = []
        n_objs = 0
        for mobj in self.get_top_level_mobjects():
            # horrible hard coding, couldnt figure out how else to keep pre_ex
            if len(mobj) < 5 or len(mobj) > 6:
                animations.append(FadeOut(mobj))
            n_objs += 1
        self.play(AnimationGroup(*animations, lag_ratio=0))
        self.clear()
        self.add(pre_ex)
        self.wait()
        
        # create transforms for every component, also unwrite desired/total
        animations = []
        for x in range(0, 7):
            if x == 0:
                animations.append(Transform(pre_ex.get_part_by_tex("p"), final_ex[0]))
            if 1 <= x <= 4:
                animations.append(Unwrite(pre_ex[x]).set_run_time(0.4))
            if x >= 1:
                animations.append(Transform(pre_ex[x+4], final_ex[x]))
        self.play(AnimationGroup(*animations, lag_ratio=0))
        self.add(final_ex)
        self.wait(1)
        return final_ex

    def draw_conclusion(self, final_ex):
        # solve for pi
        self.play(Swap(final_ex.get_part_by_tex("p"), final_ex.get_part_by_tex("pi}")))
        self.wait(1)

        # shift up
        self.play(final_ex.animate.shift(UP))
        knl = Tex("Set $k$ equal to $l$").next_to(final_ex, DOWN)
        self.play(Write(knl))
        self.wait(1)

        # plug in
        rewritten_eq = MathTex("\\pi", "=", "{2", "\\over", "p}").shift(UP)

        # rearrange        
        self.play(AnimationGroup(FadeOut(knl), 
                                Transform(final_ex.get_part_by_tex("\\pi"), rewritten_eq.get_part_by_tex("\\pi")),
                                Transform(final_ex.get_part_by_tex("="), rewritten_eq.get_part_by_tex("=")),
                                Transform(final_ex.get_part_by_tex("{2"), rewritten_eq.get_part_by_tex("2")),
                                Transform(final_ex.get_part_by_tex("p"), rewritten_eq.get_part_by_tex("p}")),
                                Transform(final_ex.get_part_by_tex("\\over"), rewritten_eq.get_part_by_tex("\\over")),
                                FadeOut(final_ex.get_part_by_tex("l")),
                                FadeOut(final_ex.get_part_by_tex("k"))), lag_ratio=0)
        
        # definition of p
        p_words = MathTex("p = {\\text{\\# of intersections} \\over \\text{\\# of drops}}").shift(DOWN*.5)
        self.play(Write(p_words))
        self.wait(1)

        # fade out everything
        animations = []
        for mobj in self.get_top_level_mobjects():
            animations.append(FadeOut(mobj))
        self.play(AnimationGroup(*animations, lag_ratio=0))