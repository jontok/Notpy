#!/bin/bash
echo "Testing..."
notpy help


notpy create nb testing
notpy create pg testing testing.md -y
notpy ls nb
notpy ls pg default
notpy show testing testing.md
notpy delete pg testing testing.md -y
notpy delete nb testing -y
