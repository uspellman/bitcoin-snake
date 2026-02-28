#!/bin/bash

# Remove Python frameworks and executables
sudo rm -rf /Library/Frameworks/Python.framework
sudo rm -rf /usr/local/bin/python*

# Remove related directories
sudo rm -rf /usr/local/lib/python*
sudo rm -rf /usr/local/include/python*

# Clean up Homebrew installations
if command -v brew &> /dev/null; then
    brew uninstall --force python@3.9 python@3.8 python@3.7 # Adjust versions as necessary
    brew cleanup
fi

# Remove configuration files
sudo rm -rf /usr/local/etc/python*

echo "Python uninstallation process completed. Please check your PATH and shell configuration files for any Python references and remove them manually."