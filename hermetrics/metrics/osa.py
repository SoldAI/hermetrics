#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 25 09:22:59 2019
Optimal String Alignment distance
@author: kampamocha
"""
# https://en.wikipedia.org/wiki/Damerau%E2%80%93Levenshtein_distance
# Optimal String Alignment (OSA) also known as Restrited Edit distance is a 
# simpler version of the Damerau-Levenshtein (DL) distance having the condiiton
# that no substring is edited more than once, whereas the DL distance presents
# no such restriction

def distance(source, target, cost=(1, 1, 1, 1)):
    """OSA (Optimal String Alignment) distance with costs for deletion, insertion, substitution and transposition"""
    s_len = len(source)
    t_len = len(target)  

    if type(cost) == int or type(cost) == float:
        del_cost = ins_cost = sub_cost = tra_cost = cost
    else:
        del_cost, ins_cost, sub_cost, tra_cost = cost
    
    if s_len == 0:
        return t_len * ins_cost
    if t_len == 0:
        return s_len * del_cost

    rows = s_len + 1
    cols = t_len + 1
    D = [[0 for j in range(cols)] for i in range(rows)]

    # source prefixes can be transformed into empty strings 
    # by deletions:
    for i in range(1, rows):
        D[i][0] = i * del_cost
    # target prefixes can be created from an empty source string
    # by inserting the characters
    for j in range(1, cols):
        D[0][j] = j * ins_cost
        
    for j in range(1, cols):
        for i in range(1, rows):
            deletion = D[i-1][j] + del_cost
            insertion = D[i][j-1] + ins_cost
            substitution_or_equal = D[i-1][j-1]
            if source[i-1] != target[j-1]:
                substitution_or_equal += sub_cost
                
            D[i][j] = min(deletion, insertion, substitution_or_equal)
            
            if i > 1 and j > 1 and source[i-1] == target[j-2] and source[i-2] == target[j-1]:
                D[i][j] = min(D[i][j], D[i-2][j-2] + tra_cost)
    
 
    return D[rows-1][cols-1]


# See comments inside functions
def max_distance(source, target, cost=(1,1,1,1)):
    """
    Levenshtein maximum distance value.
    This version of max_distance does not consider transpositions
    because doing it will supress the effect of transpositions in the
    normalized distance.
    
    """
    s_len = len(source)
    t_len = len(target)

    if type(cost) == int or type(cost) == float:
        del_cost = ins_cost = sub_cost = tra_cost = cost
    else:
        del_cost, ins_cost, sub_cost, tra_cost = cost

    max_del = max(s_len - t_len, 0)
    max_ins = max(t_len - s_len, 0)
    max_sub = min(s_len, t_len)
    
    return max_del*del_cost + max_ins*ins_cost + max_sub*sub_cost


def max_distance_with_transpositions(source, target, cost=(1,1,1,1)):
    """
    Levenshtein maximum distance value.
    This version does consider transpositions, but used with the
    normalization function supress the effect of them
    
    """
    s_len = len(source)
    t_len = len(target)

    if type(cost) == int or type(cost) == float:
        del_cost = ins_cost = sub_cost = tra_cost = cost
    else:
        del_cost, ins_cost, sub_cost, tra_cost = cost
    # Adjust substitution and transposition costs
    sub_cost = min(sub_cost, del_cost + ins_cost)
    tra_cost = min(tra_cost, sub_cost * 2)
    # Calc maximum number of operations
    max_del = max(s_len - t_len, 0)
    max_ins = max(t_len - s_len, 0)
    max_sub = min(s_len, t_len)
    max_tra = int(max_sub / 2)
    extra_sub = max_sub % 2
    # Calc max distances per operation type
    del_dist = max_del * del_cost
    ins_dist = max_ins * ins_cost
    sub_dist = max_sub * sub_cost
    tra_dist = max_tra * tra_cost + extra_sub * sub_cost
       
    return del_dist + ins_dist + min(sub_dist, tra_dist)
