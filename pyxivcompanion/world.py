from enum import Enum, auto

class XIV_WORLD(Enum):
    # Japan
    # Elemental
    Aegis     = auto()
    Atomos    = auto()
    Carbuncle = auto()
    Garuda    = auto()
    Gungnir   = auto()
    Kujata    = auto()
    Tonberry  = auto()
    Typhon    = auto()
    # Gaia
    Alexander  = auto()
    Bahamut    = auto()
    Durandal   = auto()
    Fenrir     = auto()
    Ifrit      = auto()
    Ridill     = auto()
    Tiamat     = auto()
    Ultima     = auto()
    # Mana
    Anima        = auto()
    Asura        = auto()
    Chocobo      = auto()
    Hades        = auto()
    Ixion        = auto()
    Masamune     = auto()
    Pandaemonium = auto()
    Titan        = auto()
    # Meteor
    Belias       = auto()
    Mandragora   = auto()
    Ramuh        = auto()  
    Shinryu      = auto()
    Unicorn      = auto()
    Valefor      = auto()
    Yojimbo      = auto()
    Zeromus      = auto()

    # North America  
    # Aether
    Adamantoise     = auto()
    Cactuar         = auto()
    Faerie          = auto()
    Gilgamesh       = auto()
    Jenova          = auto()
    Midgardsormr    = auto()
    Sargatanas      = auto()
    Siren           = auto()
    # Primal
    Behemoth    = auto()
    Excalibur   = auto()
    Exodus      = auto()
    Famfrit     = auto()
    Hyperion    = auto()
    Lamia       = auto()
    Leviathan   = auto()
    Ultros      = auto()
    # Crystal
    Balmung     = auto()
    Brynhildr   = auto()
    Coeurl      = auto()
    Diabolos    = auto()
    Goblin      = auto()
    Malboro     = auto()
    Mateus      = auto()
    Zalera      = auto()

    # Europe
    # Chaos
    Cerberus    = auto()
    Louisoix    = auto()
    Moogle      = auto()
    Omega       = auto()
    Phantom     = auto()
    Ragnarok    = auto()
    Sagittarius = auto()
    Spriggan    = auto()
    # Light
    Alpha       = auto()
    Lich        = auto()
    Odin        = auto()
    Phoenix     = auto()
    Raiden      = auto()
    Shiva       = auto()
    Twintania   = auto()
    Zodiark     = auto()

    @classmethod
    def Elemental(cls):
        return {cls.Aegis, cls.Atomos, cls.Carbuncle, cls.Garuda,
                cls.Gungnir, cls.Kujata, cls.Tonberry, cls.Typhon}

    @classmethod
    def Gaia(cls):
        return {cls.Alexander, cls.Bahamut, cls.Durandal, cls.Fenrir, cls.Ifrit,
                cls.Ridill, cls.Tiamat, cls.Ultima}

    @classmethod
    def Mana(cls):
        return {cls.Anima, cls.Asura, cls.Chocobo, cls.Hades, cls.Ixion,
                cls.Masamune, cls.Pandaemonium, cls.Titan}

    @classmethod
    def Meteor(cls):
        return {cls.Belias, cls.Mandragora, cls.Ramuh, cls.Shinryu, cls.Unicorn,
                cls.Valefor, cls.Yojimbo, cls.Zeromus}

    @classmethod
    def Aether(cls):
        return {cls.Adamantoise, cls.Cactuar, cls.Faerie, cls.Gilgamesh,
                cls.Jenova, cls.Midgardsormr, cls.Sargatanas, cls.Siren}

    @classmethod
    def Primal(cls):
        return {cls.Behemoth, cls.Excalibur, cls.Exodus, cls.Famfrit,
                cls.Hyperion, cls.Lamia, cls.Leviathan, cls.Ultros}

    @classmethod
    def Crystal(cls):
        return {cls.Balmung, cls.Brynhildr, cls.Coeurl, cls.Diabolos,
                cls.Goblin, cls.Malboro, cls.Mateus, cls.Zalera}

    @classmethod
    def Chaos(cls):
        return {cls.Cerberus, cls.Louisoix, cls.Moogle, cls.Omega, cls.Ragnarok,
                cls.Spriggan, cls.Sagittarius, cls.Phantom}

    @classmethod
    def Light(cls):
        return {cls.Lich, cls.Odin, cls.Phoenix, cls.Shiva, cls.Twintania,
                cls.Zodiark, cls.Alpha, cls.Raiden}


    @classmethod
    def Japan(cls):
        return (cls.Mana() | cls.Gaia() | cls.Mana() | cls.Meteor())

    @classmethod
    def NorthAmerica(cls):
        return (cls.Aether() | cls.Primal() | cls.Crystal())

    @classmethod
    def Europe(cls):
        return (cls.Chaos() | cls.Light())
