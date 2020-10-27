% CS-E4800 Artificial intelligence
% Round: Applications via Logic Programming
%
% Base Encoding for the ASP Exercise: AI Planning / Tic-Tac-Toe 
%
% Some parts of the encoding have been deleted and indicated by
% question marks "???". You are supposed to fill in the missing details
% on the basis of descriptions given as well as general understanding of
% the problem.

% The dimension (n x n) of the Tic-Tac-Toe board
% (can be changed from the command line -cn=... of clingo/gringo).

#const n=3.

% Domains for coordinate values, time steps, and players
% The domain of "tuples" is handy in a number of rules
% that concern the moves of players and changes in state

coord(???).
step(???).
player(x).
player(o).
tuple(P,X,Y,T) :- player(P), coord(X), coord(Y), step(T).

% Choose the moves of the players: at most one move per time step 0..n*n-1
% - play(P,X,Y,T) means that player P puts his/her mark at
%   coordinates X,Y at step T
% - mark(P,X,Y,T) records the state of the board which is
%   updated on the basis of moves made (and later by laws of inertia)

{ play(P,X,Y,T): ??? } ??? :- step(T), ??? .
mark(P,X,Y,T+1) :- ??? .

% A player must not mark the same cell again

:- play(P,X,Y,T+1), ???, tuple(P,X,Y,T), step(T+1).

% Subsequent moves by the same player are forbidden
% - turn(P,T) means that player P makes her/his move at step T

turn(P,T) :- ??? .
:- turn(P,T), ???, player(P), step(T), ??? .

% Plays are contiguous and should not contain gaps
% - used(T): means that a move is made at step T

used(T) :- play(P,X,Y,T), tuple(P,X,Y,T).
:- ???, step(T-1), step(T), T>0.

% Detect the end of play using the used/1 predicate

last(T+1) :- ???, step(T), step(T+1).

% Inertia: a cell that is marked by a played will stay marked

mark(???) :- mark(???), tuple(P,X,Y,T), step(T+1).

% Detecting winning positions
% - winning(P,T) means that player P has reached a winning position 
%   at time step T, i.e., has his/her mark on either
%   1. an entire column at coordinate X,
%   2. an entire row at coordinate Y,
%   3. the entire diagonal 1,1 ??? n,n; or
%   4. the entire diagonal 1,n ??? n,1.

winning(P,T) :- player(P), step(T), coord(X), mark(P,X,Y,T): coord(Y).
winning(P,T) :- player(P), step(T), ??? .
winning(P,T) :- player(P), step(T), mark(P,X,X,T): coord(X).
winning(P,T) :- player(P), step(T), ??? .

% Determine the winner and deny moves if a winning position has been reached

winner(P) :- ??? .
:- used(T), ???, step(T).

% Draws

draw :- last(n*n), not winner(P): player(P).

% Ensure that either player has won the game or a draw resulted

:- not ???, not ???, not ??? .

#show play/4.
#show winner/1.
#show draw/0.
