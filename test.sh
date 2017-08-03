# create test images
for i in {1..100}; do
	convert -verbose -size $((($i/34%2)*50+50))x$((($i/34%2)*50+50)) xc:black -background white \
		-gravity Center -extent 200x200 \
		-fill red -pointsize 20 -annotate 0 $i \
		$(printf tmp_%03d.jpg $i)
done
for ws in 5 10 20; do
	for a in 5 10 20; do
		./windowblend.py --inglob 'tmp_???.jpg' --windowsize $ws --attack $a test_windowsize-$ws-attack-$a.mkv
	done
done
