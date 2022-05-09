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
            elif "" in log:

            # FALLING # TYPE 7
            elif "" in log:

            # FALLING BLOCKS # TYPE 8
            elif "" in log:

            # FIRE # TYPE 9
            elif "" in log:

            # FIREWORK ROCKETS # TYPE 10
            elif "" in log:

            # LAVA # TYPE 11
            elif "" in log:

            # LIGHTNING # TYPE 12
            elif "" in log:

            # MAGMA BLOCK # TYPE 13
            elif "" in log:

            # MAGIC # TYPE 14
            elif "" in log:
            
            # POWDER SNOW # TYPE 15
            elif "" in log:

            # PLAYERS AND MOBS # TYPE 16
            elif "" in log:

            # STARVING # TYPE 17
            elif "" in log:

            # SUFFOCATION # TYPE 18
            elif "" in log:

            # SWEET BERRY BUSHES # TYPE 19
            elif "" in log:

            # THORNS # TYPE 20
            elif "" in log:

            # TRIDENT # TYPE 21
            elif "" in log:

            # VOID # TYPE 22
            elif "" in log:

            # WITHER EFFECT # TYPE 23
            elif "" in log:

            # DRYING OUT # TYPE 24
            elif "" in log:

            # GENERIC DEATH # TYPE 25Ç
            elif "" in log:

            # TEMPORARY # TYPE 26
            elif "" in log:

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
