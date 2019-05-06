import configparser
import json
import os

def detect_config_file():

    cwd = os.getcwd()

    # Check working directory for psistats2.conf
    path = os.path.join(cwd, 'psistats2.conf')

    if os.path.isfile(path):
        return path

    # Check $PWD/etc for psistats2.conf
    path = os.path.join(cwd, 'etc', 'psistats2.conf')
    if os.path.isfile(path):
        return path

    # Check /etc/psistats2.conf
    path = '/etc/psistats2.conf'
    if os.path.isfile(path):
        return path


def process_plugin(plugin_config, defaults, reserved):

    conf = dict(defaults)
    conf['settings'] = {}
    
    for keyName in plugin_config:
        if keyName in reserved:
            conf[keyName] = plugin_config[keyName]
        else:
            if '\n' in plugin_config[keyName]:
                value = plugin_config[keyName].strip().split('\n')
            elif '\r' in plugin_config[keyName]:
                value = plugin_config[keyName].strip().split('\r')
            else:
                value = plugin_config[keyName].strip()
    
            conf['settings'][keyName] = value
            
    return conf

def load(fn):
    config = configparser.ConfigParser()
    config.read(fn)
    
    parsed_config = {}
    
    parsed_config['settings'] = dict(config['settings'])
    parsed_config['defaults'] = {
        'reporter': dict(config['reporter']),
        'output': dict(config['output'])
    }
    parsed_config['reporters'] = {}
    parsed_config['outputters'] = {}
    
    
    for section in config.sections():

        if section.startswith('reporter:'):

            plugin_id = section.split(':')[1]
        
            plugin_config = process_plugin(dict(config[section]), parsed_config['defaults']['reporter'], [
                'interval',
                'enabled'
            ])
            
            plugin_config['interval'] = int(plugin_config['interval'])
            plugin_config['enabled'] = False if plugin_config['enabled'] == "no" else True
            
            parsed_config['reporters'][plugin_id] = plugin_config
                                
        elif section.startswith('output:'):
            
            plugin_id = section.split(':')[1]
            plugin_config = process_plugin(dict(config[section]), parsed_config['defaults']['output'], [
                'enabled'
            ])
            
            plugin_config['enabled'] = False if plugin_config['enabled'] == "no" else True
            parsed_config['outputters'][plugin_id] = plugin_config
                        
    return parsed_config
