import load_map

def main():
	with open('templates/maps/savassona.html', 'w') as template:
	 	template.write(load_map.load_map("data/savassona/savassona.txt", True))
	with open('templates/maps/sant_joan.html', 'w') as template:
	 	template.write(load_map.load_map("data/sant_joan/sant_joan.txt", True))

	all_data = ["data/sant_joan/sant_joan.txt", "data/savassona/savassona.txt"]
	with open('templates/maps/all.html', 'w') as template:
	 	template.write(load_map.load_general_map(all_data, True))


if __name__ == '__main__':
    main()