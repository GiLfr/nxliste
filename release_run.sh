source ./next_version.sh

export current=`git tag --list --sort -tag | head -n 1`
export next=`increment_version $current`

echo "$current --> $next"

# Positionnement en development
git checkout develop

# Commit si changement
if [ -n "$(git status --porcelain)" ]; then
    echo "Commit des changements ...";
    git add .
    git commit -m "Release $next"
    git push origin develop
else
    echo "Pas de changement";
fi

# Création d'une version
git flow release start $next develop

# Finalisation de la version
git flow release finish $next
git push origin master
git push origin develop
git checkout develop
