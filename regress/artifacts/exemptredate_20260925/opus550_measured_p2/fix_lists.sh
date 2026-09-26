set -u
cd /tmp/opus550p2 || exit 1
# The first version printed AB:n=$(echo $ab | wc -w), which reads "none" as n=1 -- a wrong record.  Count 0 for "none".
sed -i 's/AB:$(echo $ab | wc -w | sed .s\/^\/n=\/.)/AB:$( [ "$ab" = none ] \&\& echo n=0 || echo "n=$(echo $ab | wc -w)" )/' lists.sh
grep -n 'AB:' lists.sh | head -2
