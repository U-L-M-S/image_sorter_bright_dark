#!/bin/bash

container="container"
total_files=$(find . -maxdepth 1 -name "*.png" | wc -l)
counter=0

if [ ! -d "$container" ]; then
mkdir "$container"
fi

for file in *.png
do
# Get all the means
means=($(identify -verbose "$file" | awk '/mean:/ {print $2}'))
mean=0
# Iterate through all the means
for i in "${means[@]}"
do
mean=$(echo "($mean + $i)/${#means[@]}" | bc -l)
done
if (( $(echo "$mean > 80" | bc -l) )); then
mv "$file" "$container"
continue
fi
white_percent=$(convert "$file" -format "%[fx:mean*100]" info:)
# Check if the percentage of white color is greater than 40%
if [ $(echo "$white_percent > 40" | bc) -eq 1 ]; then
  echo "Moving $file to container"
  mv "$file" "$container"
fi
counter=$((counter+1))
echo -ne "Processing $file... $(echo "scale=2; $counter*100/$total_files" | bc)%\r"

done

echo "Done. $counter of $total_files images moved into the container"
