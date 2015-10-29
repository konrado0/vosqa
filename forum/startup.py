import sys
import os

from forum.modules import get_modules_script

get_modules_script('settings')
get_modules_script('startup')


import forum.badges
import forum.subscriptions
import forum.registry
get_modules_script('registry')



