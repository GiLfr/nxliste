source ./next_version.sh

export current=`git tag --list --sort -tag | head -n 1`
export next=`increment_version $current`

echo "$current --> $next"

# Création d'une version
git flow release start $next develop

# Finalisation de la version
git flow release finish $next