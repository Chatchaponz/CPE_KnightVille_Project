'''
role - Manage each role and do their special

[Class] + Role

last updated: 31 Oct 2021
'''
class Role:
    '''
    Role - Store role and do their ability 
    '''
    def __init__(self, role: int) :
        '''
        __init__ - Constructor of Role class
        + role - Interger indicate role
        '''
        self.__allRoles = [
            ["Merlin", "Good"], 
            ["Percival", "Good"],
            ["Royal Servant Of Arthur", "Good"],
            ["Mordred", "Evil"],
            ["Assassin", "Evil"],
            ["Morgana", "Evil"],
            ["Mininon Of Mordred", "Evil"],
            ["Oberon", "Evil"]
        ] # All role in game

        self.__thisRole = self.__allRoles[role] # Current role

    def getName(self):
        '''
        getName - Getter method for get this role's name

        + return - role's name
        '''
        return self.__thisRole[0]
    
    def getIdentity(self):
        '''
        getIdentity - Getter method for get this role's identity (good, evil)
        
        + return - role's identity
        '''
        return self.__thisRole[1]
    
    def doSpecial(self, players):
        '''
        doSpecial - Do special ability of each role
        '''
        for player in players:
            
            thisPlayerRole = player.getRole()
            playerRoleName = thisPlayerRole.getName()
            playerIdentity = thisPlayerRole.getIdentity()

            if self.getName() == self.__allRoles[0][0]: # Merlin
                if (playerIdentity == "Evil" and 
                    playerRoleName != self.__allRoles[3][0]): # Evil and Mordred
                    player.setIdentityReveal(True)
                    if playerRoleName == self.__allRoles[7][0]: # Oberon
                        player.setRoleReveal(True)

            if self.getName() == self.__allRoles[1][0]: # Percival
                if (thisPlayerRole.getName() == self.__allRoles[0][0] or # Merlin or
                    thisPlayerRole.getName() == self.__allRoles[5][0]):  # Morgana
                    player.setUnknownReveal(True)
        
            if self.getIdentity() == "Evil":
                if (playerIdentity == "Evil" and 
                    playerRoleName != self.__allRoles[7][0]): # Oberon
                    player.setIdentityReveal(True)
