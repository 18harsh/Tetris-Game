import pygame
import random

pygame.init() 

#Shapes
S=[[".....",
	".....",
	"..00.",
	".00..",
	"....."],
   [".....",
	"..0..",
	"..00.",
	"...0.",
	"....."]]
Z=[[".....",
	".....",
	".00..",
	"..00.",
	"....."],
   [".....",
	"...0.",
	"..00.",
	"..0..",
	"....."]]
I=[[".....",
	"..0..",
	"..0..",
	"..0..",
	"..0.."],
   [".....",
	".....",
	"0000",
	".....",
	"....."]]	
O =[[".....",
	 ".....",
	 "..00.",
	 "..00.",
	 "....."]]
J=[[".....",
	".0...",
	".000.",
	".....",
	"....."],
   [".....",
	"..00.",
	"..0..",
	"..0..",
	"....."],
  [ ".....",
	".....",
	".000.",
	"...0.",
	"....."],
   [".....",
	"..0..",
	"..0..",
	".00..",
	"....."]]
L=[[".....",
	"...0.",
	".000.",
	".....",
	"....."],
   [".....",
	"..0..",
	"..0..",
	"..00.",
	"....."],
  [ ".....",
	".....",
	".000.",
	".0...",
	"....."],
   [".....",
	".00..",
	"..0..",
	"..0..",
	"....."]]		
T=[[".....",
	"..0..",
	".000.",
	".....",
	"....."],
   [".....",
	"..0..",
	"..00.",
	"..0..",
	"....."],
  [ ".....",
	".....",
	".000.",
	"..0..",
	"....."],
   [".....",
	"..0..",
	".00..",
	"..0..",
	"....."]]	

shapes = [S, Z, I, O, J, L, T]
shapes_color = [(255,0,0),(0,255,0),(0,0,255),(255,100,10),(255,255,0),(115,0,0),(100,40,0)]


class Piece(object):
    rows = 20  # y
    columns = 10  # x

    def __init__(self, column, row, shape):
        self.x = column
        self.y = row
        self.shape = shape
        self.color = shapes_color[shapes.index(shape)]
        self.rotation = 0  # number from 0-3

def select_shape():
	global shapes,shapes_color
	return Piece(5, 0, random.choice(shapes))

def shape_into_format(shape):
	positions = []
	format = shape.shape[shape.rotation % len(shape.shape)]
	for i, line in enumerate(format):
		row = list(line)
		for j, column in enumerate(row):
			if column == '0':
				positions.append((shape.x + j, shape.y + i))
	for i, pos in enumerate(positions):
		positions[i] = (pos[0] - 2, pos[1] - 4)

	return positions

def draw_next_shape(next_shape):
	x = top_left_x+play_width +50
	y = top_left_y+ play_height/2 -100 
	font = pygame.font.SysFont('comicsans',30)
	label = font.render("Next Shape",1,(255,255,255))
	format = next_shape.shape[next_shape.rotation % len(next_shape.shape)]
	for i, line in enumerate(format):
		row = list(line)
		for j,column in enumerate(row):
			if column == '0':
				pygame.draw.rect(win,next_shape.color,((x+j*30),y+i*30,30,30))
	win.blit(label,(x+10,y-30))

def check_lost(positions):
	for pos in positions:
		x,y = pos
		if y<1:
			return True
	return False	

def valid_space(shape,grids):
	accepted_position = [[(j,i) for j in range(10) if grids[i][j]==(0,0,0)]for i in range(20)]
	accepted_position = [j for sub in accepted_position for j in sub]

	formatted = shape_into_format(shape)

	for pos in formatted:
		if pos not in accepted_position:
			if pos[1]>-1:
				return False
	return True	

def create_grid(locked_position = {}):
	rows = int(play_height/30)
	cols = int(play_width/30)
	grids = [[(0,0,0) for x in range(cols)] for x in range(rows)]
	for i in range(len(grids)):
		for j in range(len(grids[0])):
			if (j,i) in locked_position:
				grids[i][j] = locked_position[(j,i)]
	return grids

def draw_grid(win):
	for i in range(10):
		pygame.draw.line(win,(255,255,255),(top_left_x+30*i,top_left_y),(top_left_x+30*i,top_left_y+play_height),2)
		for j in range(20):
			pygame.draw.line(win,(255,255,255),(top_left_x,top_left_y+j*30),(top_left_x+play_width,top_left_y+j*30),2)
	
		

def draw_window():
	win.fill((0,0,0))
	rows = int(play_height/30)
	cols = int(play_width/30)
	
	font = pygame.font.SysFont('comicsans', 60)
	label = font.render('TETRIS', 1, (255,255,255))
	win.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), 30))
	
	for i in range(len(grids)):
		for j in range(len(grids[0])):
			pygame.draw.rect(win,(grids[i][j]),(top_left_x+j*30,top_left_y+i*30,30,30),0)	
	draw_grid(win)
	pygame.draw.rect(win,(255,0,0),(top_left_x,top_left_y,play_width,play_height),5)

def clear_row(grids,locked_position):
	inc = 0
	for row in range(len(grids)-1,-1,-1):
		if (0,0,0) not in grids[row]:
			inc += 1
			ind = row
			for j in range(len(grids[row])):
				try:
					del locked_position[(j,row)]
				except:
					continue

	if inc > 0:
		for key in sorted(list(locked_position), key=lambda x: x[1])[::-1]:
			x, y = key
			if y < ind:
				newKey = (x, y + inc)
				locked_position[newKey] = locked_position.pop(key)				


def main():
	global grids
	run = True
	FPS = 30
	locked_position = {}
	change_piece = False
	grids = create_grid(locked_position)
	current_shape = select_shape()
	next_shape = select_shape()
	clock = pygame.time.Clock()
	fall_count = 0
	score = 0
	while run:
		clock.tick(FPS)
		grids = create_grid(locked_position)

		if not (fall_count%10):
			current_shape.y+=1
			if not (valid_space(current_shape,grids)) and current_shape.y>0:
				current_shape.y-=1
				change_piece = True

		
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					current_shape.x-=1
					if not valid_space(current_shape, grids):
						current_shape.x += 1
				elif event.key == pygame.K_RIGHT:
					current_shape.x+=1
					if not valid_space(current_shape, grids):
						current_shape.x -= 1	
				elif event.key == pygame.K_UP:
					current_shape.rotation = current_shape.rotation+1%len(current_shape.shape)
					if not valid_space(current_shape, grids):
						current_shape.rotation = current_shape.rotation - 1 % len(current_shape.shape)
				if event.key == pygame.K_DOWN:
					current_shape.y += 1
					if not valid_space(current_shape, grids):
						current_shape.y -= 1
				if event.key == pygame.K_SPACE:
					while valid_space(current_shape, grids):
						current_shape.y += 1
					current_shape.y -= 1		

		shape_pos = shape_into_format(current_shape)
		for i in range(len(shape_pos)):
			x,y = shape_pos[i]
			if y>-1:
				# print(shape_pos)
				# print(y,x)
				grids[y][x] = current_shape.color
		
		if change_piece:
			for pos in shape_pos:
				p = (pos[0],pos[1])
				locked_position[p] = current_shape.color
			current_shape = next_shape
			next_shape = select_shape()
			change_piece = False

			if clear_row(grids,locked_position):
				score +=10
		

		draw_window()
		draw_next_shape(next_shape)
		fall_count+=1
		pygame.display.update()
		if check_lost(locked_position):
			run = False
			print(score)
	draw_text_middle("You Lost",(255,255,255),40,win)
	pygame.display.flip()
	pygame.time.delay(3000)		
	pygame.quit()	



def draw_text_middle(text,color,size,win):
	font = pygame.font.SysFont('comicsans',size)
	label = font.render(text,1,color)
	win.blit(label,(top_left_x + play_width/2 -(label.get_width()/2),top_left_y + play_height/2 - label.get_height()/2))

def main_menu():
	run = True
	while run:
		win.fill((0,0,0))
		draw_text_middle("Press any key to start...",(255,255,255),60,win)
		pygame.display.update()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
			if event.type == pygame.KEYDOWN:
				main()

s_width = 800
s_height = 700
play_width = 300  
play_height = 600
top_left_x = (s_width - play_width)//2
top_left_y = (s_height - play_height)

win = pygame.display.set_mode((s_width,s_height),0,0)
pygame.display.set_caption("Tetris")

main_menu()