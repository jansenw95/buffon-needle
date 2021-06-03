from manim import *
import math
import random
import numpy as np

class BuffonTest(Scene):
    def construct(self):
        paper_left = -1.5
        paper_right = 6.5
        paper_bottom = -3
        paper_top = 3
        num_paper_lines = 5 # >1

        # formula for calculating pi underneath only works if needle_len <= paper_spacing
        needle_len = (paper_top - paper_bottom)/(num_paper_lines - 1)
        paper_spacing = (paper_top - paper_bottom)/(num_paper_lines - 1)

        intersect = 0
        total = 0
        pi_estimate = 0

        pi_counter = MathTex(r"\pi \approx")
        estimate_text = DecimalNumber(0,
                                    num_decimal_places=5,
                                    include_sign=False,
                                    unit=None,
                                    show_ellipsis=True
                                    )
        estimate_text.add_updater(lambda d: d.set_value(pi_estimate))
        estimate_text.next_to(pi_counter, RIGHT)
        estimate_text.shift(0.03*UP)
        all_text = Group(pi_counter,estimate_text)
        all_text.to_corner(UL)

        self.add(all_text)

        for x in range(num_paper_lines):
            line = Line([paper_left, paper_bottom + paper_spacing*x, 0], 
                        [paper_right, paper_bottom + paper_spacing*x,0]).set_color(WHITE)
            self.add(line)

        self.wait()

        for x in range(10):
            # get random point that will be the center of the line, also keep line from sticking outside paper for aesthetics
            point_x = random.uniform(paper_left + needle_len/2, paper_right - needle_len/2)
            point_y = random.uniform(paper_bottom + needle_len/2, paper_top - needle_len/2)

            # calculate the closest distance between the point and a gridline
            closest_dist = min(point_y - (paper_bottom + paper_spacing*math.floor((point_y - paper_bottom)/paper_spacing)), 
                               paper_bottom + paper_spacing*math.ceil((point_y - paper_bottom)/paper_spacing) - point_y)
            
            angle = random.random()*math.pi            
            line = Line([point_x - math.cos(angle)*needle_len/2, point_y - math.sin(angle)*needle_len/2, 0], 
                        [point_x + math.cos(angle)*needle_len/2, point_y + math.sin(angle)*needle_len/2, 0])
            
            # check for intersection
            if closest_dist <= math.sin(angle)*needle_len/2:
                line.set_color(RED) 
                intersect += 1

            total += 1
            pi_estimate = 2*needle_len*total/intersect/paper_spacing if intersect else 0
            
            self.add(line)
            self.wait(0.1)
        self.wait(1)
