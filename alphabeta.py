import math

def print_board(state):
    print(state[0]+'|'+state[1]+'|'+state[2])
    print(state[3]+'|'+state[4]+'|'+state[5])
    print(state[6]+'|'+state[7]+'|'+state[8])

def count(state):
    c = 0
    for cell in state:
        if cell != ' ':
            c += 1
    return c

def player(state):
    if count(state) % 2 == 0:
        return 'x'
    else :
        return 'o'

def actions(state):
    ret = []
    for i in range(len(state)):
        if state[i] == ' ':
            ret.append(i)
    return ret

def win(state, p):
    if state[0] == state[1] == state[2] == p\
        or state[3] == state[4] == state[5] == p\
        or state[6] == state[7] == state[8] == p\
        or state[0] == state[3] == state[6] == p\
        or state[1] == state[4] == state[7] == p\
        or state[2] == state[5] == state[8] == p\
        or state[0] == state[4] == state[8] == p\
        or state[2] == state[4] == state[6] == p:
        return True
    else:
        return False

def count_XO(lst):
	x = 0
	o = 0
	for c in lst:
		if c == 'x':
			x += 1
		elif c == 'o':
			o += 1
	return x,o

def evaluation(state):
	x1 = 0
	x2 = 0
	o1 = 0
	o2 = 0
	row_col_dia = [ [state[0], state[1], state[2]], \
					[state[3], state[4], state[5]], \
					[state[6], state[7], state[8]], \
					[state[0], state[3], state[6]], \
					[state[1], state[4], state[7]], \
					[state[2], state[5], state[8]], \
					[state[0], state[4], state[8]], \
					[state[2], state[4], state[6]], ]
	for l in row_col_dia:
		temp_x,temp_o = count_XO(l)
		if temp_x == 1 and temp_o == 0:
			x1 += 1
		elif temp_x == 2 and temp_o == 0:
			x2 += 1
		elif temp_x == 0 and temp_o == 1:
			o1 += 1
		elif temp_x == 0 and temp_o == 2:
			o2 += 1
	return 3*x2+x1-3*o2-o1

def stop(state):
    if count(state) == len(state) or win(state,'x') or win(state,'o'):
        return True
    else:
        return False

def utility(state):
    if win(state, 'x'):
        print('Winner: x')
        return 1
    elif win(state, 'o'):
        print('Winner: o')
        return -1
    else:
        print('Draw')
        return 0

def result(state, action):
    p = player(state)
    new_state = list(state)
    new_state[action] = p
    return new_state

def alpha_beta(state, depth_limit):
    if player(state) == 'x':
        v,values = max_value(state, -float('inf'), float('inf'), depth_limit)
        print('Max: '+str(v))
    else:
        v,values = min_value(state, -float('inf'), float('inf'), depth_limit)
        print('Min: '+str(v))
    action_list = actions(state)
    print('Actions:')
    print(action_list)
    print('Values:')
    print(values)
    for i in range(len(values)):
        if values[i] == v:
            print('Action:'+str(action_list[i])+' Value:'+str(v))
            return action_list[i]

def max_value(state, alpha, beta, depth):
    print('--- MAX STEP ---')
    print_board(state)
    if stop(state):
        return utility(state),[]
    if depth == 0:
    	return evaluation(state),[]
    v = -float('inf')
    values =[]
    for a in actions(state):
        m_v, m_values = min_value(result(state,a), alpha, beta, depth-1)
        v = max(v, m_v)
        values.append(v)
        print('Action '+str(a)+': '+str(v))
        if v >= beta:
            print('Pruned: larger than beta')
            return v,values
        alpha = max(alpha, v)
        print('Alpha: '+str(alpha))
    return v,values

def min_value(state, alpha, beta, depth):
    print('--- MIN STEP ---')
    print_board(state)
    if stop(state):
        return utility(state),[]
    if depth == 0:
    	return evaluation(state),[]
    v = float('inf')
    values = []
    for a in actions(state):
        m_v, m_values = max_value(result(state,a), alpha, beta, depth-1)
        v = min(v, m_v)
        values.append(v)
        print('Action '+str(a)+': '+str(v))
        if v <= alpha:
            print('Pruned: smaller than alpha')
            return v,values
        beta = min(beta, v)
        print('Beta: '+str(beta))
    return v,values

def main():
    state = []
    for i in range(9):
        state.append(' ')
    print('Game start')
    while not stop(state):
        input('Press enter to continue')
        action = alpha_beta(state, 2)
        state[action] = player(state)
        print_board(state)
    print('The End')


main()

