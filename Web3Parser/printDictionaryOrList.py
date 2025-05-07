def print_dictionary_or_list(data, indent=''):
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, dict):
                print_dictionary_or_list(value, indent + '  ')
            elif isinstance(value, list):
                print(f"{indent}{key}:")
                print_dictionary_or_list(value, indent + '  ')                
            else:                
                print(f"{indent}{key}: {value}")
    if isinstance(data, list):
        for value in data:
            if isinstance(value, dict) or isinstance(value, list):
                print_dictionary_or_list(value, indent + '  ')
            else:                
                print(f"{indent}{value}")