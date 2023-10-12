# Here is the full code with the changes to maintain a backup history for reverting changes

import os
import yaml
import copy
import uuid
from bgsutils.bgsutils import log_error

class YAMLDataStore:
    """A class to store data in a YAML file.
       # Example usage:
       ```
        try:
            datastore = YAMLDataStore(filepath='example.yaml', dirpath='optional_dir')
            datastore.update_and_store_data(['section', 'subsection', 'field'], 'value1', save_all=True)
            datastore.update_and_store_data(['section', 'subsection', 'field'], 'value2', save_all=True)
            datastore.revert_changes()  # Should revert to 'value1'
        except Exception as e:
            print(f"An error occurred: {e}")
        ```
        """
    def __init__(self, filepath: str = None, dirpath: str = None):

        if filepath is None:
            # Generate a temporary name if filepath is not provided
            
            filepath = f"temp_{uuid.uuid4().hex}.yaml"            
            print(f"Filepath not provided. Creating a new file with name: {filepath}")           
        else:
            if dirpath is None:
                dirpath = os.getcwd()
             
            if os.path.exists(dirpath) and os.path.isdir(dirpath):
                if not os.path.dirname(filepath):
                    self.filepath = os.path.join(dirpath, filepath)
                    self.dirpath = dirpath
                else:
                    self.filepath = filepath
                    self.dirpath = os.path.dirname(self.filepath)

        
        self.data = {}
        self.backup_history = []
        self.backup_data = {}
        self._initialize_data()            
        
    
    def _initialize_data(self):
        """Initialize or load existing data."""
        if not os.path.exists(self.dirpath):
            os.makedirs(self.dirpath)
        
        if self.filepath and os.path.exists(self.filepath):
            with open(self.filepath, 'r', encoding='utf-8') as file:
                self.data = yaml.safe_load(file) or {}
        else:
            temp_name = f"temp_{uuid.uuid4().hex}.yaml"
            self.filepath = os.path.join(self.dirpath, temp_name)
            print(f"File not found. Creating a new file with name: {self.filepath}")
        
        self.backup_history.append(copy.deepcopy(self.data))
    
    def save(self):
        """Save the data to the file."""
        with open(self.filepath, 'w', encoding='utf-8') as file:
            yaml.safe_dump(self.data, file)
        self.backup_history.append(copy.deepcopy(self.data))
    
    def revert_changes(self):
        """Revert to the last saved data."""
        if len(self.backup_history) >= 2:
            self.backup_history.pop()
            self.data = self.backup_history[-1]
            self.save()
        else:
            print("No backup available to revert to.")

    def update_and_store_data(self, keys_list, new_value, save_all=True):
        """Update and automatically save the data."""
        data = self.data
        for key in keys_list[:-1]:
            data = data.setdefault(key, {})
        
        data[keys_list[-1]] = new_value
        
        if save_all:
            self.save()


