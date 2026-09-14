def edit_distance_with_operations(costs, str_a, str_b):
    n_val = len(str_a)
    m_val = len(str_b)
    
    cost_replace = costs[0]
    cost_insert = costs[1]
    cost_delete = costs[2]
    cost_delete_two = costs[3] if len(costs) > 3 else cost_delete * 2
    
    dp_table = [[0] * (m_val + 1) for _ in range(n_val + 1)]
    for j_idx in range(1, m_val + 1):
        dp_table[0][j_idx] = dp_table[0][j_idx - 1] + cost_insert
    
    for i_idx in range(1, n_val + 1):
        dp_table[i_idx][0] = dp_table[i_idx - 1][0] + cost_delete
    
    for i_idx in range(1, n_val + 1):
        for j_idx in range(1, m_val + 1):
            if str_a[i_idx - 1] == str_b[j_idx - 1]:
                replace_cost = 0
            else:
                replace_cost = cost_replace
            
            dp_table[i_idx][j_idx] = dp_table[i_idx - 1][j_idx - 1] + replace_cost
            
            insert_cost = dp_table[i_idx][j_idx - 1] + cost_insert
            if insert_cost < dp_table[i_idx][j_idx]:
                dp_table[i_idx][j_idx] = insert_cost
            
            delete_cost = dp_table[i_idx - 1][j_idx] + cost_delete
            if delete_cost < dp_table[i_idx][j_idx]:
                dp_table[i_idx][j_idx] = delete_cost
            
            if i_idx >= 2 and str_a[i_idx - 1] != str_a[i_idx - 2]:
                delete_two_cost = dp_table[i_idx - 2][j_idx] + cost_delete_two
                if delete_two_cost < dp_table[i_idx][j_idx]:
                    dp_table[i_idx][j_idx] = delete_two_cost
    
    operations = restore_operations(dp_table, str_a, str_b, cost_replace, 
                                   cost_insert, cost_delete, cost_delete_two)
    
    return operations, dp_table[n_val][m_val]


def restore_operations(dp_table, str_a, str_b, cost_replace, cost_insert, cost_delete, cost_delete_two):
    i_idx = len(str_a)
    j_idx = len(str_b)
    operations = []
    
    while i_idx > 0 or j_idx > 0:
        if i_idx == 0:
            operations.append('I')
            j_idx -= 1
        elif j_idx == 0:
            if i_idx >= 2 and str_a[i_idx - 1] != str_a[i_idx - 2]:
                two_del_cost = dp_table[i_idx - 2][j_idx] + cost_delete_two
                if dp_table[i_idx][j_idx] == two_del_cost:
                    operations.append('D')
                    operations.append('D')
                    i_idx -= 2
                    continue
            
            operations.append('D')
            i_idx -= 1
        else:
            current_cost = dp_table[i_idx][j_idx]
            
            if i_idx >= 2 and str_a[i_idx - 1] != str_a[i_idx - 2]:
                two_del_cost = dp_table[i_idx - 2][j_idx] + cost_delete_two
                if current_cost == two_del_cost:
                    operations.append('D')
                    operations.append('D')
                    i_idx -= 2
                    continue
            
            if str_a[i_idx - 1] == str_b[j_idx - 1]:
                replace_cost = 0
            else:
                replace_cost = cost_replace
            
            match_cost = dp_table[i_idx - 1][j_idx - 1] + replace_cost
            if current_cost == match_cost:
                if str_a[i_idx - 1] == str_b[j_idx - 1]:
                    operations.append('M')
                else:
                    operations.append('R')
                i_idx -= 1
                j_idx -= 1
                continue
            
            insert_cost = dp_table[i_idx][j_idx - 1] + cost_insert
            if current_cost == insert_cost:
                operations.append('I')
                j_idx -= 1
                continue
            
            delete_cost = dp_table[i_idx - 1][j_idx] + cost_delete
            if current_cost == delete_cost:
                operations.append('D')
                i_idx -= 1
                continue
    
    operations.reverse()
    return operations


def main():
    costs_list = list(map(int, input().split()))
    
    if len(costs_list) == 3:
        cost_replace_val = costs_list[0]
        cost_insert_val = costs_list[1]
        cost_delete_val = costs_list[2]
        cost_delete_two_val = cost_delete_val * 2
        costs_list = [cost_replace_val, cost_insert_val, cost_delete_val, cost_delete_two_val]
    
    str_a = input().strip()
    str_b = input().strip()
    
    operations, _ = edit_distance_with_operations(costs_list, str_a, str_b)
    
    ops_string = ''.join(operations)
    print(ops_string)
    print(str_a)
    print(str_b)

if __name__ == "__main__":
    main()