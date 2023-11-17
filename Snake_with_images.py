 #!/usr/bin/env python3
 #*- coding: utf-8 -*-
'''
You have just been hired at a video game software house and you have
to render the snake game on an image  by saving the final image of the
snake's path and returning the length of the snake.
Implement the generate_snake function that takes as input a path to an
image file, which is the starting image "start_img". The image can
contain black background pixels, obstacle for the snake as red pixels
and finally food as orange pixels. The snake must be drawn in green.
In addition you must draw in gray the trail that the snake leaves onto
its path. The function also takes as input the initial snake position,
"position" as a list of two integers X and Y. The commands of the
player on how to move the snake in the video game are available in a
string "commands."  The function must save the final image of the
snake's path to the path "out_img," which is passed as the last input
argument to the function. In addition, the function must return the
length of the snake at the end of the game.

Each command in "commands" corresponds to a cardinal sign, followed by
a space. The possible cardinal signs are:

| NW | N | NE |
| W  |   |  E |
| SW | S | SE |

corresponding to one-pixel snake movements such as:

| up-left     | up     | up-right     |
| left        |        | right        |
| bottom-left | bottom | bottom-right |

The snake moves according to the commands; in the case the snake
eats food, it increases its size by one pixel.

The snake can move from side to side of the image, horizontally and
vertically, this means that if the snake crosses a side of the image,
it will appear again from the opposite side.
The game ends when the commands are over or the snake dies. The snake
dies when:
- it hits an obstacle
- it hits itself so it cannot pass over itself
- crosses itself diagonally. As an examples, a 1->2->3-4 path like the
  one below on the left is not allowed; while the one on the right is
  OK.

  NOT OK - diagonal cross        OK - not a diagonal cross
       | 4 | 2 |                    | 1 | 2 |
       | 1 | 3 |                    | 4 | 3 |

For example, considering the test case data/input_00.json
the snake starts from "position": [12, 13] and receives the commands
 "commands": "S W S W W S W N N W N N N N N W N" 
generates the image in visible in data/expected_end_00.png
and returns 5 since the snake is 5 pixels long at the
end of the game.

NOTE: Analyze the images to get the exact color values to use.

NOTE: do not import or use any other library except images.
'''
import images



back_color = (0,0,0)
trace_clr = (128,128,128)
snk_clr = (0,255,0)
obst_clr = (255,0,0)
food_clr = (255, 128, 0)
moves = {"S" : [1,0], "N": [-1,0], "E": [0,1], "W": [0,-1], "SE": [1,1], "SW": [1,-1], "NE": [-1,+1], "NW": [-1,-1] }
    
def add_pixel(x,y,image,array,green):
    image[x][y] = green
    new_pixel = [x,y]
    array.append(new_pixel)
    x,y = x,y
    return x,y,array



def move(x,y,array,image,grey,green):
  r_p = array[0][0]
  c_p = array[0][1]
  image[r_p][c_p] = grey
  for i in range(len(array)-1):
      array[i] = array[i+1][:]
      r_p = array[i][0]
      c_p = array[i][1]
      image[r_p][c_p] = green
  array[-1] = [x,y]
  x,y = array[-1][:]
  image[x][y] = green
          
  return x,y,array


def check_move(x,y,image):
  height  = len(image)-1
  width = len(image[0])-1
  if x > height:
    x = 0
  elif x < 0:
    x = height
  
  if y > width:
    y = 0
  elif y < 0:
    y = width
  return x,y

def lenght_check(x,y,image):
  if (x > len(image)-1 or x < 0) or (y > len(image[0]) or y < 0):
    return False
  return True

def color_check(image,x,y,v,z,green):
  if image[x][y] == green and image[v][z] == green:
    return True
  return False

def check_invalid_move(x,y,image,green):
  if lenght_check(x-1,y-1,image) and color_check(image,x,y-1,x+1,y,snk_clr):
    return True 
     
  elif lenght_check(x+1,y+1,image) and  color_check(image,x+1,y,x,y+1,snk_clr):
        return True
  
  elif lenght_check(x-1,y-1,image) and color_check(image,x-1,y,x,y-1,snk_clr):
    return True 
  
  elif lenght_check(x-1,y+1,image) and color_check(image,x-1,y,x,y+1,snk_clr):
    return True
    
  
def generate_snake(start_img: str, position: list[int, int],
    commands: str, out_img: str) -> int:
    
    image = images.load(start_img)
    commands = commands.split()
    
    row  = position[1]
    column = position[0]
    snk_pixels = [[row,column]]
    image[row][column] = snk_clr
    
    for input in commands:
      
      new_row,new_column = row + moves[input][0], column + moves[input][1]
      row,column = check_move(new_row,new_column,image)
      
      if image[row][column] == obst_clr or image[row][column] == snk_clr:
          break

      if len(input) == 2 and check_invalid_move(row,column,image,snk_clr):
        break 
         
      if image[row][column] == food_clr:
        add_pixel(row,column,image,snk_pixels,snk_clr)
          
      else:
        move(row,column,snk_pixels,image,trace_clr,snk_clr)
      
    images.save(image, out_img)           
    return len(snk_pixels)
