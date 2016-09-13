mv project $1
find . -name '*.py' -o -name '*.conf' -o -name '*.vcl' -o -name 'entrypoint.sh' -type f | xargs perl -p -i -e "s/{{project}}/$1/g"