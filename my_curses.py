import curses 


DATA = {
	'Crossroads': 6,
	'Ironman': 90,
	'Thor': 71,
	'Silver Lining playbook': 96,
}

WIDTH = 34
HEADER = """
 --------------------------------
| Title              | Sentiment |
 --------------------------------
"""
FOOTER = " -------------------------------- "

screen = curses.initscr() 
curses.noecho() 
curses.curs_set(0) 
screen.keypad(1) 

screen.addstr("This is a Sample Curses Script\n\n", curses.A_STANDOUT) 

while True: 
	screen.addstr(HEADER)
	for title, rating in DATA.iteritems():
		if len(title) < 21:
			title = title
		else:
			title = title[:15] + '...'
		screen.addstr(("| %s" % (title,)).ljust(21, ' '))
		screen.addstr(("| %d" % (rating,)).ljust(12, ' '))
		screen.addstr("|\n")
	screen.addstr(FOOTER)

	event = screen.getch() 
	if event == ord("q"):
		break 

curses.endwin()