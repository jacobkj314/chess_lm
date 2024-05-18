def edge(coord):
	return coord in [0,7]

def corner(file, rank):
	return edge(file) and edge(rank)

def move_check(f, r, x, y):
	return not (x==f and y==r)



ranks = ['1','2','3','4','5','6','7','8']
files = ['a','b','c','d','e','f','g','h']

# KING
K = ['O-O','O-O-O']
for file in files:
	for rank in ranks:
		K.append('K' + file + rank)

# PAWNS
P = []
for f, file in enumerate(files):
	for r, rank in enumerate(ranks):
		P.append(file + rank) #vanilla pawn moves
		for capture_from_file in [f-1, f+1]:
			if 0 <= capture_from_file <= 7:
				# # # # # P.append(files[capture_from_file] + 'x' + file + rank) #capture (diagonal) moves
				P.append(files[capture_from_file] + '' + file + rank) #capture (diagonal) moves
for pawn_move in P:
	if pawn_move[-1] in ['1','8']:
		for promotion in ['=N','=B','=R','=Q']:
			P.append(pawn_move + promotion)

def piece_moves(piece_name, piece_move_check, piece_file_disambiguate, piece_rank_disambiguate, piece_2d_disambiguate):
	moves = set()

	#target file and rank
	for f, file in enumerate(files):
		for r, rank in enumerate(ranks):
			
			moves.add(piece_name + file + rank) #vanilla move

			#origin file and rank
			for x, from_file in enumerate(files):
				for y, from_rank in enumerate(ranks):

					#check that move from origin to target is legal for the piece
					if piece_move_check(f, r, x, y):

						#if the target might need disambiguation, add that option
						if piece_file_disambiguate(f, r):
							moves.add(piece_name + from_file + file + rank)
						if piece_rank_disambiguate(f, r):
							moves.add(piece_name + from_rank + file + rank)
						if piece_2d_disambiguate(f, r):
							moves.add(piece_name + from_file + from_rank + file + rank)

	return list(moves)

# QUEEN
q_move_check = lambda f, r, x, y : move_check(f, r, x, y) and ((x==f) or (y==r) or (abs(x-f) == abs(y-r))) #check if it is a valid queen move)
q_file_disambiguate = lambda f, r : True
q_rank_disambiguate = lambda f, r : True
q_2d_disambiguate = lambda f, r : True
Q = piece_moves('Q', q_move_check, q_file_disambiguate, q_rank_disambiguate, q_2d_disambiguate)

# ROOK
r_move_check = lambda f, r, x, y : move_check(f, r, x, y) and ((x==f) or (y==r))
r_file_disambiguate = lambda f, r : not edge(f)
r_rank_disambiguate = lambda f, r : not edge(r)
r_2d_disambiguate = lambda f, r : False
R = piece_moves('R', r_move_check, r_file_disambiguate, r_rank_disambiguate, r_2d_disambiguate)

# BISHOP
b_move_check = lambda f, r, x, y : move_check(f, r, x, y) and (abs(x-f) == abs(y-r))
b_file_disambiguate = lambda f, r : not edge(r)
b_rank_disambiguate = lambda f, r : not edge(f)
b_2d_disambiguate = lambda f, r : not (edge(f) or edge(r))
B = piece_moves('B', b_move_check, b_file_disambiguate, b_rank_disambiguate, b_2d_disambiguate)

# KNIGHT
n_move_check = lambda f, r, x, y : move_check(f, r, x, y) and {abs(x-f), abs(y-r)} == {1,2}
n_file_disambiguate = lambda f, r : not edge(f)
n_rank_disambiguate = lambda f, r : not edge(r)
n_2d_disambiguate = lambda f, r : not (f in [2,3,4,5] and r in [2,3,4,5])
N = piece_moves('N', n_move_check, n_file_disambiguate, n_rank_disambiguate, n_2d_disambiguate)


MOVES = K + P + Q + R + B + N

