def edit_distance_with_variant(costs, str_a, str_b):
    n_val = len(str_a)
    m_val = len(str_b)
    
    cost_replace = costs[0]
    cost_insert = costs[1]
    cost_delete = costs[2]
    cost_delete_two = costs[3] if len(costs) > 3 else cost_delete * 2
    
    dp_table = create_dp_table(n_val, m_val, str_a, str_b, cost_replace, cost_insert, cost_delete, cost_delete_two)
    
    return dp_table[n_val][m_val]


def create_dp_table(n_val, m_val, str_a, str_b, cost_replace, cost_insert, cost_delete, cost_delete_two):
    dp_table = [[0] * (m_val + 1) for _ in range(n_val + 1)]
    
    init_first_row(dp_table, m_val, cost_insert)
    init_first_col(dp_table, n_val, cost_delete)
    fill_dp_table(dp_table, n_val, m_val, str_a, str_b,
                  cost_replace, cost_insert, cost_delete, cost_delete_two)
    
    return dp_table


def init_first_row(dp_table, m_val, cost_insert):
    for j_idx in range(1, m_val + 1):
        dp_table[0][j_idx] = dp_table[0][j_idx - 1] + cost_insert


def init_first_col(dp_table, n_val, cost_delete):
    for i_idx in range(1, n_val + 1):
        dp_table[i_idx][0] = dp_table[i_idx - 1][0] + cost_delete


def fill_dp_table(dp_table, n_val, m_val, str_a, str_b, cost_replace, cost_insert, cost_delete, cost_delete_two):
    for i_idx in range(1, n_val + 1):
        for j_idx in range(1, m_val + 1):
            compute_cell(dp_table, i_idx, j_idx, str_a, str_b,
                        cost_replace, cost_insert, cost_delete, cost_delete_two)


def compute_cell(dp_table, i_idx, j_idx, str_a, str_b, cost_replace, cost_insert, cost_delete, cost_delete_two):
    replace_cost = get_replace_cost(str_a, i_idx, str_b, j_idx, cost_replace)
    
    dp_table[i_idx][j_idx] = dp_table[i_idx - 1][j_idx - 1] + replace_cost
    dp_table[i_idx][j_idx] = min(dp_table[i_idx][j_idx], 
                                 dp_table[i_idx][j_idx - 1] + cost_insert)
    dp_table[i_idx][j_idx] = min(dp_table[i_idx][j_idx], 
                                 dp_table[i_idx - 1][j_idx] + cost_delete)
    
    if i_idx >= 2 and str_a[i_idx - 1] != str_a[i_idx - 2]:
        two_del_cost = dp_table[i_idx - 2][j_idx] + cost_delete_two
        dp_table[i_idx][j_idx] = min(dp_table[i_idx][j_idx], two_del_cost)


def get_replace_cost(str_a, i_idx, str_b, j_idx, cost_replace):
    if str_a[i_idx - 1] == str_b[j_idx - 1]:
        return 0
    return cost_replace


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
    
    result = edit_distance_with_variant(costs_list, str_a, str_b)
    print(result)

if __name__ == "__main__":
    main()
