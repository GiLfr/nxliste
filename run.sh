source ./next_version.sh

export current=`git tag --list --sort -tag | head -n 1`
export next=`increment_version $current`

echo "$current --> $next"

# Positionnement en development
git branch develop

if [ -n "$(git status --porcelain)" ]; then
  echo "there are changes";
else
  echo "no changes";
fi

# Commit changes
git status
git add .
git commit -m 'nvl version'
git push origin develop

# Création d'une version
# git flow release start $next develop

# Finalisation de la version
# git flow release finish $next
# git push origin master
# git push origin develop