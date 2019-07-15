spb:
	python3.7 main.py spb 1000
ekb:
	python3.7 main.py ekb 1000
msk:
	python3.7 main.py msk 1000

screenshot_all:
	python3.7 -m http.server 2019 &
	python3.7 screenshot_map.py spb 4000 3000
	python3.7 screenshot_map.py ekb 4000 3000
	python3.7 screenshot_map.py msk 4000 3000
kill_server:
	sudo kill $$(sudo lsof -ti :2019)


	
