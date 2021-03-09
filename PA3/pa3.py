import sys, logic, utils
if __name__ == '__main__':
	input_file = sys.argv[1]
	fp = open(input_file, "r")
	lines = fp.readlines()
	additionalInfo = []
	query = []
	count = 0
	mine_kb = logic.PropKB()
	for i in range(len(lines)):
		if '#' not in lines[i]:
			boardSize = lines[i].rstrip()
		if '# Additional Info' in lines[i]:
			count = i
			break
	for i in range(count, len(lines)):
		if '#' not in lines[i]:
			additionalInfo.append(lines[i].rstrip())
		if '# Query Sentences' in lines[i]:
			count = i
			break
	for i in range(count,len(lines)):
		if '#' not in lines[i]:
			query.append(lines[i].rstrip())
	for i in range(len(additionalInfo)):
		temp = logic.to_cnf(utils.expr(additionalInfo[i]))
		mine_kb.tell(temp)
	x = int(boardSize[0])
	y = int(boardSize[2])
	for i in range(x):
		for j in range(y):
			b = 'B' + str(i) + str(j)
			mleft = 'M' + str(i-1) + str(j)
			mup = 'M' + str(i) + str(j+1)
			mright = 'M' + str(i+1) + str(j)
			mdown = 'M' + str(i) + str(j-1)
			if i == 0:
				if j == 0:
					#bottom left
					mine_kb.tell(logic.expr(b) | '<=>' | ((logic.expr(mup) | logic.expr(mright))))
				elif j == y-1:
					#top left
					mine_kb.tell(logic.expr(b) | '<=>' | ((logic.expr(mdown) | logic.expr(mright))))
				else:
					#left edge
					mine_kb.tell(logic.expr(b) | '<=>' | ((logic.expr(mup) | logic.expr(mright) | logic.expr(mdown))))
			elif i < x-1:
				if j == 0:
					#down edge
					mine_kb.tell(logic.expr(b) | '<=>' | ((logic.expr(mup) | logic.expr(mright) | logic.expr(mleft))))
				elif j == y-1:
					#top edge
					mine_kb.tell(logic.expr(b) | '<=>' | ((logic.expr(mdown) | logic.expr(mright) | logic.expr(mleft))))
				else:
					#middle
					mine_kb.tell(logic.expr(b) | '<=>' | ((logic.expr(mup) | logic.expr(mright) | logic.expr(mdown) | logic.expr(mleft))))
			else:
				if j ==0:
					#bottom right
					mine_kb.tell(logic.expr(b) | '<=>' | ((logic.expr(mup) | logic.expr(mleft))))
				elif j == y-1:
					#top right
					mine_kb.tell(logic.expr(b) | '<=>' | ((logic.expr(mdown) | logic.expr(mleft))))
				else:
					#right edge
					mine_kb.tell(logic.expr(b) | '<=>' | ((logic.expr(mup) | logic.expr(mleft) | logic.expr(mdown))))
	for i in range(len(query)):
		if mine_kb.ask_if_true(logic.to_cnf(utils.expr(query[i]))):
			print('Yes')
		else:
			print('No')