#!/bin/bash
echo "Running all projects"
tmuxinator start webclient && tmuxinator start cloud-api && tmuxinator start cloud-portal

