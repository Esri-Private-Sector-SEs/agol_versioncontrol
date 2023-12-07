
from arcgis.gis import GIS
from arcgis.gis import Item
from arcgis.features import FeatureSet, Feature

gis = GIS('home') # login scheme subject to change

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class CircularLinkedList:
    def __init__(self):
        self.head = Node(None)
        self.tail = Node(None)
        self.head.next = self.tail
        self.tail.next = self.head
        
    def add(self, data):
        newNode = Node(data)
    
        if self.head.data is None:
            self.head = newNode
            self.tail = newNode
            newNode.next = self.head
        else:
            self.tail.next = newNode
            self.tail = newNode
            self.tail.next = self.head
            
    def findNextNode(self, element):
        current = self.head
      
        if (self.head == None):
            print("CLL is empty")
        else:
            while True:
                if (current.data == element):
                    print("Element is present.")
                    return current.next.data
                current = current.next

                if (current == self.head):
                    print("Element not present.")
        
class StagedItem(Item):
    """
    Class to interface with a Staged item, which is 3 seperate items under one folder. It contains
    the live version, sandbox version and staging version (interim). We can actively switch between which
    version is 'active' at any time. This allows us to actively change 
    """
    
    def __init__(self, id):
        self.live = Item(id)
        self.active = None # active dev state of the Item
        
        # move item to dev folder where all versioning happens
        gis.content.create_folder(f"{self.title} Dev Env")
        self.move(f"{self.title} Staging Env")
        
        # make sandbox item
        sandbox_clone = gis.content.clone_items([self], folder=f"{self.title} Dev Env")
        sandbox_clone = sandbox_clone[0]
        sandbox_clone.update(item_properties={'title':f'{self.title} SANDBOX'})
        self.sandbox = sandbox_clone
        
        # make staging item
        staging_clone = gis.content.clone_items([self], folder=f"{self.title} Dev Env")
        staging_clone = staging_clone[0]
        staging_clone.update(item_properties={'title':f'{self.title} STAGING'})
        self.staging = staging_clone
        
        # CLL for devEnv workflow:
        self.devEnvs = CircularLinkedList()
        self.devEnvs.add(self.live)
        self.devEnvs.add(self.sandbox)
        self.devEnvs.add(self.staging)
    
    def show_workflow(self):
        """TODO Prints CLL"""
        pass
        
    def set_active(self, active_env):
        "Change the active development environment for the StagedItem TODO"
        self.active = active_env
            
    def push(self):
        """TODO description here"""
        
        def _push(active_env=self.active):
            
            nextStage = self.devEnvs.findNextNode(active_env)
            
            fs = gis.content.get(active_env.id)
            fl = fs.layers[0]
            
            fs_next = gis.content.get(nextStage.id)
            fl_next = fs_next.layers[0]
            
            features = fl.query(where="")
            fl_next.edit_features(updates=features)
            print(f"Advancing next active environment to {nextStage}.")
            self.active = nextStage
        
        if self.active == "None":
            print("No active environment is set. Please use the set_active() method to continue.")
            return
        
        _push()
    
    def discard(self):
        """Discards changes in the environment. TODO"""
    
        head_fs = gis.content.get(self.DevEnvs.head.data)
        head_fl = head_fs.layers[0]
        features = head_fl.query(where="")
        head_fl.edit_features(updates=features)
        
        print(f"Changes discarded. Setting active state back to head env ...")
        self.active_env = self.DevEnvs.head.data

            
    
        
        
        
        
        
        
