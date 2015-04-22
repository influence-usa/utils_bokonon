find ~/data/data/transformed/sopr_html "*.json" | xargs cat | jq ".registrant.name" | sort -u > names.txt
