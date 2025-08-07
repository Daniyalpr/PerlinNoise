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
    



class PerlinNoise2D():
    def __init__(self, seed = 1):
        self.seed = seed

    def interpolation_function(self, first_val, second_val, interpolation_function:str, dis_from_first_val):
        if interpolation_function == "linear":
            weight = dis_from_first_val
            return weight*(second_val) + (1-weight)*(first_val)
        elif interpolation_function == "fade":
            weight = 6*(dis_from_first_val**5)-15*(dis_from_first_val**4)+10*(dis_from_first_val**3)
            return weight*(second_val) + (1-weight)*(first_val)
        elif interpolation_function == "smoothstep":
            weight = -2*(dis_from_first_val**3) + 3*(dis_from_first_val**2)
            return weight*(second_val) + (1-weight)*(first_val)
        else:
            raise ValueError("interpolation function is not valid!")


            
    def __call__(self, x, y, interpolation_function, octaves, frequency, fre_mul, amp_mul, amplitude=1):
        result = 0
        for i in range(octaves):
            x = x*frequency
            y = y*frequency

            int_x = int(x)
            int_y = int(y)
            decimal_part_x = x % 1
            decimal_part_y = y % 1

            vector_pos = (int_x, int_y) 
            #ensure that the seed value is not out of range
            seed_value = (abs(hash(vector_pos)) * self.seed) % 2**31
            np.random.seed(seed_value)
            angle = np.random.uniform(0,np.pi)
            vector_top_left = (np.cos(angle), np.sin(angle))
            dis_vector_top_left = (decimal_part_x, decimal_part_y)

            vector_pos = (int_x, int_y + 1) 
            seed_value = (abs(hash(vector_pos)) * self.seed) % 2**31
            np.random.seed(seed_value)
            angle = np.random.uniform(0,np.pi)
            vector_bottom_left = (np.cos(angle), np.sin(angle))
            dis_vector_bottom_left = (decimal_part_x, -(1 - decimal_part_y))

            vector_pos = (int_x + 1, int_y) 
            seed_value = (abs(hash(vector_pos)) * self.seed) % 2**31
            np.random.seed(seed_value)
            angle = np.random.uniform(0,np.pi)
            vector_top_right = (np.cos(angle), np.sin(angle))
            dis_vector_top_right = (-(1 - decimal_part_x), decimal_part_y)

            vector_pos = (int_x + 1, int_y + 1) 
            seed_value = (abs(hash(vector_pos)) * self.seed) % 2**31
            np.random.seed(seed_value)
            angle = np.random.uniform(0,np.pi)
            vector_bottom_right = (np.cos(angle), np.sin(angle))
            dis_vector_bottom_right = (-(1 - decimal_part_x), -(1 - decimal_part_y))

            top_left_dot = np.dot(vector_top_left, dis_vector_top_left)
            bottom_left_dot = np.dot(vector_bottom_left, dis_vector_bottom_left)
            top_right_dot = np.dot(vector_top_right, dis_vector_top_right)
            bottom_right_dot = np.dot(vector_bottom_right, dis_vector_bottom_right)

            left_axis = self.interpolation_function(top_left_dot, bottom_left_dot, interpolation_function, decimal_part_y)
            right_axis = self.interpolation_function(top_right_dot, bottom_right_dot, interpolation_function, decimal_part_y)

            result += self.interpolation_function(left_axis, right_axis, interpolation_function, decimal_part_x)

            frequency *= fre_mul
            amplitude *= amp_mul

        return result












