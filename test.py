from manim import *

class Test(Scene):
    def construct(self):
      num = 1
      text = Tex(r"$\pi \approx {a}$".format(a = num))
        
      text.add_updater(lambda obj: obj.become(Tex(r"$\pi \approx {a}$".format(a = num))))
      self.add(text)
      self.wait()
      num = 2
      self.wait()