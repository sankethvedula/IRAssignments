index = 0;
for name in *.txt
do
	cp "${name}" "${index}.txt"
	index = $(index + 1)
done