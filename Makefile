PNGS=$(wildcard *.png)

all:
	@for i in $(PNGS); do \
		echo $$i; \
		./converter.py $$i $${i%_*}.txt; \
	done;

clean:
	-rm *.txt

