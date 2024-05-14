#!/bin/sh
# This script is used in the UI Dockerfile to replace values of environment variables in the vite.js build files, at container startup. solution based on 
# https://dev.to/sanjayttg/dynamic-environment-variables-for-dockerized-react-apps-5bc5
# https://github.com/vitejs/vite/issues/10059
echo "**** List of environment variables"
env

echo "*** Replacing environment variables in the build files"
for i in $(env | grep PROMPT_SAIL_ENV_PLACEHOLDER_)
do
    key=$(echo $i | cut -d '=' -f 1)
    value=$(echo $i | cut -d '=' -f 2-)
 
    echo "--- Replacing $key with $value"
    echo $key=$value
    # sed All files
    # find /usr/share/nginx/html -type f -exec sed -i "s|${key}|${value}|g" '{}' +

    #find /app/dist -type f \( -name '*.js' -o -name '*.css' \) | xargs sed 's|${key}|${value}|gp'

    # sed JS and CSS only
    find /app/dist -type f \( -name '*.js' -o -name '*.css' \) -exec sed -i "s|${key}|${value}|g" '{}' +
done

echo "*** Replacing environment variables in the build files [done]"