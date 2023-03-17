i=0
limit=30
rm -f indexListACS.json

while True
do
  offset=$(( limit * i ))
  set -x
  indexes=$(acs indexes list --count $limit --offset $offset)
  echo $?
  if [[ "$indexes" = "null" ]]; then
    echo "Stopping now"
    break
  fi
  echo $indexes | tee -a indexListACS.json
  ((i=i+1))
  echo i: $i
done
echo "Formatting IndexList"
cat indexListACS.json | jq -s add > remote_indexList.json