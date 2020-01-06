
def get_config(file_path):
    with open(file_path) as json_data:
        config = json.load(json_data)
        print("Configuration read")
  
    return config

