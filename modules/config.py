import json
import os


class Config:
    # Subclass for the "rest" section of the config
    class RestConfig:
        def __init__(self, data):
            # Path to the REST module
            self.module_path = data.get('module_path')
            # Path to the REST module
            self.module_class = data.get('module_class')
            # Base URL for the REST API
            self.url = data.get('url')
            # API key for authentication
            self.api_key = data.get('api_key')
            # Project ID for the API context
            self.project_id = data.get('project_id')

        def __repr__(self):
            return f"<RestConfig url={self.url}, project_id={self.project_id}>"

    # Subclass for the "logging" section of the config
    class LoggingConfig:
        def __init__(self, data):
            # Whether logging is enabled
            self.enabled = data.get('enabled', False)
            # Logging level (e.g., info, debug, warning)
            self.log_level = data.get('log_level', 'info')
            # Directory path for log files
            self.log_path = data.get('log_path', './logs/')
            # Log file name
            self.log_file = data.get('log_file', 'app.log')

        def __repr__(self):
            return f"<LoggingConfig enabled={self.enabled}, log_file={self.log_file}>"

    def __init__(self, filepath):
        # Load the full JSON configuration into memory
        self._data = self._load_config(filepath)

        # Parse and assign structured config sections
        self._rest = Config.RestConfig(self._data.get('rest', {}))
        self._logging = Config.LoggingConfig(self._data.get('logging', {}))
        self._token = self._data.get('token')
        self._timeout = self._data.get('timeout')
        self._channel_id = self._data.get('channel_id')

    def _load_config(self, filepath):
        """
        Reads and parses the JSON config file.
        Raises informative errors if something goes wrong.
        """
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Configuration file '{filepath}' not found.")
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse JSON in '{filepath}': {e}")

    # Provide structured access to the "rest" section
    @property
    def rest(self):
        return self._rest

    # Provide structured access to the "logging" section
    @property
    def logging(self):
        return self._logging

    # Provide access to the "token" value
    @property
    def token(self):
        return self._token
    
    # Provide access to the "timeout" value
    @property
    def timeout(self):
        return self._timeout
    
    # Provide access to the "channel ID" value
    @property
    def channel_id(self):
        return self._channel_id

    def get(self, key, default=None):
        """
        Generic getter for any top-level config value.
        """
        return self._data.get(key, default)
