% CS-E4800 Artificial intelligence
% Round: Applications via Logic Programming
%
% Base Encoding for the ASP Exercise: Tournament Scheduling
%
% Some parts of the encoding have been deleted and indicated by
% question marks "???". You are supposed to fill in the missing details
% on the basis of descriptions given as well as general understanding of
% the problem.

% Parameters: the number of teams (silently assumed to be even)

#const n=4.

% Declare the domains for the teams, fields, and weeks

team(1..n).
field(1..n/2).
week(1..n-1).

% Define matches (an ordered pair of teams)

match(T1,T2) :- team(T1), team(T2), T1<T2.

% Choose the week W for the match between T1 and T2 by default,
% unless the match is organized some other week. Encode exceptions
% using an appropriate auxiliary predicate.

thisweek(T1,T2,W) :- match(T1,T2), week(W), not thisweek(T1,T2,WX): week(WX), W!=WX.
% Add rules as needed 

% Choose the field F for the match between T1 and T2 by default,
% unless the match takes place in some other field. Encode exceptions
% using an appropriate auxiliary predicate.

thisfield(T1,T2,F) :- match(T1,T2), field(F), not thisfield(T1,T2,FX): field(FX), F!=FX.
% Add rules as needed

% Every slot (F,W) in the schedule, identified by a field F and a week W,
% must have a match scheduled

occupied(W,F) :- week(W), field(F), match(T1,T2), thisweek(T1,T2,W), thisfield(T1,T2,F).
:- not occupied(W,F), week(W), field(F).

% A team may have only one match per week

opponent(T1,W,T2) :- thisweek(T1,T2,W).
opponent(T2,W,T1) :- thisweek(T1,T2,W).
:- opponent(T,W,T2), opponent(T,W,TX), T2!=TX.

% Combine the schedule into a single relation for the ease of understanding

match(T1,T2,F,W) :- thisweek(T1,T2,W), thisfield(T1,T2,F).

% Extract solution (the following predicates are used in the evaluation)

#show match/4.
#show team/1.
