from dataclasses import dataclass
from typing import Callable, Any

import pygame
import pyscroll
import pytmx

from dialog import DialogBox
from player import NPC, Player


@dataclass
class Portal:
    from_world: str
    origin_point: str
    target_world: str
    teleport_point: str


@dataclass
class Event:
    # Un event est un portail qui nous teleporte dans une autre map, differente mais très similaire
    # Les dialogues et les elements peuvent donc etre différents.
    # Idéalement le personnage est téléporté aux mêmes coordonnées dans l'autre map.
    # Pas besoin d'avoir un pnj fantome pour lancer des dialogues
    name: str
    from_world: str
    origin_point: str
    target_world: str
    player_action: Callable[[Player], Any] = None
    dialog: list[str] = None
    teleport_point: str = None

    # music : str

    # battle :


@dataclass
class Map:
    name: str
    walls: list[pygame.Rect]
    group: pyscroll.PyscrollGroup
    tmx_data: pytmx.TiledMap
    portals: list[Portal]
    npcs: list[NPC]
    events: list[Event]


class MapManager:
    def __init__(self, screen, player, dialog_box):
        self.maps = dict()
        self.screen = screen
        self.player: Player = player
        self.dialog_box: DialogBox = dialog_box
        self.current_map = "carte"
        self.register_map("carte", portals=[
            Portal(from_world="carte", origin_point="enter_house", target_world="house", teleport_point="spawn_house"),
            Portal(from_world="carte", origin_point="enter_dungeon", target_world="dungeon 2",
                   teleport_point="spawn_dungeon")
        ], npcs=[
            NPC("paul", nb_points=4, dialog=["dépêche toi d'aller dans la chambre secrète",
                                             "avant qu'il ne soit trop tard, si tu", "veux je te suis"]),
            NPC("robin", nb_points=1, dialog=["la chambre secrète est dans la maison"])
        ], events=[
            Event(from_world="carte", origin_point="Traverser", target_world="carte_chemdiff",
                  name="Traversée pont", dialog=["Tiens cette maison se démarque des autres ?"])
        ])
        self.register_map("carte_chemdiff", portals=[
            Portal(from_world="carte_chemdiff", origin_point="enter_house", target_world="house",
                   teleport_point="spawn_house"),
            Portal(from_world="carte_chemdiff", origin_point="enter_dungeon", target_world="dungeon 2",
                   teleport_point="spawn_dungeon")
        ], npcs=[
            NPC("paul", nb_points=2, dialog=["dépêche toi d'aller dnas la chambre secrète",
                                             "avant qu'il ne soit trop tard, si tu", "veux je te suis"]),
            NPC("robin", nb_points=1, dialog=["la chambre secrète est dans la maison"])
        ], events=[
            Event(from_world="carte_chemdiff", origin_point="pp pass", target_world="carte_chemdiff",
                  name="tu ne peux pas y aller", dialog=["tu ne peux y aller pour le moment"],
                  player_action=EventActions.event_player_move_right),
            Event(from_world="carte_chemdiff", origin_point="quoi", target_world="carte_chap1",
                  name="p situation", dialog=["Pourquoi avait l'air d'en savoir tant", "tout ceci t'intrigue", "N'est-ce pas"])])
        self.register_map("carte_chap1", portals=[
        ], npcs=[
            NPC("Toad", nb_points=1,
                dialog=["Qu'est que ?! La maison a disparu..."]),
            NPC("flambino", nb_points=2, dialog=["flambi"]),
            NPC("larmeleon", nb_points=2, dialog=["larmé"]),
            NPC("gloria", nb_points=1,
                dialog=["Qu'est-ce qui se passe,", "dans la partie sud-est,", "un passage s'est ouvert,", "allons voir ce qu'il s'est passé"]),
            NPC("red", nb_points=1, dialog=[""]),
            NPC("beladonis", nb_points=1, dialog=[""]),
            NPC("fl", nb_points=1, dialog=[""]),
            NPC("nikolai", nb_points=1, dialog=[""]),
            NPC("boss", nb_points=1, dialog=[""]),
            ], events=[
            Event(from_world="carte_chap1", origin_point="att", target_world="carte_chap1.2",
                  name="Traversée pont", teleport_point="carte", dialog=["épée : Que... Mais vous êtes ?!", "??? : Oui, on a reçu le même sort que vous", "Toad : Moi c'est Toad", "Mario : Et moi Mario", "Toad : Désolé de vous avoir fait peur,", "Toad : mais derrière nous"])
        ])
        self.register_map("carte_chap1.2", npcs=[
            NPC("Toad", nb_points=1,
                dialog=[""]),
            NPC("flambino", nb_points=1, dialog=[""]),
            NPC("larmeleon", nb_points=1, dialog=[""]),
            NPC("gloria", nb_points=1,
                dialog=[""]),
            NPC("red", nb_points=1, dialog=[""]),
            NPC("rival", nb_points=1, dialog=[""]),
            NPC("beladonis", nb_points=1, dialog=[""]),
            NPC("fl", nb_points=1, dialog=[""]),
            NPC("ghetis", nb_points=1, dialog=[""]),
            NPC("saphir", nb_points=2, dialog=[""]),
            NPC("rubis", nb_points=1, dialog=[""]),
            NPC("nikolai", nb_points=1, dialog=[""]),
            NPC("boos aqua", nb_points=1, dialog=[""]),
            NPC("boss", nb_points=1, dialog=[""]),
            NPC("zacian", nb_points=1, dialog=[""]),
        ], events=[
            Event(from_world="carte_chap1.2", origin_point="enter_enemies", target_world="enemies",
                  name="entre enemies", teleport_point="spawn_rocket_base" ,dialog=["cette endroit n'était pas là avant, qu'est-ce que cela veut dire"],
                  player_action=EventActions.event_player_move_up)
        ])
        self.register_map("house", portals=[
            Portal(from_world="house", origin_point="exit_house", target_world="carte",
                   teleport_point="enter_house_exit"),
            Portal(from_world="house", origin_point="enter_bedrooms", target_world="bedroom",
                   teleport_point="spawn_bed"),
        ])
        self.register_map("bedroom", portals=[
            Portal(from_world="bedroom", origin_point="enter_bed_exit", target_world="house",
                   teleport_point="exit_bedroom"),
            Portal(from_world="bedroom", origin_point="enter_secret_room_exit", target_world="secret",
                   teleport_point="spawn_secret_room")
        ])
        self.register_map("bedroom 2", portals=[
            Portal(from_world="bedroom 2", origin_point="enter tunnel", target_world="Tunnel",
                   teleport_point="spawn tunnel")
        ])
        self.register_map("secret", portals=[
            Portal(from_world="secret", origin_point="exit_secret_room", target_world="bedroom",
                   teleport_point="spawn_secret_room_exit"),
        ], npcs=[
            NPC("Toad", nb_points=1,
                dialog=["la menace qui pèse sur le monde, tu ne pourras pas", "la stopper tout seul,",
                        "tu auras besoin" "de trouver une personne du nom de...", "TOAD !"]),
            NPC("flambino", nb_points=1, dialog=["flambi !"]),
            NPC("larmeleon", nb_points=1, dialog=["larméleon !"]),
            NPC("gloria", nb_points=1,
                dialog=["ces petits monstres s'appellent les pokémon ", "mais j'imagine que je ne t'apprends rien",
                        "nous ne savons ce qui nous est arrivé", "on a vu dans le ciel une lumière d'un",
                        "noir de jaïs, et là... plus rien", "on s'est réveillé dans le monde que tu vois là mais...",
                        "t'entend ce bruit ?! oh non !", "la caverne s'effondre, sors de là, vite !"]),
            NPC("red", nb_points=1, dialog=[" "]),
            NPC("rival", nb_points=1, dialog=["Oh c'est toi, vas parler aux autres, vite ! "]),
            NPC("beladonis", nb_points=1, dialog=["l'un de nos scientifiques à découvert que",
                                                  " des personnes similires aux pokémon serait venu dans notre monde..."]),
            NPC("fl", nb_points=1, dialog=[" "]),
            NPC("ghetis", nb_points=1, dialog=[" "]),
            NPC("saphir", nb_points=1, dialog=[" "]),
            NPC("rubis", nb_points=1, dialog=["..."])
        ], events=[
            Event(from_world="secret", origin_point="doit parler", target_world="secret",
                  name="dois parler", dialog=["Parle à tout le monde"],
                  player_action=EventActions.event_player_move_up),
            Event(from_world="secret", origin_point="caverne", target_world="secret doit parler",
                  name="peut passer", dialog=["vous entendez un bruit, vous devez vous enfuir"],
                  player_action=EventActions.event_player_move_up)])
        self.register_map("Tunnel", portals=[
            Portal(from_world="Tunnel", origin_point="exit_tunnel", target_world="carte_chemdiff",
                   teleport_point="exit_tunnel"),
        ], npcs=[
            NPC("Toad", nb_points=1,
                dialog=["On reste ici pour monter la garde"]),
            NPC("flambino", nb_points=2, dialog=["flambi !"]),
            NPC("larmeleon", nb_points=2, dialog=["larméleon !"]),
            NPC("gloria", nb_points=1,
                dialog=["Qu'est-ce qu'il se passe, j'ai déjà une idée mais ", "je n'en suis pas sûr, sortons de là déjà."]),
            NPC("red", nb_points=2, dialog=["..."]),
            NPC("rival", nb_points=2, dialog=["C'est lui, c'est sur."]),
            NPC("beladonis", nb_points=1, dialog=["au nom de la loi, il faut l'arreter",
                                                  "Tout ceci m'inquiète"]),
            NPC("fl", nb_points=1, dialog=[" "]),
            NPC("ghetis", nb_points=2, dialog=[" "]),
            NPC("saphir", nb_points=2, dialog=[" "]),
            NPC("rubis", nb_points=1, dialog=["..."]),

        ],
        events=[
            Event(from_world="Tunnel", origin_point="pp pass", target_world="Tunnel",
                  name="dois parler", dialog=["le feu a dû  se propager,", "vaut mieux ne pas y retourner"],
                  player_action=EventActions.event_player_move_right)])
        self.register_map("secret doit parler", portals=[
            Portal(from_world="secret doit parler", origin_point="exit_secret_room", target_world="bedroom 2",
                   teleport_point="spawn_secret_room_exit"),
        ], npcs=[
            NPC("Toad", nb_points=1,
                dialog=["c'est pas vrai, fuis on te rejoint !"]),
            NPC("flambino", nb_points=1, dialog=["flambi !"]),
            NPC("larmeleon", nb_points=1, dialog=["larméleon !"]),
            NPC("gloria", nb_points=1,
                dialog=["Qu'est-ce qui se passe ici, ça ne la pas suffit "]),
            NPC("red", nb_points=1, dialog=[" "]),
            NPC("rival", nb_points=1, dialog=["Oh c'est toi, vas parler aux autres, vite ! "]),
            NPC("beladonis", nb_points=1, dialog=["l'un de nos scientifiques à découvert que",
                                                  " des personnes similires aux pokémon serait venu dans notre monde..."]),
            NPC("fl", nb_points=1, dialog=[" "]),
            NPC("ghetis", nb_points=1, dialog=[" "]),
            NPC("saphir", nb_points=1, dialog=[" "]),
            NPC("rubis", nb_points=1, dialog=["..."])
        ])
        self.register_map("dungeon 2", portals=[
            Portal(from_world="dungeon 2", origin_point="exit_dungeon", target_world="carte",
                   teleport_point="enter_dungeon_exit"),
            Portal(from_world="dungeon 2", origin_point="enter_manoir", target_world="dungeon 3",
                   teleport_point="spawn_manoir")
        ])
        self.register_map("dungeon 3", portals=[
            Portal(from_world="dungeon 3", origin_point="enter_manoir_exit", target_world="dungeon 2",
                   teleport_point="exit_manoir")
        ])
        self.register_map("enemies", portals=[
        ], npcs=[
            NPC("dresseur", nb_points=1, dialog=["bienvenue dans le complexe..."]),
        ], events=[
            Event(from_world="enemies", origin_point="enter_restricted_area", target_world="restricted_area",
                  name="ch", dialog=["Qu'est ce que ?!"])
        ])
        self.teleport_player("player")
        self.teleport_npcs()


    def progress_dialog(self):
        if self.dialog_box.reading:
            # Si un dialogue est en cours, on continue le dialogue
            self.dialog_box.continue_dialog()
            if self.dialog_box.reading == False:
                # Le dialogue est terminé : on permet au joueur de bouger
                self.player.can_move = True
        else:
            # Si un dialogue n'est pas en cours,
            # On lance le dialogue du PNJ à coté (si il y en a)
            for sprite in self.get_group().sprites():
                if sprite.feet.colliderect(self.player.rect) and type(sprite) is NPC:
                    self.player.can_move = False  # Le dialogue commence : on empêche le joueur de bouger
                    self.dialog_box.start_dialog(sprite.dialog)

    def check_collisions(self):
        for portal in self.get_map().portals:
            if portal.from_world == self.current_map:
                point = self.get_object(portal.origin_point)
                rect = pygame.Rect(point.x, point.y, point.width, point.height)
                if self.player.feet.colliderect(rect):
                    copy_portal = portal
                    self.current_map = portal.target_world
                    self.teleport_player(copy_portal.teleport_point)

        for event in self.get_map().events:
            point = self.get_object(event.origin_point)
            rect = pygame.Rect(point.x, point.y, point.width, point.height)
            if self.player.feet.colliderect(rect):
                self.current_map = event.target_world
                if event.teleport_point is not None:
                    self.teleport_player(event.teleport_point)
                if event.dialog is not None:
                    self.dialog_box.start_dialog(event.dialog)
                    self.player.can_move = False
                if event.player_action is not None:
                    event.player_action(self.player)

        for sprite in self.get_group().sprites():
            if type(sprite) is NPC:
                if sprite.feet.colliderect(self.player.rect):
                    sprite.speed = 0
                else:
                    sprite.speed = 1
            if sprite.feet.collidelist(self.get_walls()) > -1:
                sprite.move_back()

    def teleport_player(self, name):
        point = self.get_object(name)
        self.player.position[0] = point.x
        self.player.position[1] = point.y
        self.player.save_location()

    def register_map(self, name, portals=[], npcs=[], events=[]):
        tmx_data = pytmx.util_pygame.load_pygame(f"./Assets/Tiles/{name}.tmx")
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2

        walls = []
        for Objects in tmx_data.objects:
            if Objects.type == "collision":
                walls.append(pygame.Rect(Objects.x, Objects.y, Objects.width, Objects.height))
        group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=6)
        group.add(self.player)
        for npc in npcs:
            group.add(npc)
        self.maps[name] = Map(name, walls, group, tmx_data, portals, npcs, events)

    def get_map(self):
        return self.maps[self.current_map]

    def get_group(self):
        return self.get_map().group

    def get_walls(self):
        return self.get_map().walls

    def get_object(self, name):
        return self.get_map().tmx_data.get_object_by_name(name)

    def teleport_npcs(self):
        for map in self.maps:
            map_data = self.maps[map]
            npcs = map_data.npcs
            for npc in npcs:
                npc.load_points(map_data.tmx_data)
                npc.teleport_spawn()

    def draw(self):
        self.get_group().draw(self.screen)
        self.get_group().center(self.player.rect.center)

    def update(self):
        self.get_group().update()
        self.check_collisions()
        for npc in self.get_map().npcs:
            npc.move()


class EventActions:
    @staticmethod
    def event_player_move_right(player: Player):
        player.move_right()

    @staticmethod
    def event_player_move_up(player: Player):
        player.move_up()
