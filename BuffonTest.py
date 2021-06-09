from manim import *
import math
import random
import numpy as np

# set random seed for consistency 
random.seed(2)  

intersect = 0
total = 0
pi_estimate = 0

class BuffonTest(Scene):
    def construct(self):
        global intersect, total, pi_estimate
        paper_left = -1.5
        paper_right = 6.5
        paper_bottom = -3
        paper_top = 3
        num_paper_lines = 5 # >1

        # formula for calculating pi  only works if needle_len <= paper_spacing
        needle_len = (paper_top - paper_bottom)/(num_paper_lines - 1)
        paper_spacing = (paper_top - paper_bottom)/(num_paper_lines - 1)

        # initialize text
        total_var = MathTex("n", "=")
        hit_var = MathTex("k", "=")

        pi_num = DecimalNumber(0,
                                num_decimal_places=5,
                                include_sign=False,
                                unit=None,
                                show_ellipsis=True
                                )
        pi_num.add_updater(lambda d: d.set_value(pi_estimate))
        total_num = Integer(0,
                            include_sign=False,
                            unit=None)
        total_num.add_updater(lambda d: d.set_value(total))
        hit_num = Integer(0,
                            include_sign=False,
                            unit=None)
        hit_num.add_updater(lambda d: d.set_value(intersect))

        total_var.move_to(6*LEFT + 3*UP)
        total_num.move_to(5.27*LEFT + 3.02*UP)
        hit_var.move_to(6*LEFT + 2.35*UP)
        hit_num.move_to(5.27*LEFT + 2.33*UP)

        line_group = VGroup()
        for x in reversed(range(num_paper_lines)):
            line = Line([paper_left, paper_bottom + paper_spacing*x, 0], 
                        [paper_right, paper_bottom + paper_spacing*x,0]).set_color(WHITE)
            line_group.add(line)
        self.play(Create(line_group, lag_ratio=0.1))   

        self.wait(2)

        self.play(AnimationGroup(Write(total_var), Write(total_num), lag_ratio=0.4))
        self.play(AnimationGroup(Write(hit_var), Write(hit_num), lag_ratio=0.4))

        self.wait(1)

        self.play(Indicate(total_var.get_part_by_tex("n"), scale_factor=1.5))

        self.wait(2)

        self.play(Indicate(hit_var.get_part_by_tex("k"), scale_factor=1.5))

        def draw_needles(num_needles, fade, time=0):
            global intersect, total, pi_estimate

            for _ in range(num_needles):
                # get random point that will be the center of the line, also keep line from sticking outside paper for aesthetics
                point_x = random.uniform(paper_left + needle_len/2, paper_right - needle_len/2)
                point_y = random.uniform(paper_bottom + needle_len/2, paper_top - needle_len/2)

                # calculate the closest distance between the point and a gridline
                closest_dist = min(point_y - (paper_bottom + paper_spacing*math.floor((point_y - paper_bottom)/paper_spacing)), 
                                   paper_bottom + paper_spacing*math.ceil((point_y - paper_bottom)/paper_spacing) - point_y)
                
                angle = random.random()*math.pi            
                needle = Line([point_x - math.cos(angle)*needle_len/2, point_y - math.sin(angle)*needle_len/2, 0], 
                            [point_x + math.cos(angle)*needle_len/2, point_y + math.sin(angle)*needle_len/2, 0])
                
                # check for intersection
                if closest_dist <= math.sin(angle)*needle_len/2:
                    needle.set_color(RED) 
            
                if fade:
                    self.play(FadeIn(needle, scale=0.66))
                else:
                    self.add(needle)
                    self.wait(time)
                
                if closest_dist <= math.sin(angle)*needle_len/2:
                    intersect += 1
                total += 1
                pi_estimate = 2*needle_len*total/intersect/paper_spacing if intersect else 0

                if num_needles == 1:
                    return ([point_x - math.cos(angle)*needle_len/2, point_y - math.sin(angle)*needle_len/2, 0], 
                            [point_x + math.cos(angle)*needle_len/2, point_y + math.sin(angle)*needle_len/2, 0])
       
        needle_ends = draw_needles(1, True)
        
        self.wait(1)

        needle_brace = BraceBetweenPoints(needle_ends[0], needle_ends[1])
        needle_brace_text = needle_brace.get_tex("1")
        
        self.play(Write(needle_brace))
        self.play(Write(needle_brace_text))

        self.wait(1)

        self.play(AnimationGroup(Transform(needle_brace, BraceBetweenPoints([-1.5, 1.5, 0], [-1.5, 0, 0])), 
                                Transform(needle_brace_text, BraceBetweenPoints([-1.5, 1.5, 0], [-1.5, 0, 0]).get_tex("1")), lag_ratio=0))

        self.wait(1)

        self.play(AnimationGroup(Unwrite(needle_brace), Unwrite(needle_brace_text), lag_ratio=0))
        
        self.wait(1)

        draw_needles(49, False, 0.1)

        self.wait(1)
        
        pi_formula = MathTex("\\pi", "\\approx", "{2n", "\\over", "k}")
        pi_formula.move_to(5.6*LEFT + 1.25*UP)
       
        target_n = total_var.get_part_by_tex("n").copy()
        target_k = hit_var.get_part_by_tex("k").copy()
        
        # draw pi approximation formula
        self.play(Transform(target_n, pi_formula.get_part_by_tex("{2n")))
        
        self.wait(1)

        self.play(Write(pi_formula.get_part_by_tex("\\over")))
        
        self.play(Transform(target_k, pi_formula.get_part_by_tex("k}")))
        
        self.wait(1)

        self.play(AnimationGroup(Write(pi_formula.get_part_by_tex("\\pi")), Write(pi_formula.get_part_by_tex("\\approx")), lag_ratio=0.5))
        
        self.wait(2)

        pi_approx_equals = MathTex("\\approx")
        pi_approx_equals.move_to(5.75*LEFT + 0.25*UP)
        pi_num.move_to(4.25*LEFT + 0.25*UP)

        # draw actual pi approximation
        self.play(AnimationGroup(Write(pi_approx_equals), Write(pi_num), lag_ratio=0.4))

        self.wait(2)

        draw_needles(450, False, 0.02)
        
        self.wait(1)


