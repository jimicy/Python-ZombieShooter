# I - Import and Initialize
import pygame,pygame.locals,sprite_module,random,os
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((1000, 620))    
            
def main():
    '''This function defines the 'mainline logic' for our game.'''
      
    # Display
    pygame.display.set_caption("")
     
    # Entities
    #Create Background
    background = pygame.image.load('bg.jpg')
    background=background.convert()
    screen.blit(background, (0, 0))
    
    #Music
    pygame.mixer.music.load("./sound/Left 4 Dead Soundtrack- 'No Mercy'.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)
    fire = pygame.mixer.Sound("./sound/bullet1.ogg")
    fire.set_volume(0.5)
    no = pygame.mixer.Sound("./sound/no.ogg")
    no.set_volume(0.8)
    
    #Create the sprites
    #Create the player
    player=sprite_module.Player(screen)
    
    #Create the zombies
    #defines number of zombies are needed
    wave=[10,1,1,1,1,1,0] #default [10,10,10,5,5,5,0]
    
    #loads zombie images
    z_img=[]
    for file in os.listdir('enemy/'):
            z_img.append(pygame.image.load('./enemy/'+file))
            
    #zombie types
    #[speed, damage, hp, attack speed, score value]
    z_info=[[3,5,10,100,2],[3,5,20,100,4],[3,5,20,100,6],[3,5,20,100,8]\
                  ,[3,5,20,100,10],[3,5,20,100,12],[15,20,100,100,40]]
    
    zombies=[]
    
    #generate 10 random type zombies
    for i in range(10):
        while True:
            a=random.randint(0,6)
            if wave[a]:
                zombies.append(sprite_module.Zombie\
                               (screen,z_info[a][0],z_info[a][1],\
                                z_info[a][2],z_info[a][3],z_info[a][4],z_img[a],a,player.rect.center))
                wave[a]=wave[a]-1
                break
            
    #Create health,armour,health text,armour text,wave text 
    health=sprite_module.StatusBar((0,20),(255,0,0),(0,0,0),(250,30),200,350,0,None)
    armour=sprite_module.StatusBar((0,52),(238,233,233),(139,137,137),(250,30),100,200,0,None)
    health_text=sprite_module.Text(25,(255,255,255),(125,35),'350,350','%s/%s',255)
    armour_text=sprite_module.Text(25,(0,0,0),(125,70),'200,200','%s/%s',255)
    wave_text=sprite_module.Text\
             (30,(255,255,255),(430,60),'0,1,'+str(sum(wave)),'Score:%s Wave:%s Zombies Left:%s',255)
    
    #Generate ammo text
    ammo=[[20,30],[40,20],[15,10],[100,10],[30,30]]
    temp_string=''
    for index in range(len(ammo)):
        temp_string+=str(ammo[index][0])+','+str(ammo[index][1])+','
    ammo_text=sprite_module.Text\
             (20,(255,255,255),(800,80),temp_string.strip(','),\
              '%s/%s          %s/%s          %s/%s          %s/%s          %s/%s',255)
    
    #Create sprite groups, sprites can be added to groups at anytime
    powerupGroup=pygame.sprite.Group()
    zombieGroup=pygame.sprite.Group(zombies)
    bullet_img=pygame.sprite.Group()
    bullet_hitbox=pygame.sprite.Group()
    reloading=pygame.sprite.Group()
    
    #add sprite groups to be updated in the following order
    allSprites = pygame.sprite.OrderedUpdates\
    (bullet_img,bullet_hitbox,player,zombieGroup,powerupGroup,reloading,health,armour,health_text,armour_text,wave_text,ammo_text)
    
    # ACTION
     
    # Assign 
    clock = pygame.time.Clock()
    keepGoing = True

    #Timer
    speed_timer=0
    damage_timer=0
    invincible_timer=0
    
    #2x damage status
    double_status=False
    #Powerup Status
    powerup_status=False 
    #Invincible Status
    invincible_status=False
    #Boss spawn
    boss_spawn=False
    
    #Power up images
    #Powerups are 2x speed,2x damage,hp,armor,ammo,invincible
    powerup_images=[]
    for file in os.listdir('powerups/'):
            powerup_images.append(pygame.image.load('./powerups/'+file))
            
    #Bullet images
    bullet_images=[]
    for file in os.listdir('bullets/'):
            bullet_images.append(pygame.image.load('./bullets/'+file))
    
    #Variable used to store a randomly generate value which is the powerup chance
    powerup_chance=0
    
    #Wave number
    wave_num=1
    
    #Wave values
    wave_value=[10,10,10,5,5,5,0]
    
    #number of zombies on screen
    active_zombies=10
    
    #Score
    score=0
    
    #Player status [[current hp, max hp], [current armour, max armour], default speed]
    player_status=[[350,350],[200,200],3]
    
    #Status of weapons Pistol, Uzi, Slow Gun, Machine Gun, Railgun
    weapon=[True,True,True,True,True]
    
    #current weapon
    current_weapon=0
    
    #Ammo
    ammo_capacity=[20,40,15,100,30]
    reload_time=[1.5,2,1,0.5,1.5]
    ammo_status=False
    
    #machine gun
    machine_gun_fire=False
    machine_gun_delay=0
    
    # Loop
    while keepGoing:
        # Time
        clock.tick(40)
        speed_timer+=1
        damage_timer+=1
        invincible_timer+=1
        
        #Key Pressed
        keystate = pygame.key.get_pressed()
        if keystate[pygame.locals.K_w]:
            player.go_up(screen) 
            if ammo_status:
                #sets the reload bar above the player
                reload.set_position((player.rect.center[0]-40,player.rect.center[1]+-60))
                
        if keystate[pygame.locals.K_s]:
            player.go_down(screen)
            if ammo_status:
                #sets the reload bar above the player
                reload.set_position((player.rect.center[0]-40,player.rect.center[1]+-60)) 
                
        if keystate[pygame.locals.K_a]:
            player.go_left(screen)
            if ammo_status:
                #sets the reload bar above the player
                reload.set_position((player.rect.center[0]-40,player.rect.center[1]+-60))   
                
        if keystate[pygame.locals.K_d]:
            player.go_right(screen)         
            if ammo_status:
                #sets the reload bar above the player
                reload.set_position((player.rect.center[0]-40,player.rect.center[1]+-60))

        # Events
        for event in pygame.event.get():
            
            #If the user closes the windows keepGoing is set to false and loop is exited
            if event.type == pygame.QUIT:
                keepGoing = False

            elif event.type==pygame.MOUSEBUTTONDOWN:
                #generate bullets based on current weapon when mouse button is down
                
                #Pistol bullets [speed: 12, damage: 2]
                if current_weapon==0 and ammo[0][0]:
                    #play sound
                    fire.play()
                    #subtract ammo
                    ammo[0][0]=ammo[0][0]-1
                    #passes img, player angle, player rect, mouse pos, speed and damage
                    bullet1=sprite_module.Bullet\
                          (bullet_images[0],player.get_angle(),\
                           player.rect.center,pygame.mouse.get_pos(),12,2,double_status)
                    bullet2=sprite_module.Bullet\
                          (None,None,player.rect.center,pygame.mouse.get_pos(),12,2,double_status)
                    bullet_img.add(bullet1)
                    bullet_hitbox.add(bullet2)
                    allSprites = pygame.sprite.OrderedUpdates\
                               (bullet_img,bullet_hitbox,player,zombieGroup,powerupGroup,\
                                reloading,health,armour,health_text,armour_text,wave_text,ammo_text)
                
                #Uzi bullets [speed: 16, damage: 5]    
                elif current_weapon==1 and ammo[1][0]:
                    fire.play()
                    ammo[1][0]=ammo[1][0]-1
                    bullet1=sprite_module.Bullet\
                          (bullet_images[1],player.get_angle(),\
                           player.rect.center,pygame.mouse.get_pos(),16,5,double_status)
                    bullet2=sprite_module.Bullet\
                          (None,None,player.rect.center,pygame.mouse.get_pos(),16,5,double_status)
                    bullet_img.add(bullet1)
                    bullet_hitbox.add(bullet2)
                    allSprites = pygame.sprite.OrderedUpdates\
                               (bullet_img,bullet_hitbox,player,zombieGroup,powerupGroup,\
                                reloading,health,armour,health_text,armour_text,wave_text,ammo_text)
                
                #Slow bullets [speed: 8, damage: 0]     
                elif current_weapon==2 and ammo[2][0]:
                    ammo[2][0]=ammo[2][0]-1
                    bullet1=sprite_module.Bullet\
                          (bullet_images[2],player.get_angle(),\
                           player.rect.center,pygame.mouse.get_pos(),8,0,double_status)
                    bullet2=sprite_module.Bullet\
                          (None,None,player.rect.center,pygame.mouse.get_pos(),8,0,double_status)
                    bullet_img.add(bullet1)
                    bullet_hitbox.add(bullet2)
                    allSprites = pygame.sprite.OrderedUpdates\
                               (bullet_img,bullet_hitbox,player,zombieGroup,powerupGroup,\
                                reloading,health,armour,health_text,armour_text,wave_text,ammo_text)
                
                # Machine gun bullets hold to keep shooting[speed: 14, damage:6]
                elif current_weapon==3 and ammo[3][0]:
                    machine_gun_fire=True
                    
                #Railgun [damage: 20]     
                elif current_weapon==4 and ammo[4][0]:
                    ammo[4][0]=ammo[4][0]-1
                    bullet1=sprite_module.RailGun\
                          (screen,player.rect.center,pygame.mouse.get_pos())
                    bullet2=sprite_module.Bullet\
                          (None,None,player.rect.center,pygame.mouse.get_pos(),20,20,double_status)
                    bullet_img.add(bullet1)
                    bullet_hitbox.add(bullet2)
                    allSprites = pygame.sprite.OrderedUpdates\
                               (bullet_img,bullet_hitbox,player,zombieGroup,powerupGroup,\
                                reloading,health,armour,health_text,armour_text,wave_text,ammo_text)
                    
                else:
                    #If ammo status does not equal true then generate reload box
                    if ammo_status!=True and ammo[current_weapon][1]:
                        reload=sprite_module.StatusBar\
                              ((player.rect.center[0]-40,player.rect.center[1]+-60),\
                               (0,255,0),(0,0,0),(70,7),0,100,1,reload_time[current_weapon])
                        reloading.add(reload)
                        allSprites = pygame.sprite.OrderedUpdates\
                                   (bullet_img,bullet_hitbox,player,zombieGroup,powerupGroup,\
                                    reloading,health,armour,health_text,armour_text,wave_text,ammo_text)
                    #sets ammo_status to True
                    ammo_status=True
                    
            elif event.type==pygame.MOUSEBUTTONUP:
                if current_weapon==3:
                    machine_gun_fire=False
            
            elif event.type == pygame.KEYDOWN:
                #Change player weapon
                if event.key == pygame.K_1 and weapon[0] and ammo_status==False:
                    current_weapon=0
                    player.change_image(0)
                    machine_gun_fire=False
                    
                elif event.key == pygame.K_2 and weapon[1] and ammo_status==False:
                    current_weapon=1
                    player.change_image(1)
                    machine_gun_fire=False
                    
                elif event.key == pygame.K_3 and weapon[2] and ammo_status==False:
                    current_weapon=2
                    player.change_image(2)
                    machine_gun_fire=False
                    
                elif event.key == pygame.K_4 and weapon[3] and ammo_status==False:
                    current_weapon=3
                    player.change_image(3)
                    machine_gun_fire=False
                    
                elif event.key == pygame.K_5 and weapon[4] and ammo_status==False:
                    current_weapon=4
                    player.change_image(4)
                    machine_gun_fire=False
                    
                elif event.key==pygame.K_1 or event.key==pygame.K_2 or event.key==pygame.K_3\
                     or event.key==pygame.K_4 or event.key==pygame.K_5:
                    #play no sound effect
                    no.play()
                    
        #Collision
        #Collsion between player and zombie
        x=pygame.sprite.spritecollide(player,zombieGroup, False)
        if x:
            for zombie in x:
                zombie.move(False)
                if not(invincible_status):
                    if zombie.get_attack():
                        #if armour is greater than 0 only then can you subtract from it
                        if player_status[1][0]>0:
                            
                            #armour is subtracted based on the damage inflicted by the specific zombie
                            player_status[1][0]=player_status[1][0]-zombie.get_damage()
                            
                            #if armour is a negative value
                            if player_status[1][0]<0:
                                #add the negative armour value to health
                                player_status[0][0]=player_status[0][0]+player_status[1][0]
                                #set current armour value to 0
                                player_status[1][0]=0
                        else:
                            #health is subtracted based on the damage inflicted by the specific zombie
                            player_status[0][0]=player_status[0][0]-zombie.get_damage()
        else:
            for zombie in zombieGroup:
                zombie.move(True)
                zombie.reset_attack()
                    
        #Collision between bullet and zombie
        c=pygame.sprite.groupcollide(bullet_hitbox,zombieGroup,True,False)
        v=pygame.sprite.groupcollide(bullet_img,zombieGroup,True,False)
        if c:
            for bullet in c.keys():
                #If the bullet is the slow bullet weapon 3, slow the enemy
                if bullet.get_damage()==0:
                    c[bullet][0].slow()
                    
                #if not do the regular bullet and enemy handling
                else:
                    
                    #calls zombie.damage_hp(damage) method which returns false if zombie hp<=0
                    #randomly generate a value and if it matches the powerup number, powerup is generated
                    if not(c[bullet][0].damage_hp(bullet.get_damage())):
                        
                        wave[c[bullet][0].get_wave_type()]=wave[c[bullet][0].get_wave_type()]-1
                        
                        powerup_chance=random.randrange(99)
                        
                        if powerup_chance==0:
                            powerup_status=True
                            power=sprite_module.Powerup\
                                   (c[bullet][0].rect.center,5,powerup_images[5])
                        elif powerup_chance==1 or powerup_chance==2:
                            powerup_status=True
                            power=sprite_module.Powerup\
                                   (c[bullet][0].rect.center,0,powerup_images[0])
                        elif powerup_chance==3 or powerup_chance==4:
                            powerup_status=True
                            power=sprite_module.Powerup\
                                   (c[bullet][0].rect.center,1,powerup_images[1])
                        elif powerup_chance==5 or powerup_chance==6:
                            powerup_status=True
                            power=sprite_module.Powerup\
                                   (c[bullet][0].rect.center,2,powerup_images[2])
                        elif powerup_chance==7 or powerup_chance==8:
                            powerup_status=True
                            power=sprite_module.Powerup\
                                   (c[bullet][0].rect.center,3,powerup_images[3])
                        elif powerup_chance==9 or powerup_chance==10 or powerup_chance==11 or powerup_chance==12:
                            powerup_status=True
                            power=sprite_module.Powerup\
                                   (c[bullet][0].rect.center,4,powerup_images[4])
                        else:
                            powerup_status=True
                            power=sprite_module.Powerup\
                                   (c[bullet][0].rect.center,4,powerup_images[4])
                        
                        #if there is a powerup add it to the powerupGroup
                        #call allSprites and update all sprites
                        if powerup_status:
                            powerupGroup.add(power)
                            allSprites = pygame.sprite.OrderedUpdates\
                                (bullet_img,bullet_hitbox,player,zombieGroup,powerupGroup,\
                                reloading,health,armour,health_text,armour_text,wave_text,ammo_text)
                        
                        #Add the value of the zombie to score
                        score+=c[bullet][0].get_value()
                        #Kill the zombie
                        c[bullet][0].kill()
                
        #Collision between powerups and player
        y=pygame.sprite.spritecollide(player,powerupGroup, False)
        if y:
            for buff in y:
                powerup_type=buff.get_type()
                #speed
                if powerup_type==0:
                    speed_timer=0
                    player.increase_speed()
                #damage
                elif powerup_type==1:
                    double_status=True
                    damage_timer=0
                #HP increase by 100
                elif powerup_type==2:
                    player_status[0][0]=player_status[0][0]+100
                    
                    #if the new current hp exceeds the max, set current hp to max
                    if player_status[0][0]>player_status[0][1]:
                        player_status[0][0]=player_status[0][1]
                        
                #Armour increase by 100
                elif powerup_type==3:
                    player_status[1][0]=player_status[1][0]+100
                    
                    #if the new current armour exceeds the max, set current armour to max
                    if player_status[1][0]>player_status[1][1]:
                        player_status[1][0]=player_status[1][1]
                        
                #Ammo
                elif powerup_type==4:
                    min_value=90000
                    min_index=0
                    for index in range(len(ammo)):
                        if min_value>ammo[index][0]*ammo[index][1]:
                            min_value=ammo[index][0]*ammo[index][1]
                            min_index=index
                    ammo[min_index][0]=ammo_capacity[min_index]
                    ammo[min_index][1]=ammo[min_index][1]+5
                    
                #Invincible
                elif powerup_type==5:
                    invincible_status=True
                    invincible_timer=0
                buff.kill()
                
        #Player and Weapon 
        #Rotate player towards mouse            
        player.rotate(pygame.mouse.get_pos())
        
        #Machine gun fire
        if machine_gun_fire:
            machine_gun_delay+=1
            #delay by %3
            if machine_gun_delay%3==0:
                fire.play()
                
                #[speed: 14, damage:6]
                bullet1=sprite_module.Bullet\
                       (bullet_images[0],player.get_angle(),\
                        player.rect.center,pygame.mouse.get_pos(),14,6,double_status)
                
                bullet2=sprite_module.Bullet\
                        (None,None,player.rect.center,pygame.mouse.get_pos(),14,6,double_status)
                
                bullet_img.add(bullet1)
                bullet_hitbox.add(bullet2)
                allSprites = pygame.sprite.OrderedUpdates\
                           (bullet_img,bullet_hitbox,player,zombieGroup,powerupGroup,\
                            reloading,health,armour,health_text,armour_text,wave_text,ammo_text)
                ammo[3][0]=ammo[3][0]-1
                
        #Check to see if machine gun has ammo. If not set fire to False        
        if ammo[3][0]==0:
            machine_gun_fire=False
        
        #checks when reload is 100% and sets ammo_status to False        
        if ammo_status:
            if reload.get_reload():
                ammo[current_weapon][0]=ammo_capacity[current_weapon]
                ammo[current_weapon][1]=ammo[current_weapon][1]-1
                ammo_status=False
        
        #Set health and armour status        
        health.set_status(player_status[0][0])
        armour.set_status(player_status[1][0])
        if player_status[0][0]<=0:
            keepGoing=False
        
        #Powerup Timer Tracker
        if speed_timer==450:
            player.reset_speed()
        if damage_timer==450:
            double_status=False
        if invincible_timer==450:
            invincible_status=False
        
        #Text
        #set wave variables
        wave_text.set_variable(0,str(score))
        wave_text.set_variable(1,str(wave_num))
        wave_text.set_variable(2,str(sum(wave)))
        
        #set health and armour variables
        health_text.set_variable(0,str(player_status[0][0]))
        armour_text.set_variable(0,str(player_status[1][0]))
        
        #set ammo variables
        index=0
        for i in range(5):
            for n in range(2):
                ammo_text.set_variable(index,str(ammo[i][n]))
                index+=1
        
        #Zombies        
        #Adjusts zombies
        for zombie in zombieGroup:
            zombie.rotate(player.rect.center)
            zombie.set_step_amount(player.rect.center)
        
        #check if 5 waves have passed
        if wave_num%5==0 and boss_spawn!=True:
            boss_spawn=True
            wave[6]=1
        else:
            boss_spawn=False
            
        #check if wave is cleared
        if sum(wave)==0:
            active_zombies+=1
            wave_num+=1
            wave_increase=1 #default 7
            for index in range(len(wave_value)-1):
                wave_value[index]=wave_value[index]+wave_increase
                wave[index]=wave_value[index]
                if index/3:
                    wave_increase-=2

                
        #generate new zombies there is less zombies than there should be
        while len(zombieGroup)!=active_zombies:
            a=random.randint(0,6)
            if wave[a]:
                wave[a]=wave[a]-1
                zombie=(sprite_module.Zombie\
                               (screen,z_info[a][0],z_info[a][1],\
                                z_info[a][2],z_info[a][3],z_info[a][4],z_img[a],a,player.rect.center))
                zombieGroup.add(zombie)
                allSprites = pygame.sprite.OrderedUpdates\
                           (bullet_img,bullet_hitbox,player,zombieGroup,powerupGroup,\
                            reloading,health,armour,health_text,armour_text,wave_text,ammo_text)
        
        # Refresh screen
        screen.blit(background,(0,0))
        allSprites.update()
        allSprites.draw(screen)
         
        pygame.display.flip()
     
    # Close the game window
    pygame.quit()    
     
         
# Call the main function
main()