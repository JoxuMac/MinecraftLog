# -*- coding: utf-8 -*-

# IMPORTS
import fileinput
from datetime import datetime

playersFile = "players"
path = 'espcraft-logs'
players = []

def main():
    loadPlayersFromFile()
    for line in fileinput.input():
            log = line.rstrip()
            date = datetime.today().strftime('%Y-%m-%d')
            # Open a file with access mode 'a'
            file_object = open(path + '/' + date + '.log', 'a')
            # Append log at the end of file
            file_object.write(log + '\n')
            # Close the file
            file_object.close()
            if log is not '':
                procesalog(log, date)

def procesalog(log, date):
    global players
    player = log.split(" ")[3]
    hora = log.split(" ")[0][1:-1]
    # JUGADOR ENTRANDO
    if "joined the game" in log:
        # JUGADOR NUEVO
        if player not in players:
            player = (' '.join(log.split("joined the game")).split(" "))
            player.pop(0)
            player.pop(0)
            player.pop(0)
            player = ' '.join(player)
            # GUARDO JUGADOR EN BBDD
            guardaJugadorBBDD(player)

            # GUARDO JUGADOR EN FICHERO
            savePlayerInFile(player)

            # GUARDO JUGADOR EN LISTA
            players.append(player)

        # ACTUALIZA HORA ENTRADA
        actualizaHoraEntradaBBDD(player, date, hora)

        # GUARDO LOG CONOCIDO
        guardaLineaConocidaLogBBDD(player, date, hora, log)

    else:
        # SI ES LOG DE JUGADOR
        pseudoplayer = list(filter(lambda x: x.startswith(player), players))
        if len(pseudoplayer) > 0:
            player = pseudoplayer[0]

        if player in players:
            # JUGADOR SALIENDO Y HORA DE ENTRADA VALIDA
            if "left the game" in log:
                actualizaHorasJugandoBBDD(player, date, hora) # ACTUALIZA HORAS JUGADAS
                actualizaHoraEntradaBBDD(player, '', '') # ELIMINO HORA DE ENTRADA
                guardaLineaConocidaLogBBDD(player, date, hora, log) # GUARDO LOG CONOCIDO

            # JUGADOR CONSIGUE LOGRO
            elif "has made the advancement" in log:
                logro = log.split("[")[-1][:-1]
                guardaLogroBBDD(player, date, hora, logro)
                guardaLineaConocidaLogBBDD(player, date, hora, log)

            # ARROW # TYPE 1
            elif "was shot by" in log and "skull from" not in log:
                if "using" in log:
                    item = log.split("using ")[1]
                    killer = log.split(" using ")[0].split("was shot by ")[1]
                    # <player> was shot by <player/mob> using <item>
                    guardaMuerteBBDD(player, date, hora, 1, killer, item)
                else:
                    killer = log.split("was shot by ")[1]
                    # <player> was shot by <player/mob>
                    guardaMuerteBBDD(player, date, hora, 1, killer, '')

                guardaLineaConocidaLogBBDD(player, date, hora, log)
          
            # SNOWBALLS # TYPE 2
            elif "was pummeled by" in log:
                if "using" in log:
                    item = log.split("using ")[1]
                    killer = log.split(" using ")[0].split("was pummeled by ")[1]
                    # <player> was pummeled by <player/mob>
                    guardaMuerteBBDD(player, date, hora, 2, killer, item)
                else:
                    killer = log.split("was pummeled by ")[1]
                    # <player> was pummeled by <player/mob> using <item>
                    guardaMuerteBBDD(player, date, hora, 2, killer, '')

                guardaLineaConocidaLogBBDD(player, date, hora, log)

            # CACTUS # TYPE 3
            elif "was pricked to death" in log:
                # <player> was pricked to death
                guardaMuerteBBDD(player, date, hora, 3, '', '')
                guardaLineaConocidaLogBBDD(player, date, hora, log)

            elif "walked into a cactus whilst" in log:
                killer = log.split("to escape ")[1]
                # <player> walked into a cactus whilst trying to escape <player/mob>
                guardaMuerteBBDD(player, date, hora, 3, killer, '')
                guardaLineaConocidaLogBBDD(player, date, hora, log)

            # DROWNING # TYPE 4
            elif "drowned" in log:
                if "escape" in log:
                    killer = log.split("to escape ")[1]
                    # <player> drowned whilst trying to escape <player/mob>
                    guardaMuerteBBDD(player, date, hora, 4, killer, '')
                else:
                    # <player> drowned
                    guardaMuerteBBDD(player, date, hora, 4, '', '')

                guardaLineaConocidaLogBBDD(player, date, hora, log)

            # ELYTRA # TYPE 5
            elif "experienced kinetic energy" in log:
                if "escape" in log:
                    killer = log.split("to escape ")[1]
                    # <player> experienced kinetic energy whilst trying to escape <player/mob>
                    guardaMuerteBBDD(player, date, hora, 5, killer, '')
                else:
                    # <player> experienced kinetic energy
                    guardaMuerteBBDD(player, date, hora, 5, '', '')

                guardaLineaConocidaLogBBDD(player, date, hora, log)

            # EXPLOSIONS # TYPE 6
            elif "blew up" in log:
                # <player> blew up
                guardaMuerteBBDD(player, date, hora, 6, '', '')
                guardaLineaConocidaLogBBDD(player, date, hora, log)
            
            elif "was blown up by" in log:
                if "using" in log:
                    item = log.split("using ")[1]
                    killer = log.split(" using ")[0].split("was blown up by ")[1]
                    # <player> was blown up by <player/mob> using <item>
                    guardaMuerteBBDD(player, date, hora, 6, killer, item)
                else:
                    killer = log.split("was blown up by ")[1]
                    # <player> was blown up by <player/mob>
                    guardaMuerteBBDD(player, date, hora, 6, killer, '')
                    
                guardaLineaConocidaLogBBDD(player, date, hora, log)

            elif "was killed by [Intentional Game Design]" in log:
                # <player> was killed by [Intentional Game Design]
                guardaMuerteBBDD(player, date, hora, 6, '[Intentional Game Design]', '')
                guardaLineaConocidaLogBBDD(player, date, hora, log)

            # FALLING # TYPE 7
            elif "hit the ground too hard" in log:
                if "escape" in log:
                    killer = log.split("to escape ")[1]
                    # <player> hit the ground too hard whilst trying to escape <player/mob>
                    guardaMuerteBBDD(player, date, hora, 7, killer, '')
                else:
                    # <player> hit the ground too hard
                    guardaMuerteBBDD(player, date, hora, 7, '', '')
                guardaLineaConocidaLogBBDD(player, date, hora, log)
                
            elif "fell from" in log or "fell off" in log or "fell while" in log or "fell out of the water" in log:
                # <player> fell off a ladder
                # <player> fell off some vines
                # <player> fell off some weeping vines
                # <player> fell off some twisting vines
                # <player> fell off scaffolding
                # <player> fell while climbing
                # <player> fell from a high place
                # <player> fell out of the water
                guardaMuerteBBDD(player, date, hora, 7, '', '')
                guardaLineaConocidaLogBBDD(player, date, hora, log)
                
            elif "was impaled on a stalagmite" in log:
                if "fighting" in log:
                    killer = log.split("fighting ")[1]
                    # <player> was impaled on a stalagmite whilst fighting <player/mob>
                    guardaMuerteBBDD(player, date, hora, 7, killer, '')
                else:
                    # <player> was impaled on a stalagmite
                    guardaMuerteBBDD(player, date, hora, 7, '', '')
                    
                guardaLineaConocidaLogBBDD(player, date, hora, log)

            # FALLING BLOCKS # TYPE 8
            elif "was squashed by a falling" in log or "was skewered by a falling" in log:
                if "fighting" in log:
                    killer = log.split("fighting ")[1]
                    # <player> was squashed by a falling anvil whilst fighting <player/mob>
                    # <player> was squashed by a falling block whilst fighting <player/mob>
                    # <player> was skewered by a falling stalactite whilst fighting <player/mob>
                    guardaMuerteBBDD(player, date, hora, 8, killer, '')
                else:
                    # <player> was squashed by a falling anvil
                    # <player> was squashed by a falling block
                    # <player> was skewered by a falling stalactite
                    guardaMuerteBBDD(player, date, hora, 8, '', '')
                    
                guardaLineaConocidaLogBBDD(player, date, hora, log)

            # FIRE # TYPE 9
            elif "went up" in log or "burned to death" in log:
                # <player> went up in flames
                # <player> burned to death
                guardaMuerteBBDD(player, date, hora, 9, '', '')    
                guardaLineaConocidaLogBBDD(player, date, hora, log)
                
            elif "was burnt" in log or "walked into fire" in log:
                killer = log.split("fighting ")[1]
                # <player> walked into fire whilst fighting <player/mob>
                # <player> was burnt to a crisp whilst fighting <player/mob>
                guardaMuerteBBDD(player, date, hora, 9, killer, '')    
                guardaLineaConocidaLogBBDD(player, date, hora, log)
                
            # FIREWORK ROCKETS # TYPE 10
            elif "went off with a bang" in log and "whilst" not in log:
                if "from" in log:
                    killer = log.split("by ")[1]
                    item = log.split(" by ")[0].split(" from ")[1]
                    # <player> went off with a bang due to a firework fired from <item> by <player/mob>
                    guardaMuerteBBDD(player, date, hora, 10, killer, item)
                else:
                    # <player> went off with a bang
                    guardaMuerteBBDD(player, date, hora, 10, '', '')  
                    
                guardaLineaConocidaLogBBDD(player, date, hora, log)

            # LAVA # TYPE 11
            elif "tried to swim in lava" in log:
                if "escape" in log:
                    killer = log.split("escape ")[1]
                    # <player> tried to swim in lava to escape <player/mob>
                    guardaMuerteBBDD(player, date, hora, 11, killer, '')  
                else:
                    # <player> tried to swim in lava
                    guardaMuerteBBDD(player, date, hora, 11, '', '')  
                    
                guardaLineaConocidaLogBBDD(player, date, hora, log)

            # LIGHTNING # TYPE 12
            elif "was struck by lightning" in log:
                if "fighting" in log:
                    killer = log.split("fighting ")[1]
                    # <player> was struck by lightning whilst fighting <player/mob>
                    guardaMuerteBBDD(player, date, hora, 12, killer, '')  
                else:
                    # <player> was struck by lightning
                    guardaMuerteBBDD(player, date, hora, 12, '', '')  
                    
                guardaLineaConocidaLogBBDD(player, date, hora, log)
                
            # MAGMA BLOCK # TYPE 13
            elif "discovered the floor was lava" in log:
                # <player> discovered the floor was lava
                guardaMuerteBBDD(player, date, hora, 13, '', '')    
                guardaLineaConocidaLogBBDD(player, date, hora, log)
                
            elif "walked into danger zone due to" in log:
                killer = log.split("due to ")[1]
                # <player> walked into danger zone due to <player/mob>
                guardaMuerteBBDD(player, date, hora, 13, killer, '')    
                guardaLineaConocidaLogBBDD(player, date, hora, log)
                
            # MAGIC # TYPE 14
            elif "was killed by magic" in log:
                if "escape" in log:
                    killer = log.split("escape ")[1]
                    # <player> was killed by magic whilst trying to escape <player/mob>
                    guardaMuerteBBDD(player, date, hora, 14, killer, '')
                else:
                    # <player> was killed by magic
                    guardaMuerteBBDD(player, date, hora, 14, '', '')    
                
                guardaLineaConocidaLogBBDD(player, date, hora, log)
                
            elif "using magic" in log:
                killer = log.split("using magic")[0].split("killed by ")[1]
                # <player> was killed by <player/mob> using magic
                guardaMuerteBBDD(player, date, hora, 14, killer, '')
                guardaLineaConocidaLogBBDD(player, date, hora, log)
                
            elif "was killed by" in log and "using" in log:
                item = log.split("using ")[1]
                killer = log.split(" using ")[0].split("killed by ")[1]
                #<player> was killed by <player/mob> using <item>
                guardaMuerteBBDD(player, date, hora, 14, killer, item)
                guardaLineaConocidaLogBBDD(player, date, hora, log)
            
            # POWDER SNOW # TYPE 15
            elif "froze to death" in log:
                # <player> froze to death
                guardaMuerteBBDD(player, date, hora, 15, '', '')
                guardaLineaConocidaLogBBDD(player, date, hora, log)
                
            elif "frozen to death by" in log:
                killer = log.split("death by ")[1]
                # <player> was frozen to death by <player/mob>
                guardaMuerteBBDD(player, date, hora, 15, killer, '')
                guardaLineaConocidaLogBBDD(player, date, hora, log)

            # PLAYERS AND MOBS # TYPE 16
            elif "was slain by" in log:
                if "using" in log:
                    item = log.split("using ")[1]
                    killer = log.split(" using ")[0].split("slain by ")[1]
                    # <player> was slain by <player/mob> using <item>
                    guardaMuerteBBDD(player, date, hora, 16, killer, item)
                else:
                    killer = log.split("slain by ")[1]
                    # <player> was slain by <player/mob>
                    guardaMuerteBBDD(player, date, hora, 16, killer, '')
                    
                guardaLineaConocidaLogBBDD(player, date, hora, log)
             
            elif "was fireballed by" in log:
                if "using" in log:
                    item = log.split("using ")[1]
                    killer = log.split(" using ")[0].split("fireballed by ")[1]
                    # <player> was fireballed by <player/mob> using <item>
                    guardaMuerteBBDD(player, date, hora, 16, killer, item)
                else:
                    killer = log.split("fireballed by ")[1]
                    # <player> was fireballed by <player/mob>
                    guardaMuerteBBDD(player, date, hora, 16, killer, '')
                    
                guardaLineaConocidaLogBBDD(player, date, hora, log)
                
            elif "was stung to death" in log and "by" not in log:
                # <player> was stung to death
                guardaMuerteBBDD(player, date, hora, 16, '', '')  
                guardaLineaConocidaLogBBDD(player, date, hora, log)
               
            elif "sonically-charged shriek" in log:
                if "escape" in log:
                    killer = log.split("escape ")[1]
                    # <player> was obliterated by a sonically-charged shriek whilst trying to escape <player/mob>‌
                    guardaMuerteBBDD(player, date, hora, 16, killer, '')
                else:
                    # <player> was obliterated by a sonically-charged shriek
                    guardaMuerteBBDD(player, date, hora, 16, '', '')
                    
                guardaLineaConocidaLogBBDD(player, date, hora, log)
            
            elif "was shot by" in log and "skull from" in log:
                killer = log.split("from ")[1]
                # <player> was shot by a skull from <player/mob>
                guardaMuerteBBDD(player, date, hora, 16, killer, '')
                guardaLineaConocidaLogBBDD(player, date, hora, log)
                
            elif "death.attack.sting.item" in log:
                # death.attack.sting.item
                # BUG REQUEST : https://bugs.mojang.com/browse/MC-186851
                guardaMuerteBBDD(player, date, hora, 16, '', '')
                guardaLineaConocidaLogBBDD(player, date, hora, log)
                
            elif "death.attack.witherSkull.item" in log:
                # death.attack.witherSkull.item
                # BUG REQUEST : https://bugs.mojang.com/browse/MC-186148
                guardaMuerteBBDD(player, date, hora, 16, '', '')
                guardaLineaConocidaLogBBDD(player, date, hora, log)
             
            # STARVING # TYPE 17
            elif "starved to death" in log:
                if "fighting" in log:
                    killer = log.split("fighting ")[1]
                    # <player> starved to death
                    guardaMuerteBBDD(player, date, hora, 17, killer, '')
                else:
                    # <player> starved to death whilst fighting <player/mob>
                    guardaMuerteBBDD(player, date, hora, 17, '', '')

                guardaLineaConocidaLogBBDD(player, date, hora, log)
    
            # SUFFOCATION # TYPE 18
            elif "suffocated in a wall" in log:
                if "fighting" in log:
                    killer = log.split("fighting ")[1]
                    # <player> suffocated in a wall whilst fighting <player/mob>
                    guardaMuerteBBDD(player, date, hora, 18, killer, '')
                else:
                    #<player> suffocated in a wall
                    guardaMuerteBBDD(player, date, hora, 18, '', '')
                    
                guardaLineaConocidaLogBBDD(player, date, hora, log)

            elif "was squished too much" in log:
                #<player> was squished too much
                guardaMuerteBBDD(player, date, hora, 18, '', '')
                guardaLineaConocidaLogBBDD(player, date, hora, log)
                
            elif "was squashed by" in log:
                killer = log.split("by ")[1]
                #<player> was squashed by <player/mob>
                guardaMuerteBBDD(player, date, hora, 18, killer, '')
                guardaLineaConocidaLogBBDD(player, date, hora, log)
                
            # SWEET BERRY BUSHES # TYPE 19
            elif "was poked to death by a sweet berry bush" in log:
                if "escape" in log:
                    killer = log.split("escape ")[1]
                    # <player> was poked to death by a sweet berry bush whilst trying to escape <player/mob>
                    guardaMuerteBBDD(player, date, hora, 19, killer, '')
                else:
                    # <player> was poked to death by a sweet berry bush
                    guardaMuerteBBDD(player, date, hora, 19, '', '')
                
                guardaLineaConocidaLogBBDD(player, date, hora, log)

            # THORNS # TYPE 20
            elif "trying to hurt" in log:
                if "by" in log:
                    killer = log.split("hurt ")[1]
                    item = log.split(" trying to hurt ")[0].split("by ")[1]
                    # <player> was killed by <item> trying to hurt <player/mob>
                    guardaMuerteBBDD(player, date, hora, 20, killer, item)
                else:
                    killer = log.split("hurt ")[1]
                    # <player> was killed trying to hurt <player/mob>
                    guardaMuerteBBDD(player, date, hora, 20, killer, '')
                    
                guardaLineaConocidaLogBBDD(player, date, hora, log)

            # TRIDENT # TYPE 21
            elif "was impaled by" in log:
                if "with" in log:
                    item = log.split("with ")[1]
                    killer = log.split(" with ")[0].split(" by ")[1]
                    # <player> was impaled by <player/mob> with <item>
                    guardaMuerteBBDD(player, date, hora, 21, killer, item)
                else:
                    killer = log.split("by ")[1]
                    # <player> was impaled by <player/mob>
                    guardaMuerteBBDD(player, date, hora, 21, killer, '')
                    
                guardaLineaConocidaLogBBDD(player, date, hora, log)
    
            # VOID # TYPE 22
            elif "fell out of the world" in log:
                # <player> fell out of the world
                guardaMuerteBBDD(player, date, hora, 22, '', '')           
                guardaLineaConocidaLogBBDD(player, date, hora, log)
                
            elif "live in the same world" in log:
                killer = log.split(" same world as ")[1]
                # <player> didn't want to live in the same world as <player/mob>
                guardaMuerteBBDD(player, date, hora, 22, killer, '')           
                guardaLineaConocidaLogBBDD(player, date, hora, log)

            # WITHER EFFECT # TYPE 23
            elif "withered away" in log:
                if "fighting" in log:
                    killer = log.split("fighting ")[1]
                    # <player> withered away whilst fighting <player/mob>
                    guardaMuerteBBDD(player, date, hora, 23, killer, '')
                else:
                    # <player> withered away
                    guardaMuerteBBDD(player, date, hora, 23, '', '') 
                    
                guardaLineaConocidaLogBBDD(player, date, hora, log)

            # DRYING OUT # TYPE 24
            elif "died from dehydration" in log:
                if "escape" in log:
                    killer = log.split("escape ")[1]
                    # <player> died from dehydration whilst trying to escape <player/mob>
                    guardaMuerteBBDD(player, date, hora, 24, killer, '')
                else:
                    # <player> died from dehydration
                    guardaMuerteBBDD(player, date, hora, 24, '', '') 
                    
                guardaLineaConocidaLogBBDD(player, date, hora, log)
                
            # GENERIC DEATH # TYPE 25
            elif "died because" in log:
                killer = log.split("because of ")[1]
                # <player> died because of <player/mob>
                guardaMuerteBBDD(player, date, hora, 25, killer, '')
                guardaLineaConocidaLogBBDD(player, date, hora, log)
                
            elif "roasted in dragon breath" in log:
                if "by" in log:
                    killer = log.split("by ")[1]
                    # <player> was roasted in dragon breath by <player/mob>
                    guardaMuerteBBDD(player, date, hora, 25, killer, '')
                else:
                    # <player> was roasted in dragon breath
                    guardaMuerteBBDD(player, date, hora, 25, '', '')
                    
                guardaLineaConocidaLogBBDD(player, date, hora, log)
                
            elif "was doomed to fall" in log:
                if "by" in log:
                    if "using" in log:
                        item = log.split("using ")[1]
                        killer = log.split(" using ")[0].split(" by ")[1]
                        # <player> was doomed to fall by <player/mob> using <item>
                        guardaMuerteBBDD(player, date, hora, 25, killer, item)
                    else:
                        killer = log.split("by ")[1]
                        # <player> was doomed to fall by <player/mob>
                        guardaMuerteBBDD(player, date, hora, 25, killer, '')
                else:
                    # <player> was doomed to fall
                    guardaMuerteBBDD(player, date, hora, 25, '', '')
                    
                guardaLineaConocidaLogBBDD(player, date, hora, log)

            elif "was finished by" in log:
                if "using" in log:
                    item = log.split("using ")[1]
                    killer = log.split(" using ")[0].split(" by ")[1]
                    # <player> fell too far and was finished by <player/mob> using <item>
                    guardaMuerteBBDD(player, date, hora, 25, killer, item)
                else:
                    killer = log.split("by ")[1]
                    # <player> fell too far and was finished by <player/mob>
                    guardaMuerteBBDD(player, date, hora, 25, killer, '')
                guardaLineaConocidaLogBBDD(player, date, hora, log)
                
            elif "was stung to death by" in log:
                killer = log.split("by ")[1]
                # <player> was stung to death by <player/mob>
                guardaMuerteBBDD(player, date, hora, 25, killer, '')
                guardaLineaConocidaLogBBDD(player, date, hora, log)
                
            elif "went off with a bang whilst" in log:
                killer = log.split("fighting ")[1]
                # <player> went off with a bang whilst fighting <player/mob>
                guardaMuerteBBDD(player, date, hora, 25, killer, '')
                guardaLineaConocidaLogBBDD(player, date, hora, log)
              
            elif "was killed by even more magic" in log:
                # <player> was killed by even more magic
                guardaMuerteBBDD(player, date, hora, 25, '', '')
                guardaLineaConocidaLogBBDD(player, date, hora, log)
           
            elif "died" in log:
                # <player> died
                guardaMuerteBBDD(player, date, hora, 25, '', '')
                guardaLineaConocidaLogBBDD(player, date, hora, log)
                
            # TEMPORARY # TYPE 26
            elif "was too soft for this world" in log:
                if "helped" in log:
                    killer = log.split(" helped")[0].split("world ")[1]
                    # <player> was too soft for this world (<player/mob> helped)
                    guardaMuerteBBDD(player, date, hora, 26, killer, '')
                else:
                    # <player> was too soft for this world
                    guardaMuerteBBDD(player, date, hora, 26, '', '')
                
                guardaLineaConocidaLogBBDD(player, date, hora, log)
                
            # GUARDO LINEA DESCONOCIDA DE LOG DE JUGADOR
            else:
                guardaLineaDesconocidaLogBBDD(player, date, hora, log)

        # DESCARTO LINEA DE LOG POR NO SER LOG DE JUGADOR
        #else:

def loadPlayersFromFile():
    playersfile = open('players', 'r')
    global players
    players = playersfile.read().splitlines()
    playersfile.close()

def savePlayerInFile(player):
    playersfile = open('players', 'a')
    playersfile.write(player + '\n')
    playersfile.close()

def guardaJugadorBBDD(player):
    #TODO
    print('TODO')

def actualizaHoraEntradaBBDD(player, date, hora):
    #TODO
    print('TODO')

def actualizaHorasJugandoBBDD(player, date, hora):
    #TODO
    print('TODO')

def guardaLogroBBDD(player, date, hora, logro):
    #TODO
    print('TODO')

def guardaLineaDesconocidaLogBBDD(player, date, hora, log):
    #TODO
    print('TODO')

def guardaMuerteBBDD(player, date, hora, tipo, killer, item):
    #TODO
    print('TODO')

def guardaLineaConocidaLogBBDD(player, date, hora, log):
    #TODO
    print('TODO')

main()
