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
    Ramuh     = auto()  
    Tonberry  = auto()      
    Typhon    = auto()  
    Unicorn   = auto()
    # Gaia
    Alexander  = auto()    
    Bahamut    = auto()
    Durandal   = auto()    
    Fenrir     = auto()
    Ifrit      = auto()
    Ridill     = auto()
    Tiamat     = auto()
    Ultima     = auto()
    Valefor    = auto()
    Yojimbo    = auto()
    Zeromus    = auto()
    # Mana
    Anima        = auto()  
    Asura        = auto()  
    Belias       = auto()  
    Chocobo      = auto()  
    Hades        = auto()  
    Ixion        = auto()  
    Mandragora   = auto()      
    Masamune     = auto()      
    Pandaemonium = auto()          
    Shinryu      = auto()  
    Titan        = auto()

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
    Ragnarok    = auto()
    Spriggan    = auto()
    # Light
    Lich        = auto()
    Odin        = auto()
    Phoenix     = auto()
    Shiva       = auto()
    Twintania   = auto()
    Zodiark     = auto()

    @classmethod
    def Elemental(cls):
        return {cls.Aegis, cls.Atomos, cls.Aegis, cls.Atomos, cls.Carbuncle, cls.Garuda, cls.Gungnir,
                cls.Kujata, cls.Ramuh, cls.Tonberry, cls.Typhon, cls.Unicorn}

    @classmethod
    def Gaia(cls):
        return {cls.Alexander, cls.Bahamut, cls.Durandal, cls.Fenrir, cls.Ifrit, cls.Ridill,
                cls.Tiamat, cls.Ultima, cls.Valefor, cls.Yojimbo, cls.Zeromus}

    @classmethod
    def Mana(cls):
        return {cls.Anima, cls.Asura, cls.Belias, cls.Chocobo, cls.Hades, cls.Ixion,
                cls.Mandragora, cls.Masamune, cls.Pandaemonium, cls.Shinryu, cls.Titan}

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
        return {cls.Cerberus, cls.Louisoix, cls.Moogle, cls.Omega, cls.Ragnarok, cls.Spriggan}

    @classmethod
    def Light(cls):
        return {cls.Lich, cls.Odin, cls.Phoenix, cls.Shiva, cls.Twintania, cls.Zodiark}


    @classmethod
    def Japan(cls):
        return (cls.Mana() | cls.Gaia() | cls.Mana())

    @classmethod
    def NorthAmerica(cls):
        return (cls.Aether() | cls.Primal() | cls.Crystal())

    @classmethod
    def Europe(cls):
        return (cls.Chaos() | cls.Light())
