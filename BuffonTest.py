from manim import *
import math
import random
import numpy as np

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
        pi_counter = MathTex(r"\pi \approx")
        total_var = MathTex(r"n")
        total_equals = MathTex(r" =")
        hit_var = MathTex(r"k")
        hit_equals = MathTex(r" =")

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

        # position variables
        hit_var.next_to(total_var, DOWN)
        pi_counter.next_to(hit_var, DOWN*1.2)
        
        # position equals signs
        total_equals.next_to(total_var, RIGHT)
        hit_equals.next_to(hit_var, RIGHT*1.1)

        # position numbers
        total_num.next_to(total_equals, RIGHT)
        total_num.shift(UP*0.04)
        hit_num.next_to(hit_equals, RIGHT)
        hit_num.shift(DOWN*0.02)
        pi_num.next_to(pi_counter, RIGHT)

        all_text = Group(pi_counter, pi_num, total_var, hit_var, total_num, hit_num, total_equals, hit_equals)
        all_text.to_corner(UL)

        ########### draw paper lines
        line_group = VGroup()
        for x in reversed(range(num_paper_lines)):
            line = Line([paper_left, paper_bottom + paper_spacing*x, 0], 
                        [paper_right, paper_bottom + paper_spacing*x,0]).set_color(WHITE)
            line_group.add(line)
        self.play(Create(line_group, lag_ratio=0.1))   
        ###########

        self.wait(1)

        self.play(AnimationGroup(*[Write(total_var), Write(total_equals), Write(total_num)], lag_ratio=0.5))
        self.play(AnimationGroup(*[Write(hit_var), Write(hit_equals), Write(hit_num)], lag_ratio=0.5))

        self.wait(1)

        self.play(Wiggle(total_var, scale_value=1.5, rotation_angle=0.2))

        self.wait(0.5)

        self.play(Wiggle(hit_var, scale_value=1.5, rotation_angle=0.2))

        # set random seed for consistency 
        random.seed('m1n3cr4ft')

        def draw_needles(num_needles, fade, time):
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
                    intersect += 1
                
            
                if fade:
                    self.play(FadeIn(needle, scale=0.66).set_run_time(time))
                else:
                    self.add(needle)
                    self.wait(time)
                
                total += 1
                pi_estimate = 2*needle_len*total/intersect/paper_spacing if intersect else 0
       
        draw_needles(1, True, 0.5)
        self.wait(1)
        draw_needles(5, True, 0.2)


