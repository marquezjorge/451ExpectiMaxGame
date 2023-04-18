STRUGGLE = 'Struggle'
FIRE_PUNCH = 'Fire Punch'
ICE_PUNCH = 'Ice Punch'
JUMP_HIM = 'Jump Him'
THUNDERBOLT = 'Thunderbolt'
SWIFT = 'Swift'
HIGH_JUMPKICK = 'High JumpKick'
SLAM = 'Slam'
TAIL_WHIP = 'Tail Whip'
LICK = 'Lick'
CURSE = 'Curse'
SHADOW_SNEAK = 'Shadow Sneak'
MIRACLE = 'Miracle'
FLAME_THROWER = 'Flame Thrower'
SEISMIC_TOSS = 'Seismic Toss'
WATER_GUN = 'Water Gun'
CRUNCH = 'Crunch'

# MoveName : (Damage, CritChance, HitChance, PP)
MOVES = {
    STRUGGLE: (50, 5, 100, 25),
    FIRE_PUNCH: (70, 10, 70, 10),
    ICE_PUNCH: (60, 20, 70, 10),
    JUMP_HIM: (80, 15, 70, 5),
    THUNDERBOLT: (90, 0, 65, 4),
    SWIFT: (60, 30, 85, 5),
    HIGH_JUMPKICK: (110, 5, 50, 5),
    SLAM: (65, 15, 100, 5),
    TAIL_WHIP: (50, 20, 100, 5),
    LICK: (25, 50, 75, 10),
    MIRACLE: (200, 0, 3, 3),
    SHADOW_SNEAK: (75, 5, 80, 3),
    CURSE: (60, 5, 100, 5),
    FLAME_THROWER: (90, 10, 60, 4),
    SEISMIC_TOSS: (80, 5, 70, 2),
    WATER_GUN: (60, 15, 95, 4),
    CRUNCH: (70, 0, 80, 3)
}

PIKACHU = "Pikachu"
MACHOP = "Machop"
GHASTLY = 'Ghastly'
MAKUHITA = 'Makuhita'
CHIMCHAR = 'Chimchar'
SQUIRTLE = 'Squirtle'

# PokemonName : (Health, Moves, Attack, Speed)
# Speed is currently unused, yet to see if it will be implemented
POKEMON = {
    PIKACHU: (130, (THUNDERBOLT, SWIFT, SLAM, TAIL_WHIP), 95, 100),
    MACHOP: (200, (FIRE_PUNCH, ICE_PUNCH, JUMP_HIM, HIGH_JUMPKICK), 70, 70),
    GHASTLY: (100, (MIRACLE, LICK, SHADOW_SNEAK, CURSE), 110, 80),
    CHIMCHAR: (160, (FLAME_THROWER, SLAM, HIGH_JUMPKICK, FIRE_PUNCH), 80, 70),
    MAKUHITA: (140, (SEISMIC_TOSS, SLAM, SWIFT, ICE_PUNCH), 80, 80),
    SQUIRTLE: (135, (ICE_PUNCH, TAIL_WHIP, WATER_GUN, CRUNCH), 85, 110),
}

POKEMON_LIST = [PIKACHU, MACHOP, GHASTLY, CHIMCHAR, MAKUHITA, SQUIRTLE]

JOSE = 'Jose'

# List of Teams of 4 based on certain rival names
TRAINERS = {
    JOSE: (GHASTLY, MAKUHITA, CHIMCHAR, SQUIRTLE)
}

TRAINERS_LIST = [JOSE]
