#!/bin/bash

container="container"
total_files=$(find . -maxdepth 1 -name "*.{png,jpg,jpeg,gif}" | wc -l)
counter=0

if [ ! -d "$container" ]; then
  mkdir "$container"
fi

for file in *.{png,jpg,jpeg,gif}
do
    means=($(identify -verbose $file | grep "mean:" | awk '{print $2}'))
    mean=0
    for i in "${means[@]}"
    do
        mean=$(echo "($mean + $i)/${#means[@]}" | bc -l)
    done
    if (( $(echo "$mean > 80" | bc -l) )); then
        mv $file $container
    fi
    counter=$((counter+1))
    echo -ne "Processing $file... $(echo "scale=2; $counter*100/$total_files" | bc)%\r"
done

echo "Done!"

