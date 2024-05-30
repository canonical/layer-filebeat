from unittest import TestCase
from unittest.mock import Mock, patch

from filebeat import render_filebeat_template

@patch("filebeat.service", Mock)
@patch("filebeat.get_package_version", list)
@patch("elasticbeats.model_info_cache", Mock)
@patch("elasticbeats.principal_unit_cache", Mock)
@patch("elasticbeats.mkdir", Mock)
@patch("filebeat.manage_filebeat_logstash_ssl", Mock)
class TestTemplates(TestCase):
    @patch("filebeat.config")
    @patch("elasticbeats.config")
    @patch("elasticbeats.write_file")
    def test_render_filebeat_template_valid_yaml(self, mock_write_file: Mock, mock_elasticbeats_config, mock_filebeat_config):
        new_config = {}
        new_config['logstash_hosts'] = ''
        new_config['kafka_hosts'] = ''
        new_config['extra_configs_default_input'] = '''
multiline:
    pattern: "^([0-9]{4}-[0-9]{2}-[0-9]{2}|[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3})"
    negate: true
    match: after
'''
        mock_filebeat_config.return_value = new_config
        mock_elasticbeats_config.return_value = new_config

        render_filebeat_template()

        expected_yaml = b'''
# WARNING! This file is managed by Juju. Edits will not persist.
# Edit at your own risk
filebeat:
  prospectors:
    -
      paths:
        
        
      input_type: log
      exclude_files: 
      exclude_lines: 
      scan_frequency: 10s
      harvester_buffer_size: 
      max_bytes: 
      
      multiline:
          pattern: "^([0-9]{4}-[0-9]{2}-[0-9]{2}|[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3})"
          negate: true
          match: after

      fields:
        juju_model_name: None
        juju_model_uuid: None
        juju_principal_unit: None
        
    
    
  registry_file: /var/lib/filebeat/registry

logging:
  
  level: 
  metrics.enabled: false

output:



'''.lstrip()
        mock_write_file.assert_called_once_with('/etc/filebeat/filebeat.yml', expected_yaml)

    @patch("filebeat.config")
    @patch("elasticbeats.config")
    @patch("elasticbeats.write_file")
    def test_render_filebeat_template_invalid_yaml(self, mock_write_file: Mock, mock_elasticbeats_config, mock_filebeat_config):
        new_config = {}
        new_config['logstash_hosts'] = ''
        new_config['kafka_hosts'] = ''
        new_config['extra_configs_default_input'] = 'a: a:'
        mock_filebeat_config.return_value = new_config
        mock_elasticbeats_config.return_value = new_config

        render_filebeat_template()

        expected_yaml = b'''
# WARNING! This file is managed by Juju. Edits will not persist.
# Edit at your own risk
filebeat:
  prospectors:
    -
      paths:
        
        
      input_type: log
      exclude_files: 
      exclude_lines: 
      scan_frequency: 10s
      harvester_buffer_size: 
      max_bytes: 
      fields:
        juju_model_name: None
        juju_model_uuid: None
        juju_principal_unit: None
        
    
    
  registry_file: /var/lib/filebeat/registry

logging:
  
  level: 
  metrics.enabled: false

output:



'''.lstrip()
        mock_write_file.assert_called_once_with('/etc/filebeat/filebeat.yml', expected_yaml)
