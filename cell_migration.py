import numpy as np

def caculate_branch_probability(seg_cells, tau, branch_alpha):
    n1 = seg_cells[14]['num']  # Number of cells in branch 15
    n2 = seg_cells[39]['num']  # Number of cells in branch 40
    tau1 = tau[14]  # Shear stress in branch 15
    tau2 = tau[39]  # Shear stress in branch 40
    # Calculate probabilities based on shear stress and cell number
    P_tau1 = tau1 / (tau1 + tau2) if tau1 + tau2 != 0 else 0.5
    # P_tau2 = tau2 / (tau1 + tau2) 
    P_n1 = n1 / (n1 + n2) if n1 + n2 != 0 else 0.5
    # P_n2 = n2 / (n1 + n2)
    P1 = branch_alpha * P_tau1 + (1 - branch_alpha) * P_n1
    # P2 = branch_alpha * P_tau2 + (1 - branch_alpha) * P_n2
    return P1

def cell_migration(seg, seg_cells, new_seg_cells, migrate, Q, branch_rule, branch_alpha=None, tau=None):
    """Handle cellular migration in the agent-based model."""

    cell_size = 10e-6  # Set the size of each cell (m)
    mchance = 1  # Assume full migration probability for now

    # Check if the segment contains cells
    if seg_cells[seg]['num'] != 0:
        for cell in range(int(seg_cells[seg]['num'])-1, -1, -1):
            mcell = np.random.rand()
            if mcell <= mchance:  # Determine if cell migrates
                polar_vect = seg_cells[seg]['polarity'][cell]
                migrate_vect = cell_size * polar_vect

                # Migration logic based on segment index
                ### Handle segments 0 and 20
                if seg == 0:
                    if migrate_vect[1] >= cell_size / 2:
                        
                        new_seg_cells[seg+1]['num'] += 1
                        new_seg_cells[seg+1]['polarity'].append(polar_vect)
                        new_seg_cells[seg]['polarity'].pop(cell)

                        migrate[seg] += 1
                    elif migrate_vect[1] <= -cell_size / 2:
                          
                        new_seg_cells[19]['num'] += 1
                        new_seg_cells[19]['polarity'].append(polar_vect)
                        new_seg_cells[seg]['polarity'].pop(cell)
                        
                        migrate[seg] += 1
                elif seg == 20:
                    if migrate_vect[1] >= cell_size / 2:
                          
                        new_seg_cells[seg+1]['num'] += 1
                        new_seg_cells[seg+1]['polarity'].append(polar_vect)
                        new_seg_cells[seg]['polarity'].pop(cell)
                                
                        migrate[seg] += 1
                    elif migrate_vect[1] <= -cell_size / 2:

                        new_seg_cells[4]['num'] += 1
                        new_seg_cells[4]['polarity'].append(polar_vect)
                        new_seg_cells[seg]['polarity'].pop(cell)
                                
                        migrate[seg] += 1
                ### Handle segments 1-3 and 21-24
                elif 1 <= seg <= 4 or (21 <= seg <= 24):
                    if migrate_vect[1] >= cell_size / 2:
                          
                        new_seg_cells[seg+1]['num'] += 1
                        new_seg_cells[seg+1]['polarity'].append(polar_vect)
                        new_seg_cells[seg]['polarity'].pop(cell)
                                
                        migrate[seg] += 1
                    elif migrate_vect[1] <= -cell_size / 2:
                        
                        new_seg_cells[seg-1]['num'] += 1
                        new_seg_cells[seg-1]['polarity'].append(polar_vect)
                        new_seg_cells[seg]['polarity'].pop(cell)
                                
                        migrate[seg] += 1
                ### Handle segments 5-14 and 25-34
                elif 5 <= seg <= 14 or (25 <= seg <= 34):
                    if migrate_vect[0] >= cell_size / 2:
                        
                        new_seg_cells[seg+1]['num'] += 1
                        new_seg_cells[seg+1]['polarity'].append(polar_vect)
                        new_seg_cells[seg]['polarity'].pop(cell)
                                
                        migrate[seg] += 1
                    elif migrate_vect[0] <= -cell_size / 2:
                        
                        new_seg_cells[seg-1]['num'] += 1
                        new_seg_cells[seg-1]['polarity'].append(polar_vect)
                        new_seg_cells[seg]['polarity'].pop(cell)
                                
                        migrate[seg] += 1
                ### Handle segments 16-18 and 35-38
                elif 16 <= seg <= 18 or (35 <= seg <= 38):
                    if migrate_vect[1] >= cell_size / 2:
                        
                        new_seg_cells[seg-1]['num'] += 1
                        new_seg_cells[seg-1]['polarity'].append(polar_vect)
                        new_seg_cells[seg]['polarity'].pop(cell)
                                
                        migrate[seg] += 1
                    elif migrate_vect[1] <= -cell_size / 2:
                        
                        new_seg_cells[seg+1]['num'] += 1
                        new_seg_cells[seg+1]['polarity'].append(polar_vect)
                        new_seg_cells[seg]['polarity'].pop(cell)
                                
                        migrate[seg] += 1
                ### Handle segment 19
                elif seg == 19:
                    if migrate_vect[1] >= cell_size / 2:
                        
                        new_seg_cells[seg-1]['num'] += 1
                        new_seg_cells[seg-1]['polarity'].append(polar_vect)
                        new_seg_cells[seg]['polarity'].pop(cell)
                                
                        migrate[seg] += 1
                    elif migrate_vect[1] <= -cell_size / 2:
                        
                        new_seg_cells[0]['num'] += 1
                        new_seg_cells[0]['polarity'].append(polar_vect)
                        new_seg_cells[seg]['polarity'].pop(cell)
                                
                        migrate[seg] += 1
                ### Handle segment 39
                elif seg == 39:
                    if migrate_vect[1] >= cell_size / 2:

                        new_seg_cells[seg-1]['num'] += 1
                        new_seg_cells[seg-1]['polarity'].append(polar_vect)
                        new_seg_cells[seg]['polarity'].pop(cell)
                                
                        migrate[seg] += 1
                    elif migrate_vect[1] <= -cell_size / 2:

                        new_seg_cells[15]['num'] += 1
                        new_seg_cells[15]['polarity'].append(polar_vect)
                        new_seg_cells[seg]['polarity'].pop(cell)
                                
                        migrate[seg] += 1


                ### Handle bifurcation segment 15
                elif seg == 15:
                    if migrate_vect[1] <= -cell_size / 2:
                        
                        new_seg_cells[seg+1]['num'] += 1
                        new_seg_cells[seg+1]['polarity'].append(polar_vect)  
                        new_seg_cells[seg]['polarity'].pop(cell)
                                
                        migrate[seg] += 1
                    elif migrate_vect[1] >= cell_size / 2:
                        
                        new_seg_cells[seg]['polarity'].pop(cell)       
                        migrate[seg] += 1

                        # BR1: Choose based on shear stress
                        if branch_rule == 1:
                            if tau[14] > tau[39]:
                                new_seg_cells[14]['num'] += 1  # Choose branch 15
                                new_seg_cells[14]['polarity'].append(polar_vect)
                            else:
                                new_seg_cells[39]['num'] += 1  # Choose branch 40
                                new_seg_cells[39]['polarity'].append(polar_vect)
                        
                        # BR2: Choose the branch with the smallest direction change
                        elif branch_rule == 2:
                            # Calculate angle between parent and child branches
                            # theta1 = np.arccos(np.dot(polar_vect, [-1, 0]))  # Angle for branch 15
                            # theta2 = np.arccos(np.dot(polar_vect, [0, 1]))  # Angle for branch 40
                            # if theta1 < theta2:
                            #     new_seg_cells[14]['num'] += 1  # Choose branch 15
                            #     new_seg_cells[14]['polarity'].append(polar_vect)
                            # else:
                            #     new_seg_cells[39]['num'] += 1  # Choose branch 40
                            #     new_seg_cells[39]['polarity'].append(polar_vect)
                            new_seg_cells[39]['num'] += 1  # Choose branch 40
                            new_seg_cells[39]['polarity'].append(polar_vect)
                            
                        
                        # BR3: Random choice with equal probability
                        elif branch_rule == 3:
                            r = np.random.rand()
                            if r < 0.5:
                                new_seg_cells[14]['num'] += 1  # Choose branch 15
                                new_seg_cells[14]['polarity'].append(polar_vect)
                            else:
                                new_seg_cells[39]['num'] += 1  # Choose branch 40
                                new_seg_cells[39]['polarity'].append(polar_vect)
                
                        # BR4: Biased probability towards high-flow branch
                        elif branch_rule == 4:
                            r = np.random.rand()
                            if r < 0.7:
                                new_seg_cells[14]['num'] += 1  # Choose branch 15
                                new_seg_cells[14]['polarity'].append(polar_vect)
                            else:
                                new_seg_cells[39]['num'] += 1  # Choose branch 40
                                new_seg_cells[39]['polarity'].append(polar_vect)
                        
                        # BR5: Weighted average of shear stress and cell number
                        elif branch_rule == 5:
                            P1 = caculate_branch_probability(seg_cells, tau, branch_alpha)

                            # Randomly choose a branch based on probabilities
                            r = np.random.rand()
                            # print(r)
                            if r < P1:
                                new_seg_cells[14]['num'] += 1  # Choose branch 15
                                new_seg_cells[14]['polarity'].append(polar_vect)
                            else:
                                new_seg_cells[39]['num'] += 1  # Choose branch 40
                                new_seg_cells[39]['polarity'].append(polar_vect)

                # elif seg == 4:
                #     if migrate_vect[1] <= -cell_size / 2:
                        
                #         new_seg_cells[seg-1]['num'] += 1
                #         new_seg_cells[seg-1]['polarity'].append(polar_vect)  
                #         new_seg_cells[seg]['polarity'].pop(cell)
                #         migrate[seg] += 1
                        
                #     elif migrate_vect[1] >= cell_size / 2:
                          
                #         new_seg_cells[seg]['polarity'].pop(cell)       
                #         migrate[seg] += 1

                #         # BR1: Choose based on shear stress
                #         if branch_rule == 1:
                #             print(tau[5], tau[20])
                #             if tau[5] > tau[20]:
                #                 new_seg_cells[5]['num'] += 1  # Choose branch 5
                #                 new_seg_cells[5]['polarity'].append(polar_vect)
                #             else:
                #                 new_seg_cells[20]['num'] += 1  # Choose branch 20
                #                 new_seg_cells[20]['polarity'].append(polar_vect)
                        
                #         # BR2: Choose the branch with the smallest direction change
                #         elif branch_rule == 2:
                #             # Calculate angle between parent and child branches
                #             theta1 = np.arccos(np.dot(polar_vect, [1, 0]))  # Angle for branch 5
                #             theta2 = np.arccos(np.dot(polar_vect, [0, 1]))  # Angle for branch 20
                #             if theta1 < theta2:
                #                 new_seg_cells[5]['num'] += 1  # Choose branch 5
                #                 new_seg_cells[5]['polarity'].append(polar_vect)
                #             else:
                #                 new_seg_cells[20]['num'] += 1  # Choose branch 20
                #                 new_seg_cells[20]['polarity'].append(polar_vect)
                        
                #         # BR3: Random choice with equal probability
                #         elif branch_rule == 3:
                #             r = np.random.rand()
                #             if r < 0.5:
                #                 new_seg_cells[5]['num'] += 1  # Choose branch 5
                #                 new_seg_cells[5]['polarity'].append(polar_vect)
                #             else:
                #                 new_seg_cells[20]['num'] += 1  # Choose branch 20
                #                 new_seg_cells[20]['polarity'].append(polar_vect)
                
                #         # BR4: Biased probability towards high-flow branch
                #         elif branch_rule == 4:
                #             r = np.random.rand()
                #             if r < 0.7:
                #                 new_seg_cells[5]['num'] += 1  # Choose branch 5
                #                 new_seg_cells[5]['polarity'].append(polar_vect)
                #             else:
                #                 new_seg_cells[20]['num'] += 1  # Choose branch 20
                #                 new_seg_cells[20]['polarity'].append(polar_vect)
                        
                #         # BR5: Weighted average of shear stress and cell number
                #         elif branch_rule == 5:
                #             n1 = seg_cells[5]['num']  # Number of cells in branch 5
                #             n2 = seg_cells[20]['num']  # Number of cells in branch 20
                #             tau1 = tau[5]  # Shear stress in branch 5
                #             tau2 = tau[20]  # Shear stress in branch 20
                #             # Calculate probabilities based on shear stress and cell number
                #             P_tau1 = tau1 / (tau1 + tau2)
                #             P_tau2 = tau2 / (tau1 + tau2)
                #             P_n1 = n1 / (n1 + n2)
                #             P_n2 = n2 / (n1 + n2)
                #             P1 = branch_alpha * P_tau1 + (1 - branch_alpha) * P_n1
                #             P2 = branch_alpha * P_tau2 + (1 - branch_alpha) * P_n2
                            
                #             # Randomly choose a branch based on probabilities
                #             r = np.random.rand()
                #             if r < P1:
                #                 new_seg_cells[5]['num'] += 1  # Choose branch 5
                #                 new_seg_cells[5]['polarity'].append(polar_vect)
                #             else:
                #                 new_seg_cells[20]['num'] += 1  # Choose branch 20
                #                 new_seg_cells[20]['polarity'].append(polar_vect)       

        new_seg_cells[seg]['num'] -= migrate[seg]

    return seg_cells, new_seg_cells
