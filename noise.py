import numpy as np


class linearFunction():
  def __init__(self,slope:int, root:int):
    self.slope = slope
    self.root = root
  def __call__(self, input):
    return self.slope*(input - self.root)


class PerlinNoise():
  def __init__(self, seed:int):
    if seed < 0:
      raise ValueError("Seed can't be negative")
    self.seed = seed

  def interpolation(self, lineA:linearFunction, lineB:linearFunction, x, interpolation_function:str):
    # be careful, LineA is must be previous line and lineB is next line
    # a and b are the y for nearset linear funtions for given input x
    dis_from_A = x - lineA.root


    if interpolation_function == "linear":
      output = dis_from_A * (lineB(x)) + (1 - dis_from_A)* (lineA(x))
      return output
    elif interpolation_function == "smoothstep":
      t = -2*(dis_from_A ** 3) + 3*(dis_from_A ** 2)
      return t * lineB(x) + (1 - t) * lineA(x)
    elif interpolation_function == "fade":
      t = 6*(dis_from_A ** 5) - 15*(dis_from_A ** 4) + 10*(dis_from_A ** 3)
      return t * lineB(x) + (1 - t) * lineA(x)
      

    raise ValueError("The interpolation function is not valid!")
  

  def __call__(self, input, interpolation_function, frequency, amp_mul, fre_mul, octaves = 1, amplitude = 1):
    if input < 0:
      raise ValueError("Input can't be negative")

   
    result = 0
    for i in range(octaves):
      input *= frequency
      round_input = int(input)
    
      np.random.seed(round_input * self.seed)
      previous_line = linearFunction(np.random.uniform(-1, 1), round_input)
      
      np.random.seed((round_input + 1) * self.seed)
      next_line = linearFunction(np.random.uniform(-1, 1), round_input + 1) 

      result += self.interpolation(previous_line, next_line, input, interpolation_function) * amplitude

      amplitude *= amp_mul
      frequency *= fre_mul


    return result
    
