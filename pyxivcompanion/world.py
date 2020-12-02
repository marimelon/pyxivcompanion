from enum import Enum, auto

class XIV_WORLD(Enum):
    #Elemental
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
    #Gaia
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
    #Mana
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
    def Japan(cls):
        return (cls.Mana() | cls.Gaia() | cls.Mana())