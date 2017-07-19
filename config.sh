#!/bin/bash
if hash pip 2>/dev/null; then
    pip install --upgrade google-api-python-client
else
    sudo easy_install pip
    pip install --upgrade google-api-python-client
fi
