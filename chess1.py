import pygame

def draw_board(the_board):

    pygame.init()
    colors = [(255,255,255), (0,0,0)]    
    rectangle_dragin = False
    n = len(the_board)         
    surface_sz = 480           
    sq_sz = surface_sz // n   
    surface_sz = n * sq_sz     
    evv = pygame.event.get()
  
    surface = pygame.display.set_mode((surface_sz, surface_sz))

    ball = pygame.image.load("Ficha_Naranja.png")
    ball2 = pygame.image.load("Ficha_Azul.png")


    ball_offset = (sq_sz-ball.get_width()) // 2 

    while True:

        ev = pygame.event.poll()
        if ev.type == pygame.QUIT:
            break;

        for row in range(n):          
            c_indx = row % 2           
            for col in range(n):       
                the_square = (col*sq_sz, row*sq_sz, sq_sz, sq_sz)
                surface.fill(colors[c_indx], the_square)

                c_indx = (c_indx + 1) % 2

        # Jugador 1.
        #i = 0
        #k = 0
        surface.blit(ball,(4*sq_sz+ball_offset,0*sq_sz+ball_offset))
        surface.blit(ball,(7*sq_sz+ball_offset,1*sq_sz+ball_offset))
        surface.blit(ball,(7*sq_sz+ball_offset,3*sq_sz+ball_offset))
        surface.blit(ball,(5*sq_sz+ball_offset,1*sq_sz+ball_offset))
        surface.blit(ball,(6*sq_sz+ball_offset,2*sq_sz+ball_offset))
        surface.blit(ball,(6*sq_sz+ball_offset,0*sq_sz+ball_offset))


        #Jugador 2
        surface.blit(ball2,(3*sq_sz+ball_offset,7*sq_sz+ball_offset))
        surface.blit(ball2,(0*sq_sz+ball_offset,4*sq_sz+ball_offset))
        surface.blit(ball2,(0*sq_sz+ball_offset,6*sq_sz+ball_offset))
        surface.blit(ball2,(1*sq_sz+ball_offset,5*sq_sz+ball_offset))
        surface.blit(ball2,(1*sq_sz+ball_offset,7*sq_sz+ball_offset))
        surface.blit(ball2,(2*sq_sz+ball_offset,6*sq_sz+ball_offset))
        pygame.display.flip()

        
        for event in evv:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if  surface.blit(ball,(4*sq_sz+ball_offset,0*sq_sz+ball_offset)).collidepoint(event.pos):   
                        rectangle_dragin = True 
                        mouse_x, mouse_y = event.pos
                        offset_x = surface.blit(ball,(4*sq_sz+ball_offset,0*sq_sz+ball_offset)) - mouse_x
                        offset_y = surface.blit(ball,(4*sq_sz+ball_offset,0*sq_sz+ball_offset)) - mouse_y
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    rectangle_dragin = False
            elif evet.type == pygame.MOUSEMOTION:
                if rectangle_dragin:
                    mouse_x, mouse_y = event.pos
                    ball.x = mouse_x + offset_x
                    surface.blit(ball,(4*sq_sz+ball_offset,0*sq_sz+ball_offset)).y = mouse_y + offset_y

                
                print(pos)
        pygame.display.flip()

      
if __name__ == "__main__":
    draw_board([6, 4, 2, 0, 5, 7, 1, 3])